import classification.morphological as cm
import segmentation.segmentation_masks as sm
from sklearn.externals import joblib
from skimage.feature import hog
import segmentation.loading_image as li
import movement.robot_move as move
import cv2 as cv
import numpy as np
import time


if __name__ == "__main__":

    # uncomment to generate cls
    # cls = sd.HogArrowsCls()
    # cls = sd.HogSvmRound(5, 10)

    ip_address = 'http://192.168.1.30:8080/video?x.mjpeg'
    clf_round_file = "round_signs_cls.pkl"
    clf_arrow_file = "rf_signs_arrows_cls.pkl"  # rf - RandomForrest, kn - K-d tree
    hog_pixels_per_cell = 5
    hog_cells_per_block = 10

    ce = cm.ColorEnhancement()
    b = cm.Binarization()
    th = cm.TopHatFilter()
    bh = cm.BlackHatFilter()
    ch = cm.ChromaticFilter()
    mr = move.Robot_move()

    frame = li.Load_image(ip_address)
    commands = []
    test_set = np.random.randint(3, size=10)

    clf_round = joblib.load(clf_round_file)
    clf_arrow = joblib.load(clf_arrow_file)
    frame.start()
    time.sleep(5)

    while True:
        img_org = frame.getFrame()
        binary_frame = ce.process_frame(img_org, cm.ColorBGR.blue)
        img = b.process_frame(binary_frame)
        cv.namedWindow('image', cv.WINDOW_NORMAL)
        cv.imshow('image', binary_frame)
        sw = sm.SlidingWindow(img_org)

        for ind, i in enumerate(sw.process_frame(img)):
            fd = hog(cv.resize(i, (hog_pixels_per_cell*hog_cells_per_block, hog_pixels_per_cell*hog_cells_per_block)),
                     orientations=9, pixels_per_cell=(hog_pixels_per_cell, hog_cells_per_block),
                     cells_per_block=(hog_cells_per_block, hog_cells_per_block), visualise=False)
            is_round = clf_round.predict(np.array([fd], 'float64'))

            if is_round:
                arrow = clf_arrow.predict(np.array([fd], 'float64'))
                commands.append(arrow[0])
                continue

        if len(commands) > 20:

            sign = np.argmax(np.bincount(np.array(commands)))
            mr.process_arrow(sign)
            time.sleep(2)
            commands = []

        cv.waitKey(1)
