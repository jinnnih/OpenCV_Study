import cv2 as cv
import numpy as np

# 1. 웹캠 연결
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("웹캠을 열 수 없습니다")
    exit()

cv.namedWindow('Line Tracing Stage 2', cv.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 가로 크기를 640으로 고정 (계산의 일관성을 위해)
    frame = cv.resize(frame, (640, 480))
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    # 이진화 (검은 선을 추적한다면 THRESH_BINARY_INV 사용 권장)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # --- [추가] 노이즈 제거: 모폴로지 연산 ---
    # 메디안 필터 (소금-후추 노이즈 제거)
    binary = cv.medianBlur(binary, 5)
    # 모폴로지 열기 (Opening): 작은 흰색 점들을 삭제
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    binary = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)

    contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    largest_cnt = None
    max_area = 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > max_area:
            max_area = area
            largest_cnt = cnt

    if largest_cnt is not None and max_area > 500:
        M = cv.moments(largest_cnt)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # --- [추가] 방향 계산: fitLine ---
            # 최적선 피팅 (직선을 가장 잘 나타내는 벡터 추출)
            vx, vy, x_pos, y_pos = cv.fitLine(largest_cnt, cv.DIST_L2, 0, 0.01, 0.01)
            # 수직(90도) 기준 각도 계산
            angle = np.arctan2(vy, vx) * 180 / np.pi

            # --- [추가] 제어신호 생성: Steering ---
            frame_center_x = frame.shape[1] // 2
            error = cx - frame_center_x
            # 정규화: 중앙이면 0.0, 왼쪽 끝이면 -1.0, 오른쪽 끝이면 1.0
            steer = error / frame_center_x

            # --- 시각화 ---
            cv.drawContours(frame, [largest_cnt], 0, (0, 255, 0), 2)
            cv.circle(frame, (cx, cy), 8, (0, 0, 255), -1)
            
            # 중앙 기준선 그리기 (회색)
            cv.line(frame, (frame_center_x, 0), (frame_center_x, 480), (200, 200, 200), 2)
            
            # [심화] Steer 시각화 (중앙에서 뻗어나가는 막대기)
            bar_end_x = frame_center_x + int(steer * 200)
            color = (255, 0, 0) if steer < 0 else (0, 0, 255) # 왼쪽 파랑, 오른쪽 빨강
            cv.line(frame, (frame_center_x, 240), (bar_end_x, 240), color, 5)

            # 정보 텍스트 표시
            cv.putText(frame, f'Angle: {angle[0]:.1f} deg', (10, 60), 
                       cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv.putText(frame, f'Steer: {steer:.2f}', (10, 90), 
                       cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # 결과 표시
    binary_color = cv.cvtColor(binary, cv.COLOR_GRAY2BGR)
    result = np.hstack([binary_color, frame])
    cv.imshow('Line Tracing Stage 2', result)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()