#! /usr/bin/env python

__author__ = 'Jinyi'

import time
import bluetooth
from connection_wrapper import Client

class Car_Control(Client):

	def __init__(self, MAC, port):
		"""
		MAC: mac address string
		Phone: '78:F7:BE:74:9D:28'
		Bluetooth module HC06: '20:14:08:05:43:82'
		"""
		Client.__init__(self, MAC, port)
		self.s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

		self.ACK = 'A'

		self._connect()

	def hand_shake(self, SYN):
		"""
		Overrding the parent function
		"""
		self._send(SYN)
		# return_code = self._receive(4)
		# if return_code != self.ACK:
		# 	raise RuntimeError('NACK')
	
	def stop_motor(self):
		self.hand_shake('0')

	def forward(self):
		"""
		Go straight forward
		"""
		self.hand_shake('1')

	def backward(self):
		self.hand_shake('2')

	def left(self):
		self.hand_shake()

	def right(self):
		self.hand_shake()

if __name__ == '__main__':
	
	MAC = '20:14:08:05:43:82'
	port = 1

	control = Car_Control(MAC, port)

	while 1:
		control.hand_shake('2')
		print("success")
		time.sleep(1)



