import numpy as np
import cv2 as cv
 
def nothing(x):
    pass
 
# Create a black image, a window
# img = np.zeros((300,512,3), np.uint8)
cap = cv.VideoCapture(0)
cv.namedWindow('image')
 
# create trackbars for color change
cv.createTrackbar('H_min','image',0,179,nothing)
cv.createTrackbar('H_max','image',179,179,nothing)
cv.createTrackbar('S_min','image',50,255,nothing)
cv.createTrackbar('S_max','image',255,255,nothing)
cv.createTrackbar('V_min','image',50,255,nothing)
cv.createTrackbar('V_max','image',255,255,nothing)
 
# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv.createTrackbar(switch, 'image',0,1,nothing)
 
while(1):
    # 1. 카메라에서 사진 한 장 찍기
    ret, frame = cap.read()
    if not ret: 
        print(f"사진 촬영 실패: {ret}") 
        break # 사진 못 찍었으면 탈출

    # 2. 트랙바에서 현재 '숫자'들 읽어오기 (이름 주의!)
    h_min = cv.getTrackbarPos('H_min', 'image')
    h_max = cv.getTrackbarPos('H_max', 'image')
    s_min = cv.getTrackbarPos('S_min', 'image')
    s_max = cv.getTrackbarPos('S_max', 'image')
    v_min = cv.getTrackbarPos('V_min', 'image')
    v_max = cv.getTrackbarPos('V_max', 'image')
    s = cv.getTrackbarPos(switch,'image')


    # 3. 색공간 변환 (BGR -> HSV)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # 4. 필터링 (범위 설정)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # 설정한 범위에 드는 부분만 흰색(255), 나머지는 검은색(0)으로 만들기
    mask = cv.inRange(hsv, lower, upper)
   
    # 5. 결과 보여주기
    cv.imshow('image', frame) # 원본
    cv.imshow('mask', mask)   # 마스크 (흑백)

    if cv.waitKey(1) & 0xFF == 27: # ESC 누르면 종료
            break
 
cv.destroyAllWindows()