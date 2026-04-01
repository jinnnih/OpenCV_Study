# 회색조 1채널 히스토그램
import cv2 as cv 
import urllib.request
import sys 
import os
from matplotlib import pyplot as plt

# github sample 주소 : https://github.com/opencv/opencv/tree/master/samples/data
def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return cv.imread(filename)

# 이미지를 그레이스케일로 읽기
img = get_sample("orange.jpg")
img_gray = cv.imread("orange", cv.IMREAD_GRAYSCALE)
if img is None:
    sys.exit("Could not read the image.")

cv.imshow('img', img)
# cv.imshow('img_gray', img_gray)

# 히스토그램 계산
hist = cv.calcHist([img], [0], None, [256], [0, 256])

# 히스토그램 그리기
plt.plot(hist)
print("hist.shape:", hist.shape)  # (256, 1)
print("hist.sum():", hist.sum(), "img.shape:", img.shape)
plt.show()