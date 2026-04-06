import cv2 as cv
import numpy as np

# 이미지 로드
img = cv.imread('road3-1.jpg')
scale = 0.5
img_resized = cv.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)))
gray = cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray, 100, 200, apertureSize=3)

# 다양한 threshold 값으로 실험
thresholds = [10, 20 , 22, 25] # 이중에서 22가 베스트

for threshold in thresholds:
    lines = cv.HoughLinesP(edges, rho=1, theta=np.pi/180,
                           threshold=threshold, minLineLength=30, maxLineGap=10)
    
    result = img_resized.copy()
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print(f"threshold={threshold} → {len(lines)}개 직선")
        cv.imshow(f'threshold={threshold}', result)

cv.waitKey(0)
cv.destroyAllWindows()
 