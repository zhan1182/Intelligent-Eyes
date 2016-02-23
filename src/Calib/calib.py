#!/usr/bin/env python
import cv2 as cv
import numpy as np
import argparse
from calib_exception import *

# calib r c size


class Camera:

    # Camera ID
    # cameraMatrix
    # distortionMatrix
    # focal length
    # horizontal view angle
    #

    def __init__(self, **kwargs):
        self.cameraMatrix = None
        self.distortionMatrix = None
        self.focal = 3.6
        self.error = 0
        self.patternSize = (6,9)
        self.corners = []
        self.img = []
        self.patternLength = 2.5

    def addCalibrateImg(self, filepath):
        img = cv.imread(filepath)
        ret, corners = cv.findChessboardCorners(image=img, patternSize=self.patternSize, )
        if not ret:
            raise ChessboardNotFound(filepath)

if __name__ == '__main__':
    pass
    # parser = argparse.ArgumentParser(description="Usage: ./Calib.py -r Row -c Column [-s Square_size] "
    #                                              "[--debug Debug_dir]")
    # parser.add_argument('-r', help='Number of chessboard corners in a row')
    # parser.add_argument('-c', help='Number of chessboard corners in a column')
    # parser.add_argument('-s', help='Size of square in actual world')
    # parser.add_argument('--debug', help='Draw corners on chessboard image')
    # imagename = "./calib_img/left00.jpg"
    # rows = 6
    # columns = 9
    # img = cv.imread(filename=imagename)
    # grey_img = cv.cvtColor(src=img, code=cv.COLOR_BGR2GRAY)
    # ret, corners = cv.findChessboardCorners(image=grey_img, patternSize=(rows, columns))
    # print(corners)
    # if not ret:
    #     raise ValueError("Chessboard corners are not found in " + imagename)
    # cv.cornerSubPix(grey_img, corners=corners, winSize=(11,11), zeroZone=(-1,-1),
    #                 criteria=(cv.TERM_CRITERIA_MAX_ITER+cv.TERM_CRITERIA_EPS, 30, 0.01))
    #
    # print(corners)
