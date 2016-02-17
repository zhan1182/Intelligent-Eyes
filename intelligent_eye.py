#! /usr/bin/env python

__author__ = 'Jinyi'

import os
import sys

import src.client

from PySide.QtCore import *
from PySide.QtGui import *

from ui.intelligent_eye_GUI import *

class Intelligent_Eye(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super(Intelligent_Eye, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':

	currentApp = QApplication(sys.argv)
	currentForm = Intelligent_Eye()

	currentForm.show()
	currentApp.exec_()


