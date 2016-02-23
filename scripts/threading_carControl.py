#! /usr/bin/env python

import threading
import Tkinter as tk


def forward(event):
	pass

def backward(event):
	pass

def left(event):
	pass

def right(event):
	pass
		

class Threading_CarControl(threading.Thread):

	def __init__(self):
		
		threading.Thread.__init__(self)
		self._exit_flag = False

	def run(self):
		"""
		Listen key board input
		"""
		pass

	def stop(self):
		self._exit_flag = True