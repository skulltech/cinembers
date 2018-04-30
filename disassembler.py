import numpy as np
import cv2 as cv


def get_frames(name, gray=False):
	cap = cv.VideoCapture(name)
	
	while True:
		ret, frame = cap.read()
		if not ret:
			break
		if gray:
			frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		yield frame

	cap.release()
