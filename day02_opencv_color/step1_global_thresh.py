import cv2 as cv  # 이미지 처리 담당 라이브러리 불러오기
import numpy as np  # 수치 계산 담당 라이브러리 불러오기

# img 변수 안에 이진화를 하기 위해 grayscale로 읽게 하기
img = cv.imread('my_id_card.png', cv.IMREAD_GRAYSCALE)
# print(img.shape) # 이미지 잘 읽었는지 확인하기

# 값이 바뀔 때마다 트랙바는 실행할 동작을 묻기 때문에 아무일도 하지 않는 함수 필요
# 트랙바가 작동할 때마다 실행될 '빈 함수'만들기
def nothing(x):
    pass   # 아무것도 하지말고 그냥 넘어가기

# Binary 라는 이름의 window 만들기 # 트랙바를 붙여놓을 창 생성하기
cv.namedWindow('Binary')

# 트랙바 만들기
# 이름: 'threshold', 범위: 0~255, 초기값: 127, 콜백함수: nothing
cv.createTrackbar('threshold', 'Binary', 127, 255, nothing)
# 트랙바 옆에 표시되는 이름 Threshold
# 만들었던 창 이름
# 트랙바를 처음 켰을 때 위치할 초기값 (0~255 중간값)
# 트랙바의 최대값 (밝기 최대)
# 값이 바뀔 때 호출할 함수


# 반전모드 트랙바 (0 or 1) 만들기
cv.createTrackbar('mode', 'Binary', 0, 1, nothing)
# 트랙바 옆에 표시되는 이름 Threshold
# 만들었던 창 이름
# 트랙바를 처음 켰을 때 위치할 초기값 (0~255 중간값)
# 트랙바의 최대값 (밝기 최대)
# 값이 바뀔 때 호출할 함수


# 컴퓨터가 트랙바 움직임에 맞춰서 1초에 수십번씩 확인할 수 있도록 반복문
while True:  # 무한반복
    # 아까 만든 트랙바를 루프 안에서 읽을 수 있게 불러오기, 변수에 저장
    thresh_val = cv.getTrackbarPos('threshold','Binary')
    mode_val = cv.getTrackbarPos('mode','Binary')

    # 읽어온 트랙바의 이진화 연산 실행하기
    # 이미지를 0과 255로 나누기
    # 조건문: mode_val이 0이면 일반 모드, 1이면 INV 모드 사용하기
    # (팁: 'Type' 트랙바가 0이면 일반, 1이면 반전 모드!)    
    if mode_val == 0:
        # cv.threshold(원본, 문턱값, 최대값, 타입)
        ret, thresh_img = cv.threshold(img, thresh_val, 255, cv.THRESH_BINARY)
    else:
        ret, thresh_img = cv.threshold(img, thresh_val, 255, cv.THRESH_BINARY_INV)

    # 두 이미지를 가로로 붙이기 (NumPy의 hstack 사용)
    # [img, thresh_img] 리스트 형태
    combined = np.hstack((img, thresh_img))

    # 화면에 보여주기
    cv.imshow('Binary', combined)
 
    # 'q'키를 누르면 루프 탈출 (waitKey) 무한루프 끊기
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 마무리, 모든창 닫기
cv. destroyAllWindows()