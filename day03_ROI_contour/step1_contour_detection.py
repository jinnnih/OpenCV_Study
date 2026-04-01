import cv2 as cv
import numpy as np

# 1. 이미지 로드 (파일명 수정 완료!)
img = cv.imread('./img/house.jpg') 
if img is None:
    print("파일을 찾을 수 없습니다.")
    exit()

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 2. 전처리 (하늘을 날리고 건물을 남기기 위해 블러와 적응형 이진화 사용)
gray_blur = cv.GaussianBlur(gray, (7, 7), 0) # 블러 크기를 약간 키워 노이즈 제거
# 배경이 밝으므로 THRESH_BINARY_INV를 사용하여 건물을 흰색으로 만듭니다.
# 마지막 인자 '5'를 조절하여 배경 노이즈를 더 강하게 억제합니다.
binary = cv.adaptiveThreshold(gray_blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                              cv.THRESH_BINARY_INV, 11, 5)

# 3. 모폴로지 (자잘한 노이즈 제거 및 건물 덩어리 합치기)
# 커널 크기를 키워 작은 구멍(노이즈)을 확실하게 메웁니다.
kernel = np.ones((7, 7), np.uint8) 
binary_cleaned = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)

# 4. 컨투어 검출 (RETR_TREE로 계층 구조 파악)
contours, hierarchy = cv.findContours(binary_cleaned, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

result = img.copy()
h, w = img.shape[:2] # 이미지 전체 크기

if hierarchy is not None:
    hierarchy = hierarchy[0]
    for i, cnt in enumerate(contours):
        area = cv.contourArea(cnt)
        
        # [핵심 1] 사진 전체 테두리 무시하기
        if area > (w * h * 0.95):
            continue
            
        # [핵심 2] 면적 필터링 강화
        if area > 10000: # 1. ✅ 큰 덩어리 (건물 윤곽) -> 초록색
            parent = hierarchy[i][3]
            if parent == -1: # 최상위 부모만 초록색으로!
                cv.drawContours(result, [cnt], -1, (0, 255, 0), 3) # 굵게
        elif 1000 < area < 8000: # 2. ✅ 중간 덩어리 (창문) -> 파란색
            # 너무 작은 건 무시하고, 창문 크기 범위만 파란색으로!
            cv.drawContours(result, [cnt], -1, (255, 0, 0), 1) # 얇게
        else: # 3. ✅ 너무 작은 것들은 무시
            pass

# 5. 결과 확인
cv.imshow('Improved Binary', binary_cleaned) # 건물이 깨끗한 흰색 덩어리인지 확인!
cv.imshow('Final Result', result)
cv.waitKey(0)
cv.destroyAllWindows()