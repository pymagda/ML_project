import classification.morphological as cm
import segmentation.segmentation_masks as sm
import detection.shape_detection as sd
from sklearn.externals import joblib
from skimage.feature import hog
from random import randint
import segmentation.loading_image as li
import movement.robot_move as move
import cv2 as cv
import numpy as np
import time


if __name__ == "__main__":

    #cls = sd.HogArrowsCls()
    #cls = sd.HogSvmRound(5, 10)
    ip_address = 'http://192.168.1.30:8080/video?x.mjpeg'
    ce = cm.ColorEnhancement()
    b = cm.Binarization()
    th = cm.TopHatFilter()
    bh = cm.BlackHatFilter()
    ch = cm.ChromaticFilter()
    mr = move.Robot_move()
    frame = li.Load_image(ip_address)
    commands = []
    test_set = np.random.randint(3, size=10)
    print "test_set", test_set
    detected_signs = []
    # load cls data
    clf_round = joblib.load("round_signs_cls.pkl")
    clf_arrow = joblib.load("rf_signs_arrows_cls.pkl")
    frame.start()
    time.sleep(5)

    while True:
        img_org = frame.getFrame()
        tic = time.clock()
        img2 = ce.process_frame(img_org, cm.ColorBGR.blue)
        img = b.process_frame(img2)
        cv.namedWindow('image', cv.WINDOW_NORMAL)
        cv.imshow('image', img2)
        sw = sm.SlidingWindow(img_org)

        for ind, i in enumerate(sw.process_frame(img)):
            fd = hog(cv.resize(i, (50, 50)), orientations=9, pixels_per_cell=(5, 5),
                          cells_per_block=(10, 10), visualise=False)
            is_round = clf_round.predict(np.array([fd], 'float64'))

            if is_round:
                #print "is round"
                arrow = clf_arrow.predict(np.array([fd], 'float64'))
                commands.append(arrow[0])
                continue

        if len(commands) > 20:
            #print "bincount", np.bincount(np.array(commands))
            sign = np.argmax(np.bincount(np.array(commands)))
            print "sign", sign
            print "test", test_set
            detected_signs.append(sign)
            #mr.process_arrow(sign)
            time.sleep(2)
            commands = []

                #cv.namedWindow('image'+str(ind), cv.WINDOW_NORMAL)
                #cv.imshow('image'+str(ind), i)


        cv.waitKey(1)

    #print "detected_signs", detected_signs
