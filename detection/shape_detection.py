import os
from skimage.feature import hog
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
import numpy as np
import cv2 as cv


trained_svm_path = "round_signs_cls.pkl"

positive_files_train = os.listdir('data/train/round')
negative_files_train = os.listdir('data/train/non_round')

round_signs_train = [('data/train/round/' + sign) for sign in positive_files_train]
non_round_signs_train = [('data/train/non_round/' + sign) for sign in negative_files_train]


class HogSvm:
    def __init__(self, pixels_per_cell=4, cells_per_block=8):
        l_hog_fd = []
        l_labels = []
        self.cells_per_block = cells_per_block
        self.pixels_per_cell = pixels_per_cell

        train_size = len(non_round_signs_train) if len(round_signs_train) > len(non_round_signs_train)\
            else len(round_signs_train)

        for i, round_sign in enumerate(round_signs_train):
            if i > train_size: break
            img = cv.imread(round_sign, 0)
            img_gray = cv.GaussianBlur(img, (5, 5), 0)
            if img_gray.shape[0] < cells_per_block*pixels_per_cell or \
                img_gray.shape[1] < cells_per_block*pixels_per_cell: continue
            """
            The optimal size of the HOG descriptor was determined to be a 144 value vector with a block size,
            stride size and cell size of 4 pixels each. It proved to be the best compromise between processing
            requirements and performance.
            """
            fd = hog(cv.resize(img_gray, (32, 32)), orientations=9, pixels_per_cell=(pixels_per_cell, pixels_per_cell),
                     cells_per_block=(cells_per_block, cells_per_block), visualise=False)
            l_hog_fd.append(fd)
            l_labels.append(1)

        for i, non_round_sign in enumerate(non_round_signs_train):
            if i > train_size: break
            img = cv.imread(non_round_sign, 0)
            img_gray = cv.GaussianBlur(img, (5, 5), 0)
            if img_gray.shape[0] < cells_per_block*pixels_per_cell or \
                img_gray.shape[1] < cells_per_block*pixels_per_cell: continue
            """
            The optimal size of the HOG descriptor was determined to be a 144 value vector with a block size,
            stride size and cell size of 4 pixels each. It proved to be the best compromise between processing
            requirements and performance.
            """
            fd = hog(cv.resize(img_gray, (32, 32)), orientations=9, pixels_per_cell=(pixels_per_cell, pixels_per_cell),
                     cells_per_block=(cells_per_block, cells_per_block), visualise=False)

            l_hog_fd.append(fd)
            l_labels.append(0)

        hog_fd = np.array(l_hog_fd, 'float64')
        labels = np.array(l_labels, 'int')

        clf = LinearSVC()
        clf.fit(hog_fd, labels)
        joblib.dump(clf, trained_svm_path, compress=3)


