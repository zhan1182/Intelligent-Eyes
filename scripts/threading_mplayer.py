#! /usr/bin/env python

__author__ = 'Jinyi & Zhaoyang'

import threading
import subprocess

class Threading_Mplayer(threading.Thread):

	def __init__(self, server_video):
		
		threading.Thread.__init__(self)
		self.server_video = server_video
		self._exit_flag = False

	def run(self):

		cmdline = ['mplayer', '-fps', '24', '-cache', '1024', '-']
		self.player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)

		while True:
			video_data = self.server_video.receive_data()
			if not video_data or self._exit_flag:
				break
			self.player.stdin.write(video_data)


	def stop(self):
		self._exit_flag = True
		self.player.terminate()