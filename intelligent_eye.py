#! /usr/bin/env python

__author__ = 'Jinyi'

import os
import sys
import signal
import subprocess
import netifaces as ni

from PySide.QtCore import *
from PySide.QtGui import *

from ui.intelligent_eye_GUI import *

from scripts.connection_wrapper import Client, Server
from scripts.threading_mplayer import Threading_Mplayer

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
        self.navigatable = False

        '''
        	Connect all buttons, set their init state
        '''
        self.btn_start.clicked.connect(self.start_preview)
        self.btn_stop.clicked.connect(self.stop_preview)
        self.btn_takePics.clicked.connect(self.take_pictures)
        self.btn_navigate.clicked.connect(self.navigate)

        self.btn_init()

    def btn_init(self):
    	self.btn_start.setEnabled(True)
    	self.btn_stop.setEnabled(False)
    	self.btn_takePics.setEnabled(False)
    	self.btn_navigate.setEnabled(False)

    def start_preview(self):
    	'''
    		Set a server socket
    		Init a Client socket and connect to the raspberry ip
    		Send instruction to raspberry pi, and get ready to receive the video file
    		Start another thread which runs mplayer locally
    		Keep reading video data and pipe them to mplayer
    		Toggle buttons
    	'''
    	self.server_video = Server(self.port_video)

    	self.client_intr = Client(self.raspberry_ip, self.port_intr)
    	self.client_intr.hand_shake('S' + self.local_ip)

    	self.server_video.receive_file()

    	self.mplayer_t = Threading_Mplayer(self.server_video)
    	self.mplayer_t.start()

    	self.btn_start.setEnabled(False)
    	self.btn_stop.setEnabled(True)
    	self.btn_takePics.setEnabled(True)

    def stop_preview(self):
    	'''
    		Send instruction to the raspberry pi to stop preview
    		Terminate the mplayer process and close the socket connection at the server side
    		Toggle buttons
    	'''
    	self.client_intr = Client(self.raspberry_ip, self.port_intr)
    	self.client_intr.hand_shake('P')

    	self.mplayer_t.stop()
    	self.server_video.close()

    	self.btn_start.setEnabled(True)
    	self.btn_stop.setEnabled(False)
    	self.btn_takePics.setEnabled(False)

    def take_pictures(self):
    	'''
    		Init Client socket and connect to the raspberry ip
    		Send instruction to raspberry pi
    		Check the return message from the raspberry pi, which means images transmitting is done
    		Toggle buttons and navigatable status
    	'''
    	self.client_intr = Client(self.raspberry_ip, self.port_intr)
    	self.client_intr.hand_shake('T' + self.local_ip)

    	self.btn_navigate.setEnabled(True)
    	self.navigatable = True

    def navigate(self):
    	pass


def main():
	currentApp = QApplication(sys.argv)

	currentUI = Intelligent_Eye()
	currentUI.show()
	
	currentApp.exec_()


if __name__ == '__main__':
	main()
	

