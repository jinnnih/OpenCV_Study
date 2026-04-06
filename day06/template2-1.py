import cv2 as cv
import numpy as np

# Sudoku 이미지 로드
img = cv.imread('sudoku.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Canny 에지 검출
edges = cv.Canny(gray, 50, 150, apertureSize=3)

# Hough Line Transform (선분 방식)
lines = cv.HoughLinesP(edges, rho=1, theta=np.pi/180,
                       threshold=50, minLineLength=50, maxLineGap=10)

# 검출된 직선 그리기
result = img.copy()
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 화면 표시
cv.imshow('Original', gray)
cv.imshow('Edges', edges)
cv.imshow('Hough Lines', result)
cv.waitKey(0)
cv.destroyAllWindows()

# 결과 저장 및 직선 개수 출력
cv.imwrite('hough_lines_result.jpg', result)
if lines is not None:
    print(f"Detected {len(lines)} lines")
