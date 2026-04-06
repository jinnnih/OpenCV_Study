import cv2 as cv
import numpy as np

# Sudoku 이미지 로드
img = cv.imread('sudoku.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 50, 150, apertureSize=3)

# 다양한 threshold 값으로 실험
thresholds = [30, 50, 70, 100]

for threshold in thresholds:
    lines = cv.HoughLinesP(edges, rho=1, theta=np.pi/180,
                           threshold=threshold, minLineLength=50, maxLineGap=10)
    
    result = img.copy()
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        print(f"threshold={threshold} → {len(lines)} lines detected")
        cv.imshow(f'threshold={threshold}', result)

cv.waitKey(0)
cv.destroyAllWindows()

