import argparse
import numpy as np
import cv2 as cv
from contextlib import contextmanager
import matplotlib.pyplot as plt



class Video:
    def __init__(self, file, **kwargs):
        self.__capture = cv.VideoCapture(file)
        self.__FPS = self.__capture.get(cv.CAP_PROP_FPS)
        self.__length = self.__capture.get(cv.CAP_PROP_FRAME_COUNT) / self.__FPS
        self.__resolution = (self.__capture.get(cv.CAP_PROP_FRAME_WIDTH), self.__capture.get(cv.CAP_PROP_FRAME_HEIGHT))

        attributes = {
            'name': file,
            'minires': (100, int(100 * self.__resolution[1] / self.__resolution[0]))
        }
        keys = attributes.keys()
        attributes.update(kwargs)
        self.__dict__.update((k, v) for k, v in attributes.items() if k in keys)


    @property
    def capture(self):
        return self.__capture


    @property
    def FPS(self):
        return self.__FPS


    @property
    def length(self):
        return self.__length


    @property
    def resolution(self):
        return self.__resolution


    def frames(self, gray=True, mini=True):
        self.__capture.set(cv.CAP_PROP_POS_FRAMES, 0)

        while True:
            ret, frame = self.__capture.read()
            if not ret:
                break
            if gray:
                frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            if mini:
                frame = cv.resize(frame, self.minires)
            yield frame


    def __pairs(self):
        frames = self.frames(gray=True, mini=True)
        first = next(frames)

        for frame in frames:
            yield first, frame
            first = frame


    def __norm(self, pair):
        return cv.norm(pair[0], pair[1], cv.NORM_L1)


    def SAD(self):
        for pair in self.__pairs():
            yield self.__norm(pair)


    def HD(self):
        for pair in self.__pairs():
            hists = [cv.calcHist([frame], [0], None, [256], [0, 256]) for frame in pair]
            yield self.__norm(hists)


    def ECR(self, rate=5):
        div = lambda x, y: x / y if y != 0 else 0

        for pair in self.__pairs():
            edged = [cv.Canny(frame, 0, 200) for frame in pair]
            dilated = [cv.dilate(frame, np.ones((rate, rate))) for frame in edged]
            inverted = [255 - frame for frame in dilated]

            out_pixels = np.sum(edged[0] & inverted[1])
            in_pixels = np.sum(edged[1] & inverted[0])
            pixels = [np.sum(frame) for frame in edged]
            yield max(div(float(in_pixels), float(pixels[0])), div(float(out_pixels), float(pixels[1])))


    def close(self):
        self.__capture.release()



@contextmanager
def video(name):
    vid = Video(name)
    yield vid
    vid.close()


def main():
    parser = argparse.ArgumentParser(description='Generating numbers from movies, one movie at a time.')
    parser.add_argument('-v', '--video', required=True, type=str, help='Filename of video.')
    parser.add_argument('-s', '--score', required=True, type=str, help='Scoring method.', choices=['SAD', 'HD', 'ECR'])
    args = parser.parse_args()

    with video(args.video) as vid:
        switcher = {
            'SAD': vid.SAD(),
            'HD': vid.HD(),
            'ECR': vid.ECR()
        }

        data = list(switcher.get(args.score))
        plt.plot(data)
        plt.show()



if __name__=='__main__':
    main()
