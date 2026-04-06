import cv2 as cv
import numpy as np
import math

# Sudoku 이미지 로드
img = cv.imread('sudoku.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 50, 150, apertureSize=3)

# 극좌표 방식
lines = cv.HoughLines(edges, 1, np.pi/180, 200)

# 극좌표 → 데카르트 좌표 변환 후 그리기
result = img.copy()
if lines is not None:
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        
        cv.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv.imshow('HoughLines (Polar)', result)
cv.waitKey(0)
cv.destroyAllWindows()

print(f"Detected {len(lines)} lines (polar form)")
