import numpy as np
import cv2 as cv
 
cap = cv.VideoCapture(0)
 
# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 20.0, (640,  480))

cnt = 1

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame = cv.flip(frame, -1)
 
    # 1. 컬러 변환 (예: 회색조)
    display_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    cv.imshow('frame', frame) # 변환된 화면 표시
    
    key = cv.waitKey(1)
    
    # 2. 'q' 누르면 종료
    if key == ord('q'):
        break
    
    # 3. 'c' 누르면 현재 화면 저장 (캡처)
    elif key == ord('c'):
        cv.imwrite(f"./capture/my_photo{cnt}.png", display_frame)
        print("사진이 저장되었습니다!")
        cnt = cnt + 1
 
# Release everything if job is finished
cap.release()
out.release()
cv.destroyAllWindows()