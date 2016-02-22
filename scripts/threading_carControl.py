#! /usr/bin/env python


import threading
import subprocess

class Threading_CarControl(threading.Thread):

	def __init__(self):
		
		threading.Thread.__init__(self)
		self._exit_flag = False

	def run(self):
		pass

	def stop(self):
		self._exit_flag = True