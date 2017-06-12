import cv2 as cv
import numpy as np


class ColorEnhancement:

    def __init__(self, img):
        self.img = img

    def process_frame(self):
        (channel_b, channel_g, channel_r) = cv.split(self.img)
        s = np.array(channel_b + channel_g + channel_r) + np.finfo(float).eps
        v = np.dstack((channel_b-channel_g, channel_b-channel_r)).min(axis=2)
        output = np.dstack((v/s, np.zeros(v.shape))).max(axis=2)
        return output
