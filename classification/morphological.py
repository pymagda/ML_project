import cv2 as cv
import numpy as np


class ColorBGR:
    blue, green, red = range(3)


class ColorEnhancement:
    def process_frame(self, img, color):
        """
        The pixels having a dominant component are extracted, while all others are set to zero.
        """
        channels = np.array(cv.split(img)).astype(int)
        s = np.array(np.sum(channels, axis=0) + np.finfo(float).eps)
        v = np.dstack((channels[color]-channels[(color+1) % 3], channels[color]-channels[(color+2) % 3])).min(axis=2)
        img_out = np.dstack((v/s, np.zeros(v.shape))).max(axis=2)
        return img_out


class ChromaticFilter:

    def __init__(self, d=20):
        self.D = d

    def process_frame(self, img):
        """
        Adapt the chromatic segmentation to obtain the red parts of the signs.
        The chromatic color decomposition of an image is computed using
            f(R,G,B) = (|R - G | + |G - B| + |B - R|) / 3D,
        where D is the degree of extraction of an achromatic color. It is empirically set to D = 20
        To extract the chromatic pixels, f (R, G, B) > 1 is used.
        """
        channels = np.array(cv.split(img)).astype(int)
        s = np.sum(np.dstack((np.abs(channels[ColorBGR.red]-channels[ColorBGR.green]),
                   np.abs(channels[ColorBGR.green]-channels[ColorBGR.blue]),
                   np.abs(channels[ColorBGR.blue]-channels[ColorBGR.red]))),
                   axis=2).astype(float)
        img_out = np.where((s/(3*self.D)) > 1, 0, 255).astype(float)
        return img_out


class TopHatFilter:
    def __init__(self):
        self.kernel = np.ones((5, 5), np.uint8)

    def process_frame(self, img):
        """
        Input must be in gray-scale.
        Emphasizes light pixels with a high contrast to their local environment, such as the inside of traffic signs.
        It is the difference between input image and opening of the image.
        Opening is just another name of erosion followed by dilation. It is useful in removing noise.
        """
        return cv.morphologyEx(img, cv.MORPH_TOPHAT, self.kernel)


class BlackHatFilter:
    def __init__(self):
        self.kernel = np.ones((5, 5), np.uint8)

    def process_frame(self, img):
        """
        Input must be in gray-scale.
        Emphasizes dark pixels with a high contrast to their local environment such as sign rims and some pictograms.
        It is the difference between the closing of the input image and input image.
        Closing is reverse of Opening, Dilation followed by Erosion.
        It is useful in closing small holes inside the foreground objects, or small black points on the object.
        """
        return cv.morphologyEx(img, cv.MORPH_BLACKHAT, self.kernel)


class Binarization:
    def process_frame(self, img):
        """
        Returns binary image. Input must be in gray-scale. The threshold used is empirically set to mean + 4 * standard deviation of
        the pixel values over the entire filtered image.
        """
        std = np.std(img)
        mean = np.mean(img)
        threshold = mean + 4 * std

        _, img_out = cv.threshold(img.astype(np.float32), threshold, 255, cv.THRESH_BINARY)
        return img_out
