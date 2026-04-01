import cv2 as cv
import numpy as np

# 1. 이미지 로드 (경로와 파일명 확인 필수!)
img = cv.imread('./img/house.jpg') 
if img is None:
    print("에러: 파일을 찾을 수 없습니다. 경로를 확인하세요.")
    exit()

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 2. 전처리 (노이즈 제거 및 이진화)
# 블러로 자잘한 질감을 뭉갭니다.
gray_blur = cv.GaussianBlur(gray, (7, 7), 0)

# 적응형 이진화: 배경이 밝으므로 INV를 사용하여 물체를 흰색으로 만듭니다.
binary = cv.adaptiveThreshold(gray_blur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                              cv.THRESH_BINARY_INV, 11, 5)

# 모폴로지: 끊어진 선을 잇고 작은 구멍을 메웁니다.
kernel = np.ones((7, 7), np.uint8) 
binary_cleaned = cv.morphologyEx(binary, cv.MORPH_CLOSE, kernel)

# 3. 컨투어 검출 (계층 구조 RETR_TREE 사용)
contours, hierarchy = cv.findContours(binary_cleaned, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# 4. 그리기 및 카운팅 변수 초기화
result = img.copy()
h, w = img.shape[:2]

green_count = 0  # 건물 윤곽 (초록색)
blue_count = 0   # 창문 등 (파란색)
noise_count = 0  # 제외된 노이즈

if hierarchy is not None:
    hierarchy = hierarchy[0]
    for i, cnt in enumerate(contours):
        area = cv.contourArea(cnt)
        
        # [필터 1] 사진 전체 테두리 무시 (이미지 면적의 95% 이상일 때)
        if area > (w * h * 0.95):
            continue
            
        # [필터 2] 면적에 따른 분류 로직
        if area > 10000: # 🟢 큰 객체: 건물 윤곽 후보
            parent = hierarchy[i][3]
            # 부모가 없는 최상위 객체만 건물 윤곽으로 인정
            if parent == -1: 
                green_count += 1
                cv.drawContours(result, [cnt], -1, (0, 255, 0), 3) # 초록색 굵게
            else:
                # 큰 면적이지만 부모가 있다면(건물 안의 큰 파트) 파란색 처리
                blue_count += 1
                cv.drawContours(result, [cnt], -1, (255, 0, 0), 1)

        elif 1000 < area <= 10000: # 🔵 중간 객체: 창문 등
            blue_count += 1
            cv.drawContours(result, [cnt], -1, (255, 0, 0), 1) # 파란색 얇게

        else: # ❌ 작은 객체: 노이즈
            noise_count += 1

# 5. 결과 출력 (해답 확인용)
print("="*40)
print(f"🏠 필터링된 건물 윤곽(초록색): {green_count}개")
print(f"🪟 필터링된 창문/기타(파란색): {blue_count}개")
print(f"🧹 제외된 노이즈 개수: {noise_count}개")
print("="*40)

# 6. 화면 표시
cv.imshow('Binary Cleaned', binary_cleaned)
cv.imshow('Final Assignment Result', result)

cv.waitKey(0)
cv.destroyAllWindows()