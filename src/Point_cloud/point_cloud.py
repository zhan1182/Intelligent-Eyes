from stereovision.calibration import StereoCalibration
from stereovision.blockmatchers import StereoSGBM
from stereovision.point_cloud import PointCloud
from stereovision.stereo_cameras import CalibratedPair

import cv2
from glob import glob


class Point_cloud():

    def __init__(self, calib_foler = 'calib_files_test', SGBM_setting = 'settings/SGBM'):
        self.calibration = StereoCalibration(input_folder=calib_foler)
        self.block_matcher = StereoSGBM()
        self.block_matcher.load_settings(settings=SGBM_setting)
        self.CalibratedPair = CalibratedPair(None, self.calibration, self.block_matcher)
        self.imageSize = (1280, 720)
        self.left_img = None
        self.right_img = None

    def load_image(self, leftPath, rightPath):
        self.left_img = cv2.imread(leftPath)
        self.right_img = cv2.imread(rightPath)

    def rectify_image(self):
        return self.calibration.rectify([self.left_img, self.right_img])

    def get_disparity(self):
        imagePair = self.rectify_image()
        return self.block_matcher.get_disparity(imagePair)

    def get_point_cloud(self, filename):
        rectify_pair = self.CalibratedPair.calibration.rectify([self.left_img, self.right_img])
        points = self.CalibratedPair.get_point_cloud(rectify_pair)
        points = points.filter_infinity()
        points.write_ply(filename)



    def highlight_point_cloud(self, rectangle):
        rectify_pair = self.CalibratedPair.calibration.rectify([self.left_img, self.right_img])
        disparity = self.get_disparity()
        points = self.block_matcher.get_3d(disparity, self.calibration.disp_to_depth_mat)
        colors = rectify_pair[0]


        #Conver to homogeneous coord
        pta = rectangle[0] + (1,)
        ptb = rectangle[1] + (1,)
        ptc = rectangle[2] + (1,)
        ptd = rectangle[3] + (1,)
        for row in range(0, self.imageSize[1]):
            for col in range(0, self.imageSize[0]):
                p = (col, row, 1)
                if pointInQuadrilateral(p, pta, ptb, ptc, ptd):
                    colors[row, col, 0] = 255
                    colors[row, col, 1] = 0
                    colors[row, col, 2] = 0
        point_cloud = PointCloud(points, colors)
        point_cloud.write_ply('test.ply')

    def find_pos(self, quadra):
        rectify_pair = self.CalibratedPair.calibration.rectify([self.left_img, self.right_img])
        disparity = self.block_matcher.get_disparity(rectify_pair)
        points = self.block_matcher.get_3d(disparity,
                                           self.calibration.disp_to_depth_mat)


        #Find the larger rectangle that contains quadrilateral
        rmin = min(map(lambda x: x[0], quadra))
        rmax = max(map(lambda x: x[0], quadra))
        cmin = min(map(lambda x: x[1], quadra))
        cmax = max(map(lambda x: x[1], quadra))

        point_lst = []

        pta = quadra[0] + (1,)
        ptb = quadra[1] + (1,)
        ptc = quadra[2] + (1,)
        ptd = quadra[3] + (1,)
        for row in range(rmin, rmax + 1):
            for col in range(cmin, cmax + 1):
                p = (col, row, 1)
                # if pointInQuadrilateral(p, pta, ptb, ptc, ptd):
                point_lst.append(points[row, col])

        x_list = map(lambda x: x[0], point_lst)
        x_list.sort()
        y_list = map(lambda x: x[1], point_lst)
        y_list.sort()
        z_list = map(lambda x: x[2], point_lst)
        z_list.sort()
        print(len(x_list))
        median = (x_list[len(x_list) / 2], y_list[len(y_list) / 2], z_list[len(z_list) / 2])

        return median





def crossProduct(a, b):
    if len(a) != 3 or len(b) != 3:
        raise ValueError("The dimension of a or b is not 3")
    cp0 = a[1] * b[2] - b[1] * a[2]
    cp1 = a[2] * b[0] - b[2] * a[0]
    cp2 = a[0] * b[1] - b[0] * a[1]
    cp = (cp0, cp1, cp2)
    return cp


def dotProduct(a, b):
    if len(a) != len(b):
        raise ValueError("The dimensions of a and b are not same")
    return sum(map(lambda x, y: x * y, a, b))


def scale(a):
    if len(a) != 3:
        raise  ValueError("The dimension of a is not 3")
    ret = (a[0] / a[2], a[1] / a[2], 1)
    return ret


def vec_minus(a, b):
    if len(a) != len(b):
        raise ValueError("The dimensions of a and b are not same")
    return tuple(map(lambda x, y: x-y, a, b))


def vec_plus(a, b):
    if len(a) != len(b):
        raise ValueError("The dimensions of a and b are not same")
    return tuple(map(lambda x, y: x+y, a, b))


def sameSide(pt0, pt1, a, b):
    cp1 = crossProduct(vec_minus(b, a), vec_minus(pt0, a))
    cp2 = crossProduct(vec_minus(b, a), vec_minus(pt1, a))
    return dotProduct(cp1, cp2) >= 0


def pointInTriangle(p, a, b, c):
    return sameSide(p, a, b, c) and sameSide(p, b, a, c) and sameSide(p, c, a, b)


def pointInQuadrilateral(p, a, b, c, d):
    return pointInTriangle(p, a, b, c) or pointInTriangle(p, a, d, c)



if __name__ == '__main__':

    pointCloud = Point_cloud()
    pointCloud.load_image('test/left_1.jpeg', 'test/right_1.jpeg')
    # pointCloud.highlight_point_cloud([(200, 200), (400, 200), (400, 400), (200, 400)])
    # pointCloud.get_point_cloud('test.ply')
    print(pointCloud.find_pos([(639, 359), (641, 359), (641, 361), (639, 361)]))
