import numpy as np
import cv2 as cv
import sample_download
 
img = cv.imread(sample_download.get_sample('messi5.jpg','opencv'))
assert img is not None, "file could not be read, check with os.path.exists()"
 
res = cv.resize(img,None,fx=2, fy=2, interpolation = cv.INTER_CUBIC)
 
#OR
 
height, width = img.shape[:2]
res = cv.resize(img,(2*width, 2*height), interpolation = cv.INTER_CUBIC)

cv.imshow('img', img)
cv.imshow('res', res)
cv.waitKey(0)
cv.destroyAllWindows()