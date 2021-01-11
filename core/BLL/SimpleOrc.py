# -*- coding: utf-8 -*-

#水平投影
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from .ObjectDetection import showImage
from utils import utils, aircv

minThresh = 0
charactMinHeight = 10
charactMinWidth = 0

# 水平投影
def horizontalProjection(image) :
    height, width = image.shape[:2]
    horizontalList = [0 for z in range(0, height)]

    for row in range(0, height):
        for column in range(0, width):
            if image[row][column][0] == 0:
                horizontalList[row] += 1           #该行的计数器加一
                if horizontalList[row] > minThresh : #大于设定值提早结束行扫描
                    break
    return horizontalList

def horizontalCut(horizontalList, image):
    (begin, end) = (0, 0)
    height, width = image.shape[:2]
    cuts=[]
    for horizontalindex, blockCount in enumerate(horizontalList) :
        if blockCount >= minThresh and begin == 0 :
            begin = horizontalindex
        elif blockCount <= minThresh and begin != 0 or len(horizontalList) - 1 == horizontalindex and begin != 0 :
            end = horizontalindex
            if end - begin >= 2 :
                cuts.append((end - begin, begin, end))
                (begin, end) = (0, 0)

    cuts = sorted(cuts, reverse = True)
    imageArray = []
    for index in range(len(cuts)) :
        imageArray.append(image[cuts[index][1]:cuts[index][2], 0:width, :])
    return imageArray

# 垂直投影
def verticalProjection(image) :
    height, width = image.shape[:2]
    verticalList = [0 for z in range(0, width)]

    for column in range(0, width) :
        for row in range(0, height) :
            if image[row][column][0] == 0 :
                verticalList[column] += 1
                # if verticalList[column] > minThresh : #大于设定值提早结束行扫描
                #     break
    return verticalList

def verticalCut(verticalList, image) :
    height, width = image.shape[:2]
    (begin, end) = (0, 0)
    cuts=[]
    for verticalindex, blockCount in enumerate(verticalList) :
        if blockCount >= minThresh and begin == 0 :
            begin = verticalindex
        elif blockCount <= minThresh and begin != 0 :
            end = verticalindex
            cuts.append((end - begin, begin, end))
            (begin, end) = (0, 0)

    verticalArray = []
    cuts = sorted(cuts, reverse = True)
    for index in range(len(cuts)) :
        if cuts[index][0] > 1 :
            verticalArray.append((cuts[index][1], cuts[index][2]))

    for index, points in enumerate(verticalArray)  :
        image2 = image[0:height, points[0]:points[1], :]
        # showImage(image2)
        aircv.imwrite(f"E:\\cocAssistant\\core\\temp\\temp{index}.jpg", image2, 10)

    # showImage(image)
    return image

# #感知哈希算法作为文字快速查找得到核心算法
# def pHash(image) :
#     dct = cv2.dct(np.float32(image))
#     dct_roi = dct[0:8,0:8]
#     avreage = np.mean(dct_roi)
#     hash = 0
#     for i in range(dct_roi.shape[0]):
#         for j in range(dct_roi.shape[1]):
#             if dct_roi[i,j] > avreage:
#                 hash = hash * 2 + 1
#             else:
#                 hash = hash * 2
#     return hash

if __name__ == "__main__" :
    image = cv2.imread("E:\\cocAssistant\\core\\temp\\orc_test_line.png")
    # ret, image = cv.threshold(img, 80, 255, cv.THRESH_BINARY)
    a = horizontalProjection(image)
    imageArray = horizontalCut(a, image)
    for image in imageArray :
        showImage(image)
        verticalList = verticalProjection(image)
        image = verticalCut(verticalList, image)
        showImage(image)
        # print(verticalArray)

