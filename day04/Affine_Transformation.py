import numpy as np
import cv2 as cv
import sample_download as spdl

img_file = spdl.get_sample('messi5.jpg','opencv')
img = cv.imread(img_file, cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"
rows,cols = img.shape

# 3개의 점의 대응관계 
pts1 = np.float32([[50,50],[200,50],[50,200]])
pts2 = np.float32([[10,100],[200,50],[100,250]]) 


# 어핀 변환 행렬 계산 
M = cv.getAffineTransform(pts1,pts2)
dst = cv.warpAffine(img,M,(cols,rows))
 
cv.imshow("Original", img)
cv.imshow("Affine", dst)
 

cv.waitKey(0)
cv.destroyAllWindows()


