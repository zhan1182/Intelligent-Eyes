#! /usr/bin/env python

__author__ = 'Jinyi'

import os
import sys

from src.client import Client

from PySide.QtCore import *
from PySide.QtGui import *

from ui.intelligent_eye_GUI import *

class Intelligent_Eye(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(Intelligent_Eye, self).__init__(parent)
        self.setupUi(self)

def main():
	# currentApp = QApplication(sys.argv)

	# currentUI = Intelligent_Eye()
	# currentUI.show()
	
	# currentApp.exec_()

	ip = '192.168.0.123'
	port = 8888

	client = Client(ip, port)
	


if __name__ == '__main__':
	main()
	

