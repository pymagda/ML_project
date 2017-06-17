import classification.morphological as cm
import segmentation.segmentation_masks as sm
import detection.shape_detection as sd
from sklearn.externals import joblib
from skimage.feature import hog
import movement.robot_move as mr
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
    sw = sm.SlidingWindow(img_org)

    # uncomment to train cls
    # cls = sd.HogRandomForrestArrows()
    # cls = sd.HogSvm()

    # load cls data
    clf_round = joblib.load("round_signs_cls.pkl")
    clf_arrow = joblib.load("rf_signs_arrow_cls.pkl")

    for ind, i in enumerate(sw.process_frame(img)):
        fd = hog(cv.resize(i, (32, 32)), orientations=9, pixels_per_cell=(4, 4),
                      cells_per_block=(8, 8), visualise=False)
        is_round = clf_round.predict(np.array([fd], 'float64'))

        if is_round:
            arrow = clf_arrow.predict(np.array([fd], 'float64'))
            print arrow
            mr.process_arrow(arrow)
            #cv.namedWindow('image'+str(ind), cv.WINDOW_NORMAL)
            #cv.imshow('image'+str(ind), i)

    # cv.waitKey(0)
    # cv.destroyAllWindows()
