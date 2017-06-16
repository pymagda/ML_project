import classification.morphological as cm
import segmentation.segmentation_masks as sm
import detection.shape_detection as sd
from sklearn.externals import joblib
from skimage.feature import hog
import cv2 as cv
import numpy as np

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
    #cls = sd.HogSvm()
    clf = joblib.load("round_signs_cls.pkl")

    for ind, i in enumerate(sw.process_frame(img)):

        fd = hog(cv.resize(i, (32, 32)), orientations=9, pixels_per_cell=(4, 4),
                      cells_per_block=(8, 8), visualise=False)
        nbr = clf.predict(np.array([fd], 'float64'))
        cv.namedWindow('image'+str(ind), cv.WINDOW_NORMAL)
        cv.imshow('image'+str(ind), i)
        print(nbr)

    cv.waitKey(0)
    cv.destroyAllWindows()
