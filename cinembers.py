import argparse
import numpy as np
import cv2 as cv
from contextlib import contextmanager
import matplotlib.pyplot as plt



class Video:
	def __init__(self, name):
		self.cap = cv.VideoCapture(name)
		self.gray = False
		self.FPS = self.cap.get(cv.CAP_PROP_FPS)
		self.length = self.cap.get(cv.CAP_PROP_FRAME_COUNT)/self.FPS

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

	def __SAD(self):
		for pair in self.__pairs():
			yield cv.absdiff(pair[0], pair[1]).sum()

	def norm(self):
		for pair in self.__pairs():
			yield cv.norm(pair[0], pair[1], cv.NORM_L1)

	def plot_norm(self):
		norms = list(self.norm())
		plt.plot(norms)
		plt.xticks([int(i*self.FPS) for i in range(0, int(self.length), 10)], 
				   [i for i in range(0, int(self.length), 10)])
		plt.show()

	def close(self):
		self.cap.release()


@contextmanager
def video(name):
	vid = Video(name)
	yield vid
	vid.close()


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--video', required=True, type=str, help='Filename of video.')
	args = parser.parse_args()

	with video(args.video) as vid:
		vid.plot_norm()


if __name__=='__main__':
	main()
