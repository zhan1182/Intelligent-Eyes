#! /usr/bin/env python

__author__ = 'Jinyi'

import os
import sys
import signal
import subprocess

from PySide.QtCore import *
from PySide.QtGui import *

from ui.intelligent_eye_GUI import *

from scripts.connection_wrapper import Client, Server
import netifaces as ni

class Intelligent_Eye(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
    	'''
    		UI set up
    	'''
        super(Intelligent_Eye, self).__init__(parent)
        self.setupUi(self)

        '''
        	Init constants
        '''
        self.raspberry_ip = '192.168.0.123' # Static IP Address
        self.local_ip = ni.ifaddresses('wlan0')[2][0]['addr']
        self.port_intr = 9999
        self.port_video = 8888

        '''
        	Connect all buttons, set their init state
        '''
        self.btn_start.clicked.connect(self.start_preview)
        self.btn_stop.clicked.connect(self.stop_preview)
        self.btn_takePics.clicked.connect(self.take_pictures)
        self.btn_navigate.clicked.connect(self.navigate)

        self.btn_init()

    def btn_init(self):
    	pass


    def start_preview(self):
    	'''
    		Set a server socket
    		Init Client socket and connect to the raspberry ip
    		Send instruction to raspberry pi
    		Start mplayer locally
    		Start receiving data from the raspberry pi
    	'''
    	print('1')
    	server_video = Server(self.port_video)
    	print('2')

    	self.client_intr = Client(self.raspberry_ip, self.port_intr)
    	self.client_intr.connect()
    	self.client_intr.send('S' + self.local_ip)
    	self.client_intr.close()

    	server_video.receive_file()
    	print('3')

    	cmdline = ['mplayer', '-fps', '24', '-cache', '1024', '-']
    	self.player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)

    	while True:
    		video_data = server_video.receive_data()
    		if not video_data:
    			break
    		self.player.stdin.write(video_data)

    	# self.stop_preview()

    def stop_preview(self):
    	'''
    		Terminate the mplayer process and close the socket connection at the server side
    	'''
    	# self.player.terminate()

    def take_pictures(self):
    	'''
    		Init Client socket and connect to the raspberry ip
    		Send instruction to raspberry pi
    		Check the return message from the raspberry pi, which means images transmitting is done
    	'''
    	self.client_intr = Client(self.raspberry_ip, self.port_intr)
    	self.client_intr.connect()
    	self.client_intr.send('T' + self.local_ip)
    	chunk = self.client_intr.receive(16)
    	if chunk == 'done':
    		pass
    	self.client_intr.close()

    def navigate(self):
    	pass

def main():
	currentApp = QApplication(sys.argv)

	currentUI = Intelligent_Eye()
	currentUI.show()
	
	currentApp.exec_()


if __name__ == '__main__':
	main()
	

