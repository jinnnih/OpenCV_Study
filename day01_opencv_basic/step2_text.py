import cv2 as cv
import numpy as np

# 1. 배경이 될 사진 읽기 (가장 중요!)
# 방금 찍은 사진 파일명을 정확히 적어주세요. 예: 'capture1.jpg'
img = cv.imread("./capture/my_photo.png") 

# 이미지가 잘 불러와졌는지 확인 (예외 처리)
if img is None:
    print("Error: 이미지를 불러올 수 없습니다. 파일명을 확인하세요.")
    exit()

# 2. 이미지 높이(h), 너비(w) 가져오기
h, w = img.shape[:2] # 이미지의 세로, 가로 크기를 숫자로 가져옵니다.

# --- 3. 하단 반투명 배경 바 만들기 (가장 어려운 부분!) ---

# 1) 원본 이미지 복사본 만들기 (overlay)
overlay = img.copy()

# 2) overlay 이미지 하단 80px 영역에 검정 사각형 채우기
# 시작점 (x, y) = (0, h-80) -> 왼쪽 끝, 바닥에서 80px 위
# 끝점 (x, y) = (w, h) -> 오른쪽 끝, 맨 바닥
# 색상 (0, 0, 0) = 검정색
# 두께 -1 = 속을 꽉 채움
cv.rectangle(overlay, (0, h-80), (w, h), (0, 0, 0), -1)

# 3) addWeighted로 원본(img)과 검정 사각형(overlay)을 50:50 합성
# alpha=0.5 (원본 이미지 50% 반영)
# beta=0.5 (검정 사각형 이미지 50% 반영)
# 결과적으로 원본 위에 검정색이 50% 섞여 '반투명'하게 보입니다.
img = cv.addWeighted(overlay, 0.5, img, 0.5, 0)

# --- 4. 텍스트 넣기 ---

# 1) 이름 텍스트 넣기 (putText)
# (이미지, "글자", (시작 x, y), 폰트, 크기, 색상(BGR), 두께)
# 위치: 하단 반투명 바 안쪽 (예: x=20, y=h-45)
# 색상: (255, 255, 255) = 흰색
cv.putText(img, "zeenee", (20, h-45), 
           cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# 2) 소속 텍스트 넣기 (이름 아래에 작은 크기로)
# 위치: 이름 아래 (예: x=20, y=h-15)
# 크기: 0.6 (이름보다 작게)
cv.putText(img, "Mobility Lab.", (20, h-15), 
           cv.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

# 5. 결과 표시 + 키 입력 대기
cv.imshow('My ID Card', img)
cv.waitKey(0) # 아무 키나 누를 때까지 창을 띄워둠

# 6. my_id_card.png로 저장
cv.imwrite('my_id_card.png', img)
print("my_id_card.png로 저장이 완료되었습니다!")

# 7. 창 닫기
cv.destroyAllWindows()