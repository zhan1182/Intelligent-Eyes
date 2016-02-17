#! /usr/bin/env python

import socket


def main():
	
	raspberry_pi_ip = '192.168.0.123'
	port = 8888

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.connect((raspberry_pi_ip, port))



	s.close

if __name__ == '__main__':

	main()
	