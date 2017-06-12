from classification.color_enhacement import ColorEnhancement, ColorBGR
import cv2 as cv

if __name__ == "__main__":
    img = cv.imread('data/znak_nakazu.jpg')
    c = ColorEnhancement(img)
    img2 = c.process_frame(ColorBGR.blue)
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.imshow('image', img2)
    cv.waitKey(0)
    cv.destroyAllWindows()
