#! /usr/bin/env python

__author__ = 'Jinyi'

import socket

class Client:

	def __init__(self, ip, port):
		"""
			Raspberry_ip = '192.168.0.123'
			port_intrs = 9999
		"""
		self.ip = ip
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.ACK = 'ACK'

	def _connect(self):
		self.s.connect((self.ip, self.port))

	def _close(self):
		self.s.close()

	def _send(self, message):
		sent_len = self.s.send(message)
		if sent_len == 0:
			raise RuntimeError('Socket connection broken')

	def _receive(self, size):
		chunk = self.s.recv(size)
		if chunk == '':
			raise RuntimeError('Socket connection broken')
		return chunk

	def hand_shake(self, SYN):
		"""
		Send instruction to the server. Receive server's response.
		Return True if hand_shake success, else return False
		"""
		self._connect()
		self._send(SYN)
		return_code = self._receive(16)
		self._close()
		if return_code != self.ACK:
			raise RuntimeError('NACK')	
				

class Server:

	def __init__(self, port):
		"""
			ip = '0.0.0.0'
		"""
		self.ip = '0.0.0.0'
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind((self.ip, self.port))
		self.s.listen(1)

	def receive_file(self):
		self.connection = self.s.accept()[0].makefile('rb')

	def receive_data(self):
		return self.connection.read(1024)


	def close(self):
		self.s.close()



	