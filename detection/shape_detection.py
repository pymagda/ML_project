import os
from skimage.feature import hog
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import cv2 as cv

trained_svm_path = "round_signs_cls.pkl"
trained_rf_path = "rf_signs_arrows_cls.pkl"
trained_kn_path = "kn_signs_arrows_cls.pkl"

positive_files_train = os.listdir('data/train/round')
negative_files_train = os.listdir('data/train/non_round')

round_signs_train = [('data/train/round/' + sign) for sign in positive_files_train]
non_round_signs_train = [('data/train/non_round/' + sign) for sign in negative_files_train]

left_arrow_files_train = os.listdir('data/train/left')
right_arrow_files_train = os.listdir('data/train/right')
straight_arrow_files_train = os.listdir('data/train/straight')

left_arrow_signs_train = [('data/train/left/' + sign) for sign in left_arrow_files_train]
right_arrow_signs_train = [('data/train/right/' + sign) for sign in right_arrow_files_train]
straight_arrow_signs_train = [('data/train/straight/' + sign) for sign in straight_arrow_files_train]


class Arrows:
    left, right, straight = range(3)


class HogSvmRound:
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


class HogArrowsCls:
    def __init__(self, pixels_per_cell=4, cells_per_block=8):
        l_hog_fd = []
        l_labels = []
        self.cells_per_block = cells_per_block
        self.pixels_per_cell = pixels_per_cell

        for i, left_sign in enumerate(left_arrow_signs_train):
            img = cv.imread(left_sign, 0)
            img_gray = cv.GaussianBlur(img, (5, 5), 0)
            if img_gray.shape[0] < cells_per_block*pixels_per_cell or \
                img_gray.shape[1] < cells_per_block*pixels_per_cell: continue

            fd = hog(cv.resize(img_gray, (32, 32)), orientations=9, pixels_per_cell=(pixels_per_cell, pixels_per_cell),
                     cells_per_block=(cells_per_block, cells_per_block), visualise=False)
            l_hog_fd.append(fd)
            l_labels.append(Arrows.left)

        for i, right_sign in enumerate(right_arrow_signs_train):
            img = cv.imread(right_sign, 0)
            img_gray = cv.GaussianBlur(img, (5, 5), 0)
            if img_gray.shape[0] < cells_per_block*pixels_per_cell or \
                img_gray.shape[1] < cells_per_block*pixels_per_cell: continue

            fd = hog(cv.resize(img_gray, (32, 32)), orientations=9, pixels_per_cell=(pixels_per_cell, pixels_per_cell),
                     cells_per_block=(cells_per_block, cells_per_block), visualise=False)
            l_hog_fd.append(fd)
            l_labels.append(Arrows.right)

        for i, straight_sign in enumerate(straight_arrow_signs_train):
            img = cv.imread(straight_sign, 0)
            img_gray = cv.GaussianBlur(img, (5, 5), 0)
            if img_gray.shape[0] < cells_per_block*pixels_per_cell or \
                img_gray.shape[1] < cells_per_block*pixels_per_cell: continue

            fd = hog(cv.resize(img_gray, (32, 32)), orientations=9, pixels_per_cell=(pixels_per_cell, pixels_per_cell),
                     cells_per_block=(cells_per_block, cells_per_block), visualise=False)
            l_hog_fd.append(fd)
            l_labels.append(Arrows.straight)

        hog_fd = np.array(l_hog_fd, 'float64')
        labels = np.array(l_labels, 'int')

        clf = RandomForestClassifier()
        clf.fit(hog_fd, labels)

        clf2 = KNeighborsClassifier(algorithm='kd_tree')
        clf2.fit(hog_fd, labels)

        joblib.dump(clf, trained_rf_path, compress=3)
        joblib.dump(clf, trained_kn_path, compress=3)