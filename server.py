#! /usr/bin/env python

import socket
import os
import sys
import picamera

class Two_Cameras:
    
    def __init__(self, connection_instr):

        self.cam0 = picamera.camera.PiCamera(camera_num=0)
        self.cam0.resolution = (800, 600)
        self.cam0.framerate = 15
        
        self.cam1 = picamera.camera.PiCamera(camera_num=1)
        self.cam1.resolution = (800, 600)
        self.cam1.framerate = 15

        self.port_video = 8888

        self.connection_instr = connection_instr

    def set_connection_instr(self, connection_instr):
        self.connection_instr = connection_instr

    def start_preview(self, remote_ip):
        '''
        Connect the remote_ip socket as a client
        Assume a server has been created on the remote_ip
        '''
        self.client_video = socket.socket()
        self.client_video.connect((remote_ip, self.port_video))
        self.video_connection = self.client_video.makefile('wb')

        self.connection_instr.send('ACK')

        self.cam0.start_recording(self.video_connection, format='h264')

    def stop_preview(self):
        '''
        Stop Cam 0 preview, but keep the camera open
        Close the video connection and client socket
        '''
        self.cam0.stop_recording()
        self.video_connection.close()
        self.client_video.close()

        self.connection_instr.send('ACK')

    def take_pics(self, remote_ip):
        '''
        Take two pictures and scp them to the remote_ip
        After scp, send a message to inform the remote_ip that transmitting is done
        '''
        self.cam0.capture('cam0.jpeg', format='jpeg', use_video_port=True)
        self.cam1.capture('cam1.jpeg', format='jpeg', use_video_port=True)

        self.connection_instr.send('ACK')

    def decode(self, message):
        '''
        Decode the instruction message
        Execute the corresponding functions
        '''
        if message[0] == 'S':
            '''
            Start Preview
            '''
            self.start_preview(message[1:])

        elif message[0] == 'P':
            '''
            Stop Preview
            '''
            self.stop_preview()

        elif message[0] == 'T':
            '''
            Take two Pictures
            '''
            self.take_pics(message[1:])

        else:
            raise ValueError('Invalid Instruction')


def main():

    ip = '0.0.0.0'
    port_instr = 9999
    
    server_instr = socket.socket()
    server_instr.bind((ip, port_instr))
    server_instr.listen(1)

    print('Instruction server created, listening port {0}'.format(port_instr))

    two_cameras = None

    while 1:
        connection_instr, client_addr = server_instr.accept()

        if two_cameras == None:
            two_cameras = Two_Cameras(connection_instr)
        else:
            two_cameras.set_connection_instr(connection_instr)

        try:
            message = connection_instr.recv(16)
            print('message = {0}'.format(message))
            
            two_cameras.decode(message)

        finally:
            connection_instr.close()


if __name__ == '__main__':

    main()
    
