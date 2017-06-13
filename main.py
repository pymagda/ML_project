import classification.morphological as cm
import cv2 as cv

if __name__ == "__main__":
    ce = cm.ColorEnhancement()
    b = cm.Binarization()
    th = cm.TopHatFilter()
    bh = cm.BlackHatFilter()
    ch = cm.ChromaticFilter()

    img = cv.imread('data/znak_nakazu.jpg')

    img2 = b.process_frame(th.process_frame(ce.process_frame(img, cm.ColorBGR.blue)))
    img3 = b.process_frame(bh.process_frame(ce.process_frame(img, cm.ColorBGR.blue)))
    img4 = b.process_frame(bh.process_frame(ch.process_frame(img)))

    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.namedWindow('image2', cv.WINDOW_NORMAL)
    cv.imshow('image', img2)
    cv.imshow('image2', img4)
    cv.waitKey(0)
    cv.destroyAllWindows()
