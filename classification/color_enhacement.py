import cv2 as cv
import numpy as np


class ColorBGR:
    blue, green, red = range(3)


class ColorEnhancement:

    def __init__(self, img):
        self.img = img

    def process_frame(self, color):
        channels = np.array(cv.split(self.img)).astype(int)
        s = np.array(np.sum(channels, axis=0) + np.finfo(float).eps)
        v = np.dstack((channels[color]-channels[(color+1) % 3], channels[color]-channels[(color+2) % 3])).min(axis=2)
        output = np.dstack((v/s, np.zeros(v.shape))).max(axis=2)
        return output
