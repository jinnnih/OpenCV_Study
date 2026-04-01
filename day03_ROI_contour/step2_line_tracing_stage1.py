import cv2 as cv
import numpy as np

# 1. 웹캠 연결 (0번은 보통 노트북 내장 캠)
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("웹캠을 열 수 없습니다")
    exit()

# 창 크기 설정
cv.namedWindow('Line Tracing Stage 1', cv.WINDOW_NORMAL)

while True:
    # 2. 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        break

    # [중요] 영상이 너무 크면 처리가 느리므로 크기를 줄이기도 합니다.
    # frame = cv.resize(frame, (640, 480))

    # 3. 그레이스케일 변환 (색상 정보 제거)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # 4. 이진화 (Otsu 알고리즘: 주변 밝기에 따라 최적의 문턱값을 스스로 찾음)
    # 배경이 밝고 물체가 어두우면 THRESH_BINARY_INV를 써야 할 수도 있습니다.
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # 5. 컨투어 검출
    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # 6. 가장 큰 컨투어(물체) 찾기 (노이즈 방지)
    largest_cnt = None
    max_area = 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > max_area:
            max_area = area
            largest_cnt = cnt

    # 7. 중심좌표 계산 (모멘트 활용)
    if largest_cnt is not None and max_area > 500: # 너무 작은 먼지는 무시
        M = cv.moments(largest_cnt)
        
        # 분모가 0이 되는 것을 방지 (m00은 면적임)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # 결과 시각화
            # 외곽선 그리기 (초록색)
            cv.drawContours(frame, [largest_cnt], -1, (0, 255, 0), 2)
            # 중심점 그리기 (빨간색 점)
            cv.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
            # 좌표 텍스트 표시
            cv.putText(frame, f'Center: ({cx}, {cy})', (20, 50),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # 8. 화면 표시 (이진화 영상과 원본 영상을 가로로 붙여서 비교)
    # binary는 1채널이므로 3채널로 바꿔야 BGR 원본과 붙일 수 있습니다.
    binary_bgr = cv.cvtColor(binary, cv.COLOR_GRAY2BGR)
    result = np.hstack([binary_bgr, frame])
    
    cv.imshow('Line Tracing Stage 1', result)

    # 'q' 키를 누르면 종료
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 9. 정리
cap.release()
cv.destroyAllWindows()