#!/usr/bin/env python

import numpy as np
import cv2

import sys

def det_overlap(r, found_filtered):
	r_x_left = r[0]
	r_y_up = r[1]
	r_width = r[2]
	r_height = r[3]

	r_x_right = r_x_left + r_width
	r_y_down = r_y_up + r_height

	left_up = False
	left_down = False
	right_up = False
	right_down = False

	len_found_filter = len(found_filtered)

	for ct in range(len_found_filter):
		x_left = found_filtered[ct][0]
		y_up = found_filtered[ct][1]
		width = found_filtered[ct][2]
		height = found_filtered[ct][3]
		
		x_right = x_left + width
		y_down = y_up + height

		if r_x_left >= x_left and r_x_left <= x_right:
			if r_y_up >= y_up and r_y_up <= y_down:
				left_up = True
			if r_y_down >= y_up and r_y_down <= y_down:
				left_down = True

		if r_x_right >= x_left and r_x_right <= x_right:
			if r_y_up >= y_up and r_y_up <= y_down:
				right_up = True
			if r_y_down >= y_up and r_y_down <= y_down:
				right_down = True


		if left_up or left_down or right_up or right_down:

			overlap_combine(left_up, left_down, right_up, right_down, r, ct, found_filtered)

			return

	found_filtered.append(r)

def overlap_combine(left_up, left_down, right_up, right_down, r, ct, found_filtered):

	if (left_up) and (not left_down) and (not right_up) and (not right_down):
		found_filtered[ct][2] = r[0] + r[2] - found_filtered[ct][0]
		found_filtered[ct][3] = r[1] + r[3] - found_filtered[ct][1]

	elif (not left_up) and (left_down) and (not right_up) and (not right_down):
		found_filtered[ct][2] = r[0] + r[2] - found_filtered[ct][0]
		found_filtered[ct][3] = found_filtered[ct][1] + found_filtered[ct][3] - r[1]
		found_filtered[ct][1] = r[1]

	elif (not left_up) and (not left_down) and (right_up) and (not right_down):
		found_filtered[ct][2] = found_filtered[ct][0] + found_filtered[ct][2] - r[0]
		found_filtered[ct][3] = r[1] + r[3] - found_filtered[ct][1]
		found_filtered[ct][0] = r[0]

	elif (not left_up) and (not left_down) and (not right_up) and (right_down):
		found_filtered[ct][2] = found_filtered[ct][0] + found_filtered[ct][2] - r[0]
		found_filtered[ct][3] = found_filtered[ct][1] + found_filtered[ct][3] - r[1]
		found_filtered[ct][0] = r[0]
		found_filtered[ct][1] = r[1]

	elif (left_up) and (left_down) and (not right_up) and (not right_down):
		found_filtered[ct][2] = r[0] + r[2] - found_filtered[ct][0]

	elif (not left_up) and (not left_down) and (right_up) and (right_down):
		found_filtered[ct][2] = found_filtered[ct][0] + found_filtered[ct][2] - r[0]
		found_filtered[ct][0] = r[0]

	elif (left_up) and (not left_down) and (right_up) and (not right_down):
		found_filtered[ct][3] = r[1] + r[3] - found_filtered[ct][1]

	elif (not left_up) and (left_down) and (not right_up) and (right_down):
		found_filtered[ct][1] = r[1]

	else:
		raise ValueError('Fully overlapped rectangle')



def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 1):
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.25 * w), int(0.1 * h)
        cv2.rectangle(img, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), thickness)
        # cv2.rectangle(img, (x, y), (w, h), (0, 255, 0), thickness)

def detect(image_list):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

    for fn in image_list:
		img = cv2.imread(fn)

		found, w = hog.detectMultiScale(img, winStride=(4, 4), padding=(16,16), scale=1.075)
		found_filtered = []

		for ri, r in enumerate(found):
			for qi, q in enumerate(found):
				if ri != qi and inside(r, q):
					break
			else:
				# Thresh hold check
				width = r[2]
				height = r[3]
				if width < 100 and height < 200:
					continue

				# r_pad_w, r_pad_h = int(0.25 * width), int(0.1 * height)
				# r[2] += r[0] - r_pad_w
				# r[3] += r[1] - r_pad_h
				# r[0] += r_pad_w
				# r[1] += r_pad_h
				# if not (r[2] >= 200 and r[3] >= 400):
				# 	det_overlap(r, found_filtered)
				# else:
				# 	found_filtered.append(r)

				found_filtered.append(r)

		# draw_detections(img, [max_rectange(found_filtered)], 1)
		# draw_detections(img, found_filtered, 1)
		# cv2.imwrite(fn, img)
	
    return max_rectange(found_filtered)

def max_rectange(found_filtered):
	if len(found_filtered) == 0:
		return None
	max_r = found_filtered[0]
	for r in found_filtered[1:]:
		if r[2] * r[3] > max_r[2] * max_r[3]:
			max_r = r
	return max_r

def detect_image_list(image_list, filename_list):
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

	tmp_list = range(len(image_list))

	for ct in tmp_list:

		img = image_list[ct]

		found, w = hog.detectMultiScale(img, winStride=(4, 4), padding=(16,16), scale=1.075)
		found_filtered = []

		for ri, r in enumerate(found):
			for qi, q in enumerate(found):
				if ri != qi and inside(r, q):
					break
			else:
				if r[2] < 100 and r[3] < 200:
					continue
				found_filtered.append(r)

		draw_detections(img, found_filtered, 1)
		cv2.imwrite(filename_list[ct], img)

	return found_filtered
	# return max_rectange(found_filtered)

if __name__ == '__main__':
    detect(sys.argv[1:])


