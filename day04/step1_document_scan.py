# 마우스와 원근 변환으로 문서 스캔 효과 내기 (perspective_scan.py)

import cv2 as cv
import numpy as np

# ============================================================
# 전역 변수
# ============================================================
win_name = "Document Scanning"
img = None
draw = None
rows, cols = 0, 0
pts_cnt = 0
pts = np.zeros((4, 2), dtype=np.float32)

# ============================================================
# 마우스 콜백 함수
# ============================================================
def onMouse(event, x, y, flags, param):
    """
    마우스로 4개 점을 클릭하면:
    1. 클릭 위치에 초록색 원 표시
    2. 4개 점 수집 후 자동으로 좌상/우상/우하/좌하 판단
    3. 원근 변환 적용
    """
    global pts_cnt, draw, pts, img
    
    if event == cv.EVENT_LBUTTONDOWN:
        # 1️⃣ 클릭한 위치에 원 표시
        cv.circle(draw, (x,y), 10, (0,255,0), -1)
        cv.imshow(win_name, draw)

        # 2️⃣ 좌표 저장
        pts[pts_cnt] = [x,y]
        pts_cnt+=1

        # 3️⃣ 4개 점 수집 완료 → 좌표 정렬 + 변환
        if pts_cnt == 4:

            # 합 계산 (좌상단: 최소, 우하단: 최대)
            sm = pts.sum(axis=1)                 # 4쌍의 좌표 각각 x+y 계산
            diff = np.diff(pts, axis = 1)       # 4쌍의 좌표 각각 x-y 계산
       

            # 차 계산 (우상단: 최소, 좌하단: 최대)
            topLeft = pts[np.argmin(sm)]         # x+y가 가장 값이 좌상단 좌표
            bottomRight = pts[np.argmax(sm)]     # x+y가 가장 큰 값이 우하단 좌표
            topRight = pts[np.argmin(diff)]     # x-y가 가장 작은 것이 우상단 좌표
            bottomLeft = pts[np.argmax(diff)]   # x-y가 가장 큰 값이 좌하단 좌표
      

            # 변환 전 4개 좌표
            pts1 = np.float32([topLeft, topRight, bottomRight , bottomLeft])
   
            # 변환 후 서류 크기 계산
            w1 = abs(bottomRight[0] - bottomLeft[0])    # 상단 좌우 좌표간의 거리
            w2 = abs(topRight[0] - topLeft[0])          # 하당 좌우 좌표간의 거리
            h1 = abs(topRight[1] - bottomRight[1])      # 우측 상하 좌표간의 거리
            h2 = abs(topLeft[1] - bottomLeft[1])        # 좌측 상하 좌표간의 거리
            width = max([w1, w2])                       # 두 좌우 거리간의 최대값이 서류의 폭
            height = max([h1, h2]) 

            # ✅ 1. width와 height를 정수(int)로 변환 (중요!)
            width = int(width)
            height = int(height)

            # ✅ 2. pts2 좌표도 정수화된 width, height 사용
            pts2 = np.float32([[0,0], [width-1,0], 
                               [width-1,height-1], [0,height-1]])
            
            mtrx = cv.getPerspectiveTransform(pts1, pts2)

            # ✅ 3. (width, height) 부분이 정수여야 에러 없이 실행됩니다.
            result = cv.warpPerspective(img, mtrx, (width, height))
            cv.imshow('scanned', result)

            # 4. 결과 저장
            cv.imwrite('scanned_document.png', result) 
            print(f"💾 '{width}x{height}' 크기로 'scanned_document.png' 저장 완료!")

            # 5. 초기화
            pts_cnt = 0
            draw = img.copy() # 초록색 원이 그려진 도화지도 초기화 (선택 사항)


# ============================================================
# 메인 실행
# ============================================================

cap = cv.VideoCapture(0) # 웹캠 연결

if not cap.isOpened():
    print("❌ 카메라를 열 수 없습니다.")
    exit()

print("📸 [Step 1] 웹캠 모드: 'Space' 키를 눌러 문서를 촬영하세요. (종료: 'q')")

while True:
    ret, frame = cap.read()
    if not ret: break
    
    cv.imshow('Webcam View (Press Space)', frame)
    
    key = cv.waitKey(1)
    if key == ord(' '):  # Space 바를 누르면 현재 화면을 고정(캡처)
        img = frame.copy()
        draw = frame.copy()
        print("📸 촬영 성공! 이제 마우스로 네 모서리를 클릭하세요.")
        break
    elif key == ord('q'):
        cap.release()
        cv.destroyAllWindows()
        exit()

cap.release() # 촬영이 끝났으니 캠은 끕니다.
cv.destroyWindow('Webcam View (Press Space)') # 촬영 창 닫기

# [Step 2] 클릭 및 변환 모드
# ✅ [Step 2] 촬영이 끝난 후, 이미지가 존재할 때만 윈도우를 엽니다.
if img is not None:
    cv.imshow(win_name, img) # 이제 img에 사진이 들어있어서 에러가 안 납니다!
    cv.setMouseCallback(win_name, onMouse)
    cv.waitKey(0)
    cv.destroyAllWindows()

# print("📝 사용법:")
# print("1. 이미지 위에 4개 점을 클릭하세요 (좌상단, 우상단, 우하단, 좌하단 순서 무관)")
# print("2. 4번째 점 클릭 후 자동으로 문서 스캔이 실행됩니다.")
# print("3. 'Scanned Document' 윈도우에서 결과를 확인하세요.")
