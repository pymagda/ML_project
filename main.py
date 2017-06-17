import classification.morphological as cm
import segmentation.segmentation_masks as sm
import detection.shape_detection as sd
from sklearn.externals import joblib
from skimage.feature import hog
import segmentation.loading_image as li
import movement.robot_move as move
import cv2 as cv
import numpy as np

if __name__ == "__main__":

    ce = cm.ColorEnhancement()
    b = cm.Binarization()
    th = cm.TopHatFilter()
    bh = cm.BlackHatFilter()
    ch = cm.ChromaticFilter()
    mr = move.Robot_move()
    ip_address = 'http://192.168.1.30:8080/video?x.mjpeg'
    for img_org in li.load_image(ip_address):
        img2 = ce.process_frame(img_org, cm.ColorBGR.blue)
        img = b.process_frame(img2)
        cv.namedWindow('image', cv.WINDOW_NORMAL)
        cv.imshow('image', img2)
        sw = sm.SlidingWindow(img_org)

        # uncomment to train cls
        cls = sd.HogRandomForrestArrows()
        # cls = sd.HogSvm()

        # load cls data
        clf_round = joblib.load("round_signs_cls.pkl")
        clf_arrow = joblib.load("rf_signs_arrows_cls.pkl")

        for ind, i in enumerate(sw.process_frame(img)):
            fd = hog(cv.resize(i, (32, 32)), orientations=9, pixels_per_cell=(4, 4),
                          cells_per_block=(8, 8), visualise=False)
            is_round = clf_round.predict(np.array([fd], 'float64'))

            if is_round:
                arrow = clf_arrow.predict(np.array([fd], 'float64'))
                mr.process_arrow(arrow[0])
            
                #cv.namedWindow('image'+str(ind), cv.WINDOW_NORMAL)
                #cv.imshow('image'+str(ind), i)

        # cv.waitKey(0)
        # cv.destroyAllWindows()
