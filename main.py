import classification.morphological as cm
import segmentation.segmentation_masks as sm
import cv2 as cv

if __name__ == "__main__":
    ce = cm.ColorEnhancement()
    b = cm.Binarization()
    th = cm.TopHatFilter()
    bh = cm.BlackHatFilter()
    ch = cm.ChromaticFilter()

    img_org = cv.imread('data/znak_nakazu.jpg')

    img = b.process_frame(ce.process_frame(img_org, cm.ColorBGR.blue))
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.imshow('image', img)

    sw = sm.SlidingWindow(img_org)

    for ind, i in enumerate(sw.process_frame(img)):
        cv.namedWindow('image'+str(ind), cv.WINDOW_NORMAL)
        cv.imshow('image'+str(ind), i)

    cv.waitKey(0)
    cv.destroyAllWindows()
