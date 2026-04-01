import cv2 as cv
import numpy as np

# 1. 이미지 로드
img = cv.imread('./img/coins_spread1.jpg') 
if img is None:
    print("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
    exit()

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 2. 전처리 (블러 + 이진화)
gray_blur = cv.GaussianBlur(gray, (7, 7), 0)
ret, binary = cv.threshold(gray_blur, 100, 255, cv.THRESH_BINARY)

# 3. 모폴로지 (내부 구멍 메우기)
kernel = np.ones((5, 5), np.uint8)
binary_cleaned = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)

# 4. 컨투어 검출 (깨끗해진 binary_cleaned 사용!)
contours, _ = cv.findContours(binary_cleaned, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# 5. 그리기 및 카운팅
result = img.copy()
coin_count = 0
noise_count = 0

for cnt in contours:
    area = cv.contourArea(cnt)
    
    if area > 500: 
        coin_count += 1
        # 검출된 동전은 파란색(BGR: 255, 0, 0)으로 그리기
        cv.drawContours(result, [cnt], -1, (255, 0, 0), 3)
    else:
        noise_count += 1

# 결과 출력
print("-" * 30)
print(f"✅ 검출된 동전 개수: {coin_count}개")
print(f"❌ 제외된 노이즈 개수: {noise_count}개")
print("-" * 30)

cv.imshow('Original Binary', binary)        # 원본 이진화
cv.imshow('Cleaned Binary', binary_cleaned) # 구멍 메워진 이진화
cv.imshow('Result', result)                # 최종 결과

cv.waitKey(0)
cv.destroyAllWindows()