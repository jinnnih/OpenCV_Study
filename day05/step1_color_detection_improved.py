# 라이브러리 import
import cv2 as cv
import numpy as np

# 웹캠을 열기
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다")
    exit()

# 감지할 색상의 HSV 범위 설정
def detect_color(frame, lower, upper):
    # 1. BGR -> HSV 색공간으로 변환
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower, upper)
    
    # 2. 지정한 범위의 마스크 생성 (특정 색상만 추출)
    # lower_blue= np.array([18, 65, 130])
    # upper_blue = np.array([65, 255, 255])
    # mask = cv.inRange(hsv, lower_blue, upper_blue)

    # 모폴로지 적용
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    
    # 3. 마스크에서 흰 픽셀(색상 감지 부분)의 개수를 계산
    pixel_count = cv.countNonZero(mask)

    # 4. 임계값보다 면적이 크면 True(감지), 아니면 False(감지x) 반환 
    if pixel_count > 500: 
        return True, pixel_count, mask
    else: return False, pixel_count, mask

ret, frame = cap.read()
if not ret:
    print("❌ 프레임을 읽을 수 없습니다")
    cap.release()
    exit()

# 트랙바 
def nothing(x):
    pass
 
cv.namedWindow('settings')
 
# create trackbars for color change
cv.createTrackbar('H_min','settings',29,179,nothing)
cv.createTrackbar('H_max','settings',179,179,nothing)
cv.createTrackbar('S_min','settings',179,255,nothing)
cv.createTrackbar('S_max','settings',255,255,nothing)
cv.createTrackbar('V_min','settings',68,255,nothing)
cv.createTrackbar('V_max','settings',255,255,nothing)
 
# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv.createTrackbar(switch, 'settings',0,1,nothing)

# roi 영역지정 (화면의 세로 200~480, 가로 100~500 영역만 사용)
roi_y1, roi_y2 = 200, 480
roi_x1, roi_x2 = 100, 500

# 반복:
while(1):
    # 웹캠에서 프레임 읽기
    ret, frame = cap.read()
    if not ret: break

    # ROI 추출 (슬라이싱)
    roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]

    # 트랙바 불러오기
    h_min = cv.getTrackbarPos('H_min', 'settings')
    h_max = cv.getTrackbarPos('H_max', 'settings')
    s_min = cv.getTrackbarPos('S_min', 'settings')
    s_max = cv.getTrackbarPos('S_max', 'settings')
    v_min = cv.getTrackbarPos('V_min', 'settings')
    v_max = cv.getTrackbarPos('V_max', 'settings')

    lower_color = np.array([h_min, s_min, v_min])
    upper_color = np.array([h_max, s_max, v_max])

    # 함수 호출
    is_detected, area, mask = detect_color(roi, lower_color, upper_color)

    # 결과 로직처리
    if is_detected:
        print(f"✅ DETECTED! 면적: {area}")
        status_text = f"DETECTED ({area})"
        color = (0, 255, 0) # 초록색
    else:
        print(f"❌ NOT DETECTED. 면적: {area}")
        status_text = "NOT DETECTED"
        color = (0, 0, 255) # 빨간색

    # 결과 표시
    cv.rectangle(frame, (100, 100), (500, 400), (255, 0, 0), 2) # 파란색 사각형

    # 상태를 터미널과 화면에 표시
    cv.putText(frame, status_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('roi', roi)

    #   'q' 키 입력 시 루프 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    

# 리소스 해제 
cap.release()

cv.destroyAllWindows()