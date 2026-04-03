# 라이브러리 import
import cv2 as cv
import numpy as np

# 웹캠을 열기
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("❌ 웹캠을 열 수 없습니다")
    exit()

# 감지할 색상의 HSV 범위 설정
def detect_color(frame):
    # 1. BGR -> HSV 색공간으로 변환
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # 2. 지정한 범위의 마스크 생성 (특정 색상만 추출)
    lower_blue = np.array([18, 65, 130])
    upper_blue = np.array([65, 255, 255])
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    
    # 3. 마스크에서 흰 픽셀(색상 감지 부분)의 개수를 계산
    pixel_count = cv.countNonZero(mask)

    # 4. 임계값보다 면적이 크면 True(감지), 아니면 False(감지x) 반환 
    if pixel_count > 500: 
        return True, pixel_count
    else: return False, pixel_count

ret, frame = cap.read()
if not ret:
    print("❌ 프레임을 읽을 수 없습니다")
    cap.release()
    exit()


# 반복:
while(1):
    # 웹캠에서 프레임 읽기
    ret, frame = cap.read()
    if not ret: break

    # 함수 호출
    is_detected, area = detect_color(frame)

    # 결과 로직처리
    if is_detected:
        print(f"✅ DETECTED! 면적: {area}")
        status_text = f"DETECTED ({area})"
        color = (0, 255, 0) # 초록색
    else:
        print(f"❌ NOT DETECTED. 면적: {area}")
        status_text = "NOT DETECTED"
        color = (0, 0, 255) # 빨간색

    # 상태를 터미널과 화면에 표시
    cv.putText(frame, status_text, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv.imshow('frame', frame)
    print('frame', frame)

    #   'q' 키 입력 시 루프 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    

# 리소스 해제 
cap.release()

cv.destroyAllWindows() 