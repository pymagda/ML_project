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





    """def __init__(self, ip_address):
        self.cap = cv2.VideoCapture(ip_address)

    def load_image(self):

        i = 0
        while True:
            ret, frame = self.cap.read()
            ret, frame = self.cap.read()
            ret, frame = self.cap.read()
            ret, frame = self.cap.read()
            ret, frame = self.cap.read()
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 0)
           # cv2.imshow('frame', frame)
            if cv2.waitKey(30) == 27:
                break
            yield frame
        self.cap.release()
        cv2.destroyAllWindows()"""