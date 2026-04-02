import urllib.request
import os
import numpy as np 
import cv2 as cv 
import sample_download

img_file = sample_download.get_sample('messi5.jpg','opencv')
img = cv.imread(img_file, cv.IMREAD_GRAYSCALE)
h, w = img.shape

#res = cv.resize(img, None, fx=4, fy=4, interpolation = cv.INTER_CUBIC)
# 평행 이동 
# M = np.float32([[1, 0, 100], [0, 1, 50]])
# dst = cv.warpAffine(img, M, (w, h))

# 회전이동
M = cv.getRotationMatrix2D(((w-1)/2.0, (h-1)/2.0), 90, 1)
dst = cv.warpAffine(img, M, (w, h))

cv.imshow("Original", img)
#cv.imshow("Scaling", res)
#cv.imshow("Traslated", dst)
cv.imshow("Rotated", dst)

cv.waitKey(0)
cv.destroyAllWindows()