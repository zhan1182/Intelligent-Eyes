# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/intelligent_eye_GUI.ui'
#
# Created: Wed Apr 20 21:21:24 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1120, 591)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_start = QtGui.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(110, 380, 98, 27))
        self.btn_start.setObjectName("btn_start")
        self.btn_stop = QtGui.QPushButton(self.centralwidget)
        self.btn_stop.setGeometry(QtCore.QRect(280, 380, 98, 27))
        self.btn_stop.setObjectName("btn_stop")
        self.btn_takePics = QtGui.QPushButton(self.centralwidget)
        self.btn_takePics.setGeometry(QtCore.QRect(710, 380, 98, 27))
        self.btn_takePics.setObjectName("btn_takePics")
        self.btn_navigate = QtGui.QPushButton(self.centralwidget)
        self.btn_navigate.setGeometry(QtCore.QRect(890, 380, 98, 27))
        self.btn_navigate.setObjectName("btn_navigate")
        self.view_cam0 = QtGui.QGraphicsView(self.centralwidget)
        self.view_cam0.setGeometry(QtCore.QRect(580, 60, 533, 300))
        self.view_cam0.setObjectName("view_cam0")
        self.view_cam1 = QtGui.QGraphicsView(self.centralwidget)
        self.view_cam1.setGeometry(QtCore.QRect(10, 60, 533, 300))
        self.view_cam1.setObjectName("view_cam1")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_start.setText(QtGui.QApplication.translate("MainWindow", "Start Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_stop.setText(QtGui.QApplication.translate("MainWindow", "Stop Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_takePics.setText(QtGui.QApplication.translate("MainWindow", "Take Pics", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_navigate.setText(QtGui.QApplication.translate("MainWindow", "Navigate", None, QtGui.QApplication.UnicodeUTF8))

