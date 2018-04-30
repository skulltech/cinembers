import numpy as np
import cv2 as cv
from contextlib import contextmanager



class Video:
	def __init__(self, name):
		self.cap = cv.VideoCapture(name)
		self.gray = False

	def frames(self):
		while True:
			ret, frame = self.cap.read()
			if not ret:
				break
			if self.gray:
				frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
			yield frame

	def __pairs(self):
		frames = self.frames()
		first = next(frames)
		for frame in frames:
			yield first, frame
			first = frame

	def SAD(self):
		for pair in self.__pairs():
			yield cv.absdiff(pair[0], pair[1]).sum()

	def norm(self):
		for pair in self.__pairs():
			yield cv.norm(pair[0], pair[1], cv.L1_NORM).sum()

	def close(self):
		self.cap.release()


@contextmanager
def video(name):
	vid = Video(name)
	yield vid
	vid.close()
