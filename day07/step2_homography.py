import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# ========== Step 1: 이미지 로드 (로컬 파일) ==========
# img1: 찾고자 하는 대상 (책 표지 캡처본)
# img2: 대상이 포함된 실제 촬영 사진
img1 = cv.imread('book.jpg', cv.IMREAD_GRAYSCALE)
img2 = cv.imread('book_pic.png', cv.IMREAD_GRAYSCALE)

if img1 is None or img2 is None:
    print("Error: 이미지를 불러올 수 없습니다. 파일명과 경로를 확인하세요.")
    exit()

# ========== Step 2: SIFT 특징점 검출 및 디스크립터 계산 ==========
sift = cv.SIFT_create()

kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

print(f"Keypoints - Book: {len(kp1)}, Scene: {len(kp2)}")

# ========== Step 3: FLANN 매칭기 설정 및 매칭 (k=2) ==========
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

# ========== Step 4: Lowe's Ratio Test (비율 테스트) ==========
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

print(f"Good Matches after Ratio Test: {len(good_matches)}")

# ========== Step 5: 호모그래피 계산 및 객체 위치 추정 ==========
MIN_MATCH_COUNT = 10  # 최소 매칭 개수 기준

if len(good_matches) >= MIN_MATCH_COUNT:
    # 1) 매칭된 점들의 좌표 추출
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # 2) RANSAC을 이용한 호모그래피 행렬 계산
    M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

    if M is not None:
        # 3) 원본 이미지(img1)의 네 모서리 좌표 정의
        h, w = img1.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        
        # 4) 호모그래피 행렬을 이용한 좌표 변환 (투영)
        dst = cv.perspectiveTransform(pts, M)

        # 5) 촬영 사진(img2) 위에 바운딩 박스 그리기
        # 시각화를 위해 그레이스케일을 컬러로 변환
        img2_color = cv.cvtColor(img2, cv.COLOR_GRAY2BGR)
        img2_rect = cv.polylines(img2_color, [np.int32(dst)], True, (0, 255, 0), 10, cv.LINE_AA)

        # 6) 결과 출력 (Inlier 매칭 결과 포함)
        matchesMask = mask.ravel().tolist()
        draw_params = dict(matchColor=(0, 255, 0),
                           singlePointColor=None,
                           matchesMask=matchesMask, # RANSAC 인라이어만 표시
                           flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        result_img = cv.drawMatches(img1, kp1, img2_rect, kp2, good_matches, None, **draw_params)

        # Matplotlib 시각화
        plt.figure(figsize=(20, 10))
        plt.imshow(cv.cvtColor(result_img, cv.COLOR_BGR2RGB))
        plt.title(f'Detected Book with {sum(matchesMask)} Inliers')
        plt.axis('off')
        plt.show()

        print(f"Success: {sum(matchesMask)}개의 인라이어를 찾아 객체를 검출했습니다.")
    else:
        print("Fail: 호모그래피 행렬 계산에 실패했습니다.")
else:
    print(f"Fail: 매칭점이 부족합니다. ({len(good_matches)}/{MIN_MATCH_COUNT})")