from classification.color_enhacement import ColorEnhancement
import cv2 as cv
import matplotlib.pyplot as plt

if __name__ == "__main__":
    img = cv.imread('data/znak_nakazu.jpg')
    c = ColorEnhancement(img)
    img2 = c.process_frame()
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.imshow('image', img2)
    cv.waitKey(0)
    cv.destroyAllWindows()
