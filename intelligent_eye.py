#! /usr/bin/env python

__author__ = 'Jinyi'

import os
import sys

from PySide.QtCore import *
from PySide.QtGui import *

from ui.intelligent_eye_GUI import *

from scripts.client import Client
import netifaces as ni

class Intelligent_Eye(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(Intelligent_Eye, self).__init__(parent)
        self.setupUi(self)

        '''
        	Init Client and connect the socket
        '''
        self.raspberry_ip = '192.168.0.123' # Static IP Address
        self.local_ip = ni.ifaddresses('wlan0')[2][0]['addr']
        self.port = 8888

        self.client = Client(self.raspberry_ip, self.port)
        '''
        	Connect all buttons
        '''
        self.btn_start.clicked.connect(self.start_preview)
        self.btn_stop.clicked.connect(self.stop_preview)

    def start_preview(self):
    	self.client.connect()
    	self.client.send('S' + self.local_ip)

    def stop_preview(self):
    	self.client.close()

def main():
	currentApp = QApplication(sys.argv)

	currentUI = Intelligent_Eye()
	currentUI.show()
	
	currentApp.exec_()


if __name__ == '__main__':
	main()
	

