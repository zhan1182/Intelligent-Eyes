#! /usr/bin/env python

import os

def main():

	uic_path = '/usr/local/lib/python2.7/dist-packages/PySide-1.2.4-py2.7-linux-x86_64.egg/PySide/scripts/uic.py'
	ui_file = 'ui/intelligent_eye_GUI.ui'
	target_file = 'ui/intelligent_eye_GUI.py'
	command = 'python ' + uic_path + ' ' + ui_file + ' -o ' + target_file

	os.system(command)

if __name__ == '__main__':

	main()