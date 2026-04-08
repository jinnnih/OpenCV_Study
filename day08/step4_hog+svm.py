import cv2

import numpy as np

# HOG 디스크립터 설정

hog = cv2.HOGDescriptor()

hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# 웹캠 열기

cap = cv2.VideoCapture(0)  # 0 = 기본 웹캠

if not cap.isOpened():

    print("Error: 웹캠을 열 수 없습니다")

    exit()

# 프레임 크기 설정 (처리 속도 향상)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_count = 0

detected_frames = 0

print("="*50)

print("웹캠 보행자 감지 시작")

print("'q' 또는 ESC로 종료")

print("="*50)

while True:

    ret, frame = cap.read()

    if not ret:

        break

    

    frame_count += 1

    

    # ① HOG로 보행자 감지 ---

    detections, weights = hog.detectMultiScale(

        frame,

        winStride=(8, 8),

        padding=(16, 16),

        scale=1.05

    )

    

    # ② 신뢰도 필터링 ---

    CONFIDENCE_THRESHOLD = 0.5

    filtered_detections = [

        (x, y, w, h) for (x, y, w, h), weight in zip(detections, weights)

        if weight > CONFIDENCE_THRESHOLD

    ]

    

    if len(filtered_detections) > 0:

        detected_frames += 1

    

    # ③ 바운딩 박스 그리기 ---

    for (x, y, w, h) in filtered_detections:

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    

    # ④ 정보 표시 ---

    cv2.putText(frame, f"Frame: {frame_count}", (10, 30),

                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.putText(frame, f"Detected: {len(filtered_detections)}", (10, 70),

                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.putText(frame, f"Detection Rate: {detected_frames/max(1, frame_count)*100:.1f}%", (10, 110),

                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 200, 255), 2)

    

    # ⑤ 화면 표시 ---

    cv2.imshow('Webcam - Pedestrian Detection', frame)

    

    # ⑥ 종료 조건 ---

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q') or key == 27:  # 'q' 또는 ESC

        break

cap.release()

cv2.destroyAllWindows()

# 통계 출력

print(f"\n{'='*50}")

print(f"처리 완료")

print(f"{'='*50}")

print(f"총 프레임: {frame_count}개")

print(f"보행자 감지된 프레임: {detected_frames}개")

print(f"감지율: {detected_frames/max(1, frame_count)*100:.1f}%")
