import cv2
import numpy as np  # 수학 계산을 위해 꼭 필요합니다!
import urllib.request
from sample_download import get_sample

# 1. 이미지 준비
# 인터넷에서 메시와 사람들이 있는 사진을 가져옵니다.
# url = "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/messi5.jpg"
# urllib.request.urlretrieve(url, 'pedestrian.jpg')
img = cv2.imread('test2.jpg')

if img is None:
    print("❌ 이미지 로드 실패!")
    exit()

# 2. HOG 검출기 설정
hog = cv2.HOGDescriptor() # 특징 추출 도구 생성
# OpenCV에서 제공하는 '이미 학습된 보행자 모델'을 가져옵니다.
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# 3. 보행자 검출 실행
# 이미지에서 사람 모양의 특징을 찾아 사각형 좌표(detections)와 확신도(weights)를 반환합니다.
detections, weights = hog.detectMultiScale(
    img,
    winStride=(3, 3),  # 검출 창이 이동하는 간격 (작을수록 정밀하지만 느림)
    padding=(12, 12),  # 이미지 외곽 여백
    scale= 1.4         # 이미지 피라미드 비율 (이미지를 줄여가며 작은 사람도 찾음)
)

# 4. 신뢰도(Weights) 분석
print(f"전체 검출된 개수: {len(detections)}개")
if len(weights) > 0:
    for threshold in [0.3, 0.5, 0.7]:
        count = np.sum(weights > threshold)
        print(f"확신도 {threshold} 이상: {count}명")

# 5. 결과 시각화 (신뢰도 필터링 적용)
CONFIDENCE_THRESHOLD = 0.5  # 0.5보다 확신이 생길 때만 표시
result_img = img.copy()

for (x, y, w, h), weight in zip(detections, weights):
    if weight > CONFIDENCE_THRESHOLD:
        # 사람이라고 판단된 곳에 녹색 사각형 그리기
        cv2.rectangle(result_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # 사각형 위에 확신도 숫자 쓰기
        cv2.putText(result_img, f'{weight:.2f}', (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

# 6. 파라미터 튜닝 테스트 (간략화)
print("\n[파라미터 비교]")
configs = [
    {"name": "Default", "winStride": (3, 8), "scale": 1.05},
    {"name": "Fast", "winStride": (16, 16), "scale": 1.1},
]

for config in configs:
    found, _ = hog.detectMultiScale(img, winStride=config["winStride"], scale=config["scale"])
    print(f"- {config['name']}: {len(found)}명 검출")

# 7. 화면에 출력
cv2.imshow('Pedestrian Detection (HOG)', result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()