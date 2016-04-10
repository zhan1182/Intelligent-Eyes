#! /usr/bin/env python

__author__ = 'Jinyi'

import os
import sys
import signal
from subprocess import check_call
import netifaces as ni

from PySide.QtCore import *
from PySide.QtGui import *

from ui.intelligent_eye_GUI import *

from scripts.connection_wrapper import Client, Server
from scripts.threading_mplayer import Threading_Mplayer
from scripts.bluetooth_carControl import Car_Control

import scripts.peopledetect as People_Detect

from time import time
from threading import Timer

class Intelligent_Eye(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
    	"""
    		UI set up, install event filter (key board listener)
    	"""
        super(Intelligent_Eye, self).__init__(parent)
        self.setupUi(self)
        self.installEventFilter(self) # Bind key listerner here

        """
        	Init constants
        """
        self.raspberry_ip = '192.168.0.123' # Static IP Address
        self.local_ip = ni.ifaddresses('wlan0')[2][0]['addr']
        self.port_intr = 9999
        self.port_video = 8888
        self.navigatable = False
        self.timer = True

        """
            Connect bluetooth module
        """
        # self.bt_MAC = '20:14:08:05:43:82'
        # self.bt_port = 1
        # self.bt_control = Car_Control(self.bt_MAC, self.bt_port)

        """
        	Connect all buttons, set their init state
        """
        self.btn_start.clicked.connect(self.start_preview)
        self.btn_stop.clicked.connect(self.stop_preview)
        self.btn_takePics.clicked.connect(self.take_pictures)
        self.btn_navigate.clicked.connect(self.navigate)

        self.btn_init()

        """
            Display ready message
        """

    def btn_init(self):
    	"""
    		Init the states of buttons
    	"""
    	self.btn_start.setEnabled(True)
    	self.btn_stop.setEnabled(False)
    	self.btn_takePics.setEnabled(False)
    	self.btn_navigate.setEnabled(False)

    def start_preview(self):
    	"""
    		Set a server socket
    		Init a Client socket and connect to the raspberry ip
    		Send instruction to raspberry pi, and get ready to receive the video file
    		Start another thread which runs mplayer locally
    		Keep reading video data and pipe them to mplayer
    		Toggle buttons
    	"""
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
    	"""
    		Send instruction to the raspberry pi to stop preview
    		Terminate the mplayer process and close the socket connection at the server side
    		Toggle buttons
    	"""
    	self.client_intr = Client(self.raspberry_ip, self.port_intr)
    	self.client_intr.hand_shake('P')

    	self.mplayer_t.stop()
    	self.server_video.close()

    	self.btn_start.setEnabled(True)
    	self.btn_stop.setEnabled(False)
    	self.btn_takePics.setEnabled(False)

    def take_pictures(self):
    	"""
    		Init Client socket and connect to the raspberry ip
    		Send instruction to raspberry pi
    		Check the return message from the raspberry pi, which means images transmitting is done
    		Conduct human detection and display the results on the image views
    		Toggle buttons and navigatable status
    	"""
        # time.sleep(3)

    	self.client_intr = Client(self.raspberry_ip, self.port_intr)
    	self.client_intr.hand_shake('T' + self.local_ip)

    	check_call(['scp', '-q', 'pi@' + self.raspberry_ip + ':~/cam0.jpeg', 'pi@' + self.raspberry_ip + ':~/cam1.jpeg', './images/'])
    	name1 = './images/' + str(time()) + '_left.jpeg'
        name2 = './images/' + str(time()) + '_right.jpeg'
        os.rename('./images/cam0.jpeg', name1)
    	os.rename('./images/cam1.jpeg', name2)

    	new_capture_image_list = [name1, name2]

    	People_Detect.detect(new_capture_image_list)

        self._views_showImage(self.view_cam0, new_capture_image_list[0])
        self._views_showImage(self.view_cam1, new_capture_image_list[1])

    	self.btn_navigate.setEnabled(True)
    	self.navigatable = True

    def navigate(self):
    	pass


    def _views_showImage(self, view, image):
        """
            Display image on the view widget
        """
    	imageScene = QGraphicsScene()
        imageScene.addPixmap(QPixmap(image))

        view.setScene(imageScene)
        view.fitInView(imageScene.sceneRect(), Qt.KeepAspectRatio)
        view.show()

    def eventFilter(self, obj, event):
        """
            Listen and decode key board input: W, S, A, D
        """
        if event.type() == QEvent.KeyPress:
        	if event.key() == Qt.Key_W:
        		print("w")
        		# self.bt_control.forward()
        	elif event.key() == Qt.Key_S:
        		print("s")
        		# self.bt_control.backward()
        	elif event.key() == Qt.Key_A:
        		pass
        		# self.bt_control.left()
        	elif event.key() == Qt.Key_D:
        		pass
        		# self.bt_control.right()
        	elif event.key() == Qt.Key_Escape:
        		print("space")
        		# self.bt_control.stop_motor()
        	return True

        elif event.type() == QEvent.KeyRelease:
        	print(self.timer)
        	if self.timer ==  True:
        		print("start timer")
        		self.timer = False
        		self.t = Timer(0.2, stop_motor)
        		self.t.start()
        	else:
        		self.t.cancel()
        	return True

        else:
            return QObject.eventFilter(self, obj, event)


    def stop_motor(self):
    	# self.bt_control.stop_motor()
    	print("Release")
    	self.timer = True

def main():
    """
        Start the UI at the main thread
    """

    currentApp = QApplication(sys.argv)

    currentUI = Intelligent_Eye()
    currentUI.show()

    currentApp.exec_()


if __name__ == '__main__':
	main()
	

