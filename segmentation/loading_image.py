from threading import Thread

import cv2

class Load_image:
    def __init__(self, ip_address):
        self.currentFrame = None
        self.capture = cv2.VideoCapture(ip_address)

    def start(self):
        Thread(target=self.updateFrame, args=()).start()

        # Continually updates the frame

    def updateFrame(self):
        while True:
            ret, self.currentFrame = self.capture.read()

            while (self.currentFrame is None):
                ret, frame = self.capture.read()

    def getFrame(self):
        return cv2.flip(self.currentFrame, 0)
