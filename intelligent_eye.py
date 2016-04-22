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

from time import sleep, time
from threading import Timer

from src.Point_cloud.point_cloud import *

import math

class Intelligent_Eye(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
    	"""
    		UI set up, install event filter (key board listener)
    	"""
        super(Intelligent_Eye, self).__init__(parent)
        self.setupUi(self)
        self.installEventFilter(self) # Bind key listerner here
        self.point_cloud = Point_cloud(calib_foler='./src/Point_cloud/calib_files_test', SGBM_setting='./src/Point_cloud/settings/SGBM_1')

        """
        	Init constants
        """
        self.raspberry_ip = '192.168.0.123' # Static IP Address
        self.local_ip = ni.ifaddresses('wlan0')[2][0]['addr']
        self.port_intr = 9999
        self.port_video = 8888
        self.navigatable = False
        self.timer = True
        self.image_number = 0

        """
            Connect bluetooth module
        """
        self.bt_MAC = '20:14:08:05:43:82'
        self.bt_port = 1
        self.bt_control = Car_Control(self.bt_MAC, self.bt_port)

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
    	# self.btn_takePics.setEnabled(False)
    	self.btn_navigate.setEnabled(True)

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
    	# self.btn_takePics.setEnabled(False)

    def take_pictures(self):
    	"""
    		Init Client socket and connect to the raspberry ip
    		Send instruction to raspberry pi
    		Check the return message from the raspberry pi, which means images transmitting is done
    		Conduct human detection and display the results on the image views
    		Toggle buttons and navigatable status
            cam0: left
            cam1: right
    	"""
        self.client_intr = Client(self.raspberry_ip, self.port_intr)
        self.client_intr.hand_shake('T' + self.local_ip)
        check_call(['scp', '-q', 'pi@' + self.raspberry_ip + ':~/cam0.jpeg', 'pi@' + self.raspberry_ip + ':~/cam1.jpeg', './images/'])
        self.name1 = './images/left_' + str(self.image_number) + '.jpeg'
        self.name2 = './images/right_' + str(self.image_number) + '.jpeg'
        os.rename('./images/cam0.jpeg', self.name1)
        os.rename('./images/cam1.jpeg', self.name2)

        self.image_number += 1

    	# Calibration
        self.point_cloud.load_image(self.name1, self.name2)
        image_list = self.point_cloud.rectify_image()
        self.rectangle_coor_list = People_Detect.detect_image_list(image_list[:1], [self.name1])

        self._views_showImage(self.view_cam1, self.name1)
        self._views_showImage(self.view_cam0, self.name2)

        for rectangle_coor in self.rectangle_coor_list:
            x, y, w, h = rectangle_coor
            pad_w = int(0.2 * w)
            pad_h = int(0.2 * h)
            coor = [(x + pad_w, y + pad_h), (x + w - pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (x + pad_w, y + h - pad_h)]
            print(coor)
            coor_x, coor_y, coor_z = self.point_cloud.find_pos(coor)
            print(coor_x, coor_y, -coor_z)

    	self.btn_navigate.setEnabled(True)
    	self.navigatable = True

    def navigate(self):
    	if self.navigatable:
    		self._navigate()
    	else:
    		self.removeEventFilter(self) # Disable key listerner here
    		self.take_pictures()
    		self._navigate()
    		self.installEventFilter(self) # Enable key listerner here

    def _navigate(self):
    	for rectangle_coor in self.rectangle_coor_list:
            x, y, w, h = rectangle_coor
            pad_w = int(0.15 * w)
            pad_h = int(0.15 * h)
            coor = [(x + pad_w, y + pad_h), (x + w - pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (x + pad_w, y + h - pad_h)]
            print(coor)

            coor_x, coor_y, coor_z = self.point_cloud.find_pos(coor)

            print(coor_x, coor_y, coor_z)

            x_m = self._x_to_m(coor_x)
            z_m = self._z_to_m(coor_z)

            degree, distance = self._m_to_degree_distance(x_m, z_m)

            self._naviagete_send_request(degree, distance)            

    def _x_to_m(x):
        pass

    def _z_to_m(z):
        pass

    def _m_to_degree_distance(x_m, z_m):
        
        distance = math.sqrt(x_m * x_m + z_m * z_m)

        degree = int(math.atan2(x_m, z_m) / math.pi * 180.0)

        return degree, distance


    def _naviagete_send_request(degree, distance):
        t_distance = 1.2408 * distance + 0.2321

        if degree < 0:
            if degree == -1:
                self.bt_control.hand_shake('A')
        elif degree > 0:
            if degree == 1:
                self.bt_control.hand_shake('a')

        sleep(1)

        self.bt_control.forward()
        sleep(t_distance)
        self.bt_control.stop_motor()


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
            # if self.timer == False:
            # 	return True
            self.btn_navigate.setEnabled(False)
            self.navigatable = False
            if event.key() == Qt.Key_W:
                self.bt_control.forward()
            elif event.key() == Qt.Key_S:
                self.bt_control.backward()
            elif event.key() == Qt.Key_A:
                self.bt_control.left()
            elif event.key() == Qt.Key_D:
                self.bt_control.right()
            elif event.key() == Qt.Key_Escape:
                self.bt_control.stop_motor()

            # elif event.key() == Qt.Key_B:
            #     self.bt_control.forward()
            #     sleep(7)
            #     self.bt_control.stop_motor()

            return True

        elif event.type() == QEvent.KeyRelease:
            if self.timer ==  True:
                self.timer = False
                self.t = Timer(0.2, self.stop_motor)
                self.t.start()
            else:
                self.t.cancel()
                self.t = Timer(0.2, self.stop_motor)
                self.t.start()
            return True

        else:
            return QObject.eventFilter(self, obj, event)


    def stop_motor(self):
    	"""
    		Stop the motor, reset timer, enable navigate button
    	"""
    	self.bt_control.stop_motor()
    	self.timer = True

    	self.btn_navigate.setEnabled(True)

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
	

