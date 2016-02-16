#! /usr/bin/env python

import socket

if __name__ == '__main__':

	ip = '192.168.0.100'
	port = 8888

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect((ip, port))
	print s.recv(1024)
	s.close 