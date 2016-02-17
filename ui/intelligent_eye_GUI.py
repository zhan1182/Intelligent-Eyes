# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'intelligent_eye_GUI.ui'
#
# Created: Tue Feb 16 22:16:35 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_start = QtGui.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(130, 400, 98, 27))
        self.btn_start.setObjectName("btn_start")
        self.btn_stop = QtGui.QPushButton(self.centralwidget)
        self.btn_stop.setGeometry(QtCore.QRect(130, 470, 98, 27))
        self.btn_stop.setObjectName("btn_stop")
        self.btn_takePics = QtGui.QPushButton(self.centralwidget)
        self.btn_takePics.setGeometry(QtCore.QRect(280, 400, 98, 27))
        self.btn_takePics.setObjectName("btn_takePics")
        self.btn_navigate = QtGui.QPushButton(self.centralwidget)
        self.btn_navigate.setGeometry(QtCore.QRect(440, 400, 98, 27))
        self.btn_navigate.setObjectName("btn_navigate")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
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

