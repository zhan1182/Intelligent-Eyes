#!/usr/bin/env python
import cv2 as cv
from copy import deepcopy
import numpy as np
import argparse
from glob import glob
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
        self.cameraID = 0
        self.camMat = None
        self.distMat = None
        self.rvec = None
        self.tvec = None
        self.newCam = None
        self.focal = 3.6
        self.error = 0
        self.patternSize = (6,9)
        self.corners = []
        self.img = []
        self.grey_img = []
        self.patternLength = 2.5
        self.image_count = 0
        self.__debug = True
        self.img_size = None
        self.obj_pts = []

        pattern_points = np.zeros( (np.prod(self.patternSize), 3), np.float32 )
        pattern_points[:,:2] = np.indices(self.patternSize).T.reshape(-1, 2)
        pattern_points *= self.patternLength
        self.pattern_points = pattern_points

    def addChessboardImg(self, filepath):
        img = cv.imread(filepath)
        grey_img = cv.cvtColor(src=img, code=cv.COLOR_BGR2GRAY)
        ret, corners = cv.findChessboardCorners(image=grey_img, patternSize=self.patternSize, )

        if not ret:
            raise ChessboardNotFound(filepath)
        cv.cornerSubPix(grey_img, corners, winSize=(5, 5), zeroZone=(-1, -1),
                        criteria=(cv.TERM_CRITERIA_MAX_ITER+cv.TERM_CRITERIA_EPS, 100, 0.001))
        if self.img_size is None:
            height, width = img.shape[:2]
            self.img_size = (width, height)
        if self.__debug:
            img_corner = deepcopy(img)
            cv.drawChessboardCorners(img_corner, self.patternSize, corners, True)
            debug_fn = filepath.replace("calib_img", "debug")
            cv.imwrite(debug_fn, img_corner)

        self.img.append(img)
        self.grey_img.append(grey_img)
        self.corners.append(corners.reshape(-1, 2))
        self.obj_pts.append(self.pattern_points)
        self.image_count += 1

    def Calibrate(self):
        if self.image_count < 10:
            raise ValueError("Chessboard images are not enough for accurate calibration")

        rms, cameraMat, dist, rvec, tvec = cv.calibrateCamera(self.obj_pts, self.corners, self.img_size, None, None)
        newCam = cv.getOptimalNewCameraMatrix(cameraMat, dist, self.img_size, 1, self.img_size, 0)
        self.newCam = newCam
        self.camMat = cameraMat
        self.distMat = dist
        self.rvec = rvec
        self.tvec = tvec
        print("Error:"+str(rms))

    def saveCalib(self):
        np.save("calib_files/cam-l.npy", self.camMat)
        np.save("calib_files/dist-l.npy", self.distMat)
        np.save("calib_files/rvec-l.npy", self.rvec)
        np.save("calib_files/tvec-l.npy", self.tvec)
        np.save("calib_files/newCam-l.npy", self.newCam)

    def __str__(self):
        retstr = 'Camera ID: '+str(self.cameraID)+'\n\n'
        retstr += 'CameraMatrix:\n'+str(self.camMat)+'\n\n'
        retstr += 'DistortionMatrix:\n'+str(self.distMat)+'\n\n'
        return retstr

if __name__ == '__main__':
    imgL = glob("calib_img/*l*.jpg")
    imgL.sort()
    imgR = glob("calib_img/*r*.jpg")
    imgR.sort()
    cam0 = Camera()
    cam0.__debug = True
    cam1 = Camera()
    cam1.__debug = True
    for file in imgL:
        cam0.addChessboardImg(file)
    cam0.Calibrate()
    cam0.saveCalib()
    # for file in imgR:
    #     cam1.addChessboardImg(file)
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
