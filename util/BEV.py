

import cv2
import numpy as np
from collections import defaultdict

IMAGE_RATIO = 1.3


def on_line(p1, p2, ycoord):
    return [int(p1[0]+ (p2[0]-p1[0])/float(p2[1]-p1[1])*(ycoord-p1[1])), ycoord]


def main(img, debugging = False):
    img_original = img.copy()

    mean_position = [0,0]
    mean_position[1], mean_position[0], _ = img.shape

    mean_position[1] = mean_position[1] / 2
    mean_position[0] = mean_position[0] / 2

    top = mean_position[1] + 20
    bottom,width,_=img.shape
    bottom = bottom + 0
    width = int(width*2 / 5)
    p1 = [int(mean_position[0] - width/2), top]
    p2 = [int(mean_position[0] + width/2), top]
    p3 = on_line(p2, mean_position, bottom)
    p4 = on_line(p1, mean_position, bottom)

    warped_image_size = [int(mean_position[0]), int(mean_position[0] * IMAGE_RATIO)]

    src_points = np.array([p1,p2,p3,p4], dtype = np.float32)
    dst_points = np.array([[0,0],[warped_image_size[0],0],[warped_image_size[0],warped_image_size[1]],[0,warped_image_size[1]]], dtype=np.float32)

    if debugging == True:
        cv2.polylines(img, [src_points.astype(np.int32)], True, (0,0,255), thickness = 1)

    perspective = cv2.getPerspectiveTransform(src_points, dst_points)
    warpped_image = cv2.warpPerspective(img, perspective, (warped_image_size[0], warped_image_size[1]))

    return warpped_image