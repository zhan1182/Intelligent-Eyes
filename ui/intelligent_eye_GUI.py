# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'intelligent_eye_GUI.ui'
#
# Created: Tue Feb 16 16:41:48 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.btn_start = QtGui.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(130, 400, 98, 27))
        self.btn_start.setObjectName(_fromUtf8("btn_start"))
        self.btn_stop = QtGui.QPushButton(self.centralwidget)
        self.btn_stop.setGeometry(QtCore.QRect(130, 470, 98, 27))
        self.btn_stop.setObjectName(_fromUtf8("btn_stop"))
        self.btn_takePics = QtGui.QPushButton(self.centralwidget)
        self.btn_takePics.setGeometry(QtCore.QRect(280, 400, 98, 27))
        self.btn_takePics.setObjectName(_fromUtf8("btn_takePics"))
        self.btn_navigate = QtGui.QPushButton(self.centralwidget)
        self.btn_navigate.setGeometry(QtCore.QRect(440, 400, 98, 27))
        self.btn_navigate.setObjectName(_fromUtf8("btn_navigate"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btn_start.setText(_translate("MainWindow", "Start Preview", None))
        self.btn_stop.setText(_translate("MainWindow", "Stop Preview", None))
        self.btn_takePics.setText(_translate("MainWindow", "Take Pics", None))
        self.btn_navigate.setText(_translate("MainWindow", "Navigate", None))

