#! /usr/bin/env python

__author__ = 'Jinyi'


import bluetooth

class Car_Control:

	def __init__(self, MAC, port):
		"""
		MAC: mac address string
		Phone: '78:F7:BE:74:9D:28'
		Bluetooth module: ''
		"""
		self.MAC = MAC
		self.port = port
		self.client = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

	def connect(self):
		self.client.connect((self.MAC, self.port))

	def send(self):
		self.client.send("hello")

	def close(self):
		self.client.close()

	def forward(self):
		pass

	def backward(self):
		pass

	def left(self):
		pass

	def right(self):
		pass

if __name__ == '__main__':
	
	MAC = '78:F7:BE:74:9D:28'
	port = 1

	control = Car_Control(MAC, port)

	control.connect()
	control.send()
	control.close()



