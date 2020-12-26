# -*- coding:utf-8 -*-
import cv2
import matplotlib.pyplot as plt
from timeit import timeit

def detection(image1, image2, method = cv2.TM_SQDIFF_NORMED) :
    result = cv2.matchTemplate(image1, image2, method)
    #返回最小值，最大值，最小值在数组的位置，最大值在数组的位置
    minValue, maxValue, minLocal, mxaLocal = cv2.minMaxLoc(result)
    topLeft = minLocal
    return topLeft

def drawrectangle(image, topLeft, bottomRight) :
    cv2.rectangle(image, topLeft, bottomRight, (255, 0, 0), 2)
    return image

def showImage(image) :
    plt.subplot(221), plt.imshow(image)
    plt.title('image'), plt.xticks([]), plt.yticks([])
    plt.show()

if __name__ == "__main__" :
    image = cv2.imread("E:\\cocAssistant\\core\\temp\\screen.jpg", 1)
    image = image[:, :, ::-1]
    image = image.copy()
    templ = image[450:780, 500:830]
    print(templ.shape)
    print(image.shape)
    w, h, c = templ.shape
    methods = [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED]
    topLeft = detection(image, templ)
    bottomRight = (topLeft[0] + w, topLeft[1] + h)
    image2 = drawrectangle(image, topLeft, bottomRight)
    showImage(image2)
