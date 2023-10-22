from PIL import Image
import cv2
import numpy as np
from pathlib import Path

DEBUG_ON = True

def write_image(path_name, mat):
    if DEBUG_ON:
        cv2.imwrite(path_name, mat)

file_string_output_root = "./imgOut/"

# 检测框
class Rectangle:
    def __init__(self, x, y, width, height, angle, types):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.types = types

# 检测结果结构体
class DetectionResult:
    def __init__(self):
        self.rect_angles = []
        self.contours = []

# 图像预处理参数，用于分割
class PreProcessParams:
    def __init__(self):
        self.adaGray = 50
        self.minGray = 50
        self.maxGray = 255
        self.closRadius = 2
        self.openRadius = 2
        self.adaSize = 50
        self.offset = 10

        self.processBright = False
        self.processDark = False
        self.imgProcessCloseing = False
        self.imgProcessOpening = False
        self.imgProcessAda = False

Path = str

preProcessParams = PreProcessParams()
preProcessParams.adaGray = 190
preProcessParams.minGray = 220
preProcessParams.maxGray = 255
preProcessParams.closRadius = 2
preProcessParams.openRadius = 2
preProcessParams.adaSize = 81
preProcessParams.offset = -15
preProcessParams.processBright = True  # Find white objects
preProcessParams.processDark = False  # Find dark objects
preProcessParams.imgProcessCloseing = True  # Enable closing operation
preProcessParams.imgProcessOpening = True  # Enable opening operation
preProcessParams.imgProcessAda = True  # Enable adaptive thresholding

def imgPreProcess(imgGray, preProcessParams):
    imgBright = np.zeros_like(imgGray)
    imgDark = np.zeros_like(imgGray)

    if preProcessParams.processBright:
        # Thresholding for bright objects
        ret, imgBright = cv2.threshold(
            imgGray, preProcessParams.minGray, preProcessParams.maxGray, cv2.THRESH_BINARY)
        cv2.imwrite(file_string_output_root+'imgBright.png', imgBright)

        if preProcessParams.imgProcessAda:
            # Adaptive thresholding for dark objects
            imgFilt = np.zeros_like(imgGray)
            ret, imgFilt = cv2.threshold(
                imgGray, preProcessParams.adaGray, preProcessParams.maxGray, cv2.THRESH_BINARY)
            imgAda = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, preProcessParams.adaSize, preProcessParams.offset)
            imgBright = (imgFilt & imgAda) | imgBright

            cv2.imwrite(file_string_output_root+'imgAda.png', imgAda)
            cv2.imwrite(file_string_output_root+'imgFilt.png', imgFilt)
            cv2.imwrite(file_string_output_root+'imgBright.png', imgBright)

        if preProcessParams.imgProcessCloseing:
            # Morphological closing for bright objects
            kernel = np.ones((preProcessParams.closRadius,
                             preProcessParams.closRadius), np.uint8)
            cv2.morphologyEx(imgBright, cv2.MORPH_CLOSE, kernel)
            cv2.imwrite(file_string_output_root+'imgBright.png', imgBright)

        if preProcessParams.imgProcessOpening:
            # Morphological opening for bright objects
            kernel = np.ones((preProcessParams.openRadius,
                             preProcessParams.openRadius), np.uint8)
            cv2.morphologyEx(imgBright, cv2.MORPH_OPEN, kernel)
            cv2.imwrite(file_string_output_root+'imgBright.png', imgBright)
        
        img = imgBright
    if preProcessParams.processDark:
        # region processDark
        # Thresholding operation to get dark regions
        cv2.threshold(imgGray, preProcessParams.minGray,
                      preProcessParams.maxGray, cv2.THRESH_BINARY_INV, imgDark)
        cv2.imwrite(file_string_output_root + "imgDark.png", imgDark)

        if preProcessParams.imgProcessAda:
            # Thresholding operation to get filtered image
            cv2.threshold(imgGray, preProcessParams.adaGray,
                          preProcessParams.maxGray, cv2.THRESH_BINARY_INV, imgFilt)
            # Adaptive thresholding operation to get AdaGrad image
            cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                                  preProcessParams.adaSize, preProcessParams.offset, imgAda)
            # Combine filtered and AdaGrad images with dark regions
            imgDark = (imgFilt & imgAda) | imgDark

            cv2.imwrite(file_string_output_root + "imgAda.png", imgAda)
            cv2.imwrite(file_string_output_root + "imgFilt.png", imgFilt)
            cv2.imwrite(file_string_output_root + "imgDark.png", imgDark)

        if preProcessParams.imgProcessCloseing:
            # Get structuring element for closing operation
            e = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (preProcessParams.closRadius, preProcessParams.closRadius))
            # Close operation on dark regions
            cv2.morphologyEx(imgDark, cv2.MORPH_CLOSE, e)
            cv2.imwrite(file_string_output_root + "imgDark.png", imgDark)

        if preProcessParams.imgProcessOpening:
            # Get structuring element for opening operation
            e = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE, (preProcessParams.openRadius, preProcessParams.openRadius))
            # Open operation on dark regions
            cv2.morphologyEx(imgDark, cv2.MORPH_OPEN, e)
            cv2.imwrite(file_string_output_root + "imgDark.png", imgDark)

        img = imgDark
    # endregion

    return img


def traditional_detect(imgGray, preProcessParams=preProcessParams, result=DetectionResult()):

    # Convert grayscale image to BGR
    img = imgPreProcess(imgGray, preProcessParams)

    # 找轮廓
    contours = []
    hierarchy = []
    ret, thresh = cv2.threshold(
        img, 127, 255, cv2.THRESH_BINARY)  # Thresholding the image
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    hierarchy = hierarchy[0]

    # 选出合适的轮廓
    areaThre = 400
    widthThre = 30
    heightThre = 30
    result.rect_angles = []
    for i in range(len(contours)):
        if hierarchy[i][3] == -1 and cv2.contourArea(contours[i]) > areaThre and cv2.arcLength(contours[i], True) > widthThre and cv2.arcLength(contours[i], True) > heightThre:
            rectangle = {}
            (rectangle['x'], rectangle['y']), (rectangle['width'], rectangle['height']), rectangle['angle'] = cv2.minAreaRect(
                contours[i])
            result.rect_angles.append(rectangle)
            # cv2.drawContours(imgGray, contours, i, (0, 0, 255), 8)
    result.contours = [c.tolist() for c in contours]
    # cv2.imwrite(file_string_output_root + "imgDrawContours.png", imgGray)
    return result

def main():
    svmfilestring = "./imgOut/"
    # Convert to grayscale
    imgGray = Image.open(svmfilestring + "standard.bmp").convert('L')
    result = DetectionResult()
    traditional_detect(np.array(imgGray), preProcessParams, result)
    print(result.rect_angles)


if __name__ == "__main__":
    main()
