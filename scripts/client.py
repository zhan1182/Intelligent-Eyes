#! /usr/bin/env python

import socket

class Client:

	def __init__(self, ip, port):
		'''
			ip = '192.168.0.123'
			port = 8888
		'''
		self.ip = ip
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self):
		self.s.connect((self.ip, self.port))

	def close(self):
		self.s.close()

	def send(self, message):
		sent_len = self.s.send(message)
		if sent_len == 0:
			raise RuntimeError('Socket connection broken')

	def receive(self):
		chunk = self.s.recv(16)
		if chunk == '':
			raise RuntimeError('Socket connection broken')
		
		


	

	