import numpy as np
import cv2


cap = cv2.VideoCapture('/home/sumit/Downloads/IllustriousKindheartedGordonsetter.mp4')
# cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()
	print(ret)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	cv2.imshow('frame', gray)

	if cv2.waitKey(1) & 0xFF==ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
