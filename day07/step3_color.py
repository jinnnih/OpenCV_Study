import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# ========== Step 1: 이미지 로드 (직접 읽기) ==========
# 주의: 흑백(GRAYSCALE)이 아닌 컬러로 읽어야 HSV 변환이 가능합니다.
img = cv.imread('stop_sign.jpg') 

if img is None:
    print("Error: 'stop_sign.jpg' 파일을 찾을 수 없습니다.")
    print("인터넷에서 정지 표지판 사진을 다운로드하여 같은 폴더에 넣어주세요.")
    exit()

# BGR을 HSV 색상 공간으로 변환
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# ========== Step 2: 빨간색 마스크 생성 ==========
# 1) 낮은 빨간색 범위
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
mask1 = cv.inRange(hsv, lower_red1, upper_red1)

# 2) 높은 빨간색 범위
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([180, 255, 255])
mask2 = cv.inRange(hsv, lower_red2, upper_red2)

red_mask = cv.bitwise_or(mask1, mask2)

# ========== Step 3: 노이즈 제거 (모폴로지) ==========
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
red_mask = cv.morphologyEx(red_mask, cv.MORPH_CLOSE, kernel)
red_mask = cv.morphologyEx(red_mask, cv.MORPH_OPEN, kernel)

# ========== Step 4: 컨투어 검출 ==========
contours, _ = cv.findContours(red_mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# ========== Step 5: 컨투어 필터링 ==========
min_area = 1000 
detected_signs = []

for contour in contours:
    area = cv.contourArea(contour)
    if area < min_area:
        continue
    
    perimeter = cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, 0.02 * perimeter, True)
    num_vertices = len(approx)
    
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = float(w) / h if h > 0 else 0
    
    # 정지 표지판(8각형) 조건: 꼭짓점 6~10개 사이, 종횡비 약 1:1
    if 6 <= num_vertices <= 10:
        if 0.8 <= aspect_ratio <= 1.2:
            detected_signs.append((x, y, w, h, num_vertices))

# ========== Step 6: 결과 시각화 ==========
result_img = img.copy()
for x, y, w, h, vertices in detected_signs:
    cv.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 3) # 초록색 박스
    cv.putText(result_img, f'Stop ({vertices}v)', (x, y - 10), 
               cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

plt.figure(figsize=(12, 6))
plt.subplot(121)
plt.imshow(red_mask, cmap='gray')
plt.title('Red Mask')
plt.subplot(122)
plt.imshow(cv.cvtColor(result_img, cv.COLOR_BGR2RGB))
plt.title(f'Detected: {len(detected_signs)}')
plt.show()