import numpy as np
import imutils


class SlidingWindow:
    def __init__(self, img_orig):
        self.threshold = 0.03
        self.scale = 2
        self.min_size = (50, 50)
        self.step = 32
        self.w_factor = 3
        self.img_orig = img_orig

    def pyramid(self, img):
        yield img
        while True:
            img = imutils.resize(img, width=int(img.shape[1] / self.scale))
            if any(x < y for x, y in zip(img.shape, self.min_size)):
                break
            yield img

    def get_window(self, img, window_size):
        for y in xrange(0, img.shape[0], self.step):
            for x in xrange(0, img.shape[1], self.step):
                yield (x, y, img[y:y + window_size[1], x:x + window_size[0]])

    def process_frame(self, img):
        """
        The image is resized and scanned at different scales. The sum of the pixel values sum(img (x, y, w, h))
        in each subwindow img (x, y, w, h) is computed, where (x, y) and (w, h) are the top left corner,
        width and height of the subwindow in the image. If the ratio of the white pixels to the area of the subwindow
        area(img (x, y, w, h)) exceeds a given threshold, the subwindow is considered to contain a potential sign.
        """

        (win_w, win_h) = (img.shape[0]/self.w_factor, img.shape[1]/self.w_factor)
        for img in self.pyramid(img):
            for (x, y, window) in self.get_window(img, window_size=(win_w, win_h)):
                if window.shape[0] != win_h or window.shape[1] != win_w:
                    if np.sum(window)/(255*window.shape[0]*window.shape[1]) > self.threshold:
                        img_out = imutils.resize(self.img_orig, width=int(img.shape[1]))
                        yield img_out[y:y+window.shape[0], x:x+window.shape[1]]

