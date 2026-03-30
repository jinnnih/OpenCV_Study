import cv2 as cv
import numpy as np

# 1. 이전 단계에서 만든 ID 카드 읽기
img = cv.imread('my_id_card.png')
if img is None:
    print("이미지를 찾을 수 없습니다. step2를 먼저 실행하세요.")
    exit()

# 2. 원본 복사본 만들기 (드래그 중 지우기 용도)
img_original = img.copy()

# 3. 전역 변수 설정
ix, iy = -1, -1
drawing = False

# 4. 마우스 콜백 함수 정의
def draw_face_rect(event, x, y, flags, param):
    global ix, iy, drawing, img

    # 마우스 왼쪽 버튼을 눌렀을 때 (시작)
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    # 마우스가 움직일 때 (드래그 중)
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            # [중요] 이전 사각형이 그려진 이미지를 원본으로 덮어씌워 지웁니다.
            img[:] = img_original[:]
            # 현재 마우스 위치까지 실시간 사각형 그리기
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

    # 마우스 왼쪽 버튼을 뗐을 때 (끝)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        # 최종 사각형 고정
        cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        # 사각형 위에 "FACE" 텍스트 추가 (조금 위에 표시되도록 y값 조절)
        cv.putText(img, "FACE", (ix, iy - 10), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# 5. 창 생성 및 마우스 콜백 등록
cv.namedWindow('Face Selection')
cv.setMouseCallback('Face Selection', draw_face_rect)

print("마우스로 얼굴을 드래그하세요. 's'를 누르면 저장, 'q'는 종료합니다.")

# 6. 무한 루프 (화면 갱신)
while True:
    cv.imshow('Face Selection', img)
    key = cv.waitKey(1) & 0xFF
    
    # 's' 키를 누르면 저장 후 종료
    if key == ord('s'):
        cv.imwrite('my_id_card_final.png', img)
        print("최종본(my_id_card_final.png)이 저장되었습니다!")
        break
    # 'q' 키를 누르면 그냥 종료
    elif key == ord('q'):
        break

cv.destroyAllWindows()