import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import os

def get_sample(filename):
    """OpenCV 공식 샘플 이미지 자동 다운로드"""
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return filename

# 이미지 로드
img = cv.imread(get_sample('messi5.jpg'))
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
template = gray[80:230, 20:150]

# 6가지 매칭 방법
methods = ['TM_CCOEFF', 'TM_CCOEFF_NORMED', 'TM_CCORR', 'TM_CCORR_NORMED',
           'TM_SQDIFF', 'TM_SQDIFF_NORMED']

results = []
for method_name in methods:
    # 메서드 타입 선택
    method = getattr(cv, method_name)
    
    # Template Matching 실행
    result = cv.matchTemplate(gray, template, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    
    # TM_SQDIFF* 계열은 min_loc이 최적, 나머지는 max_loc
    if 'SQDIFF' in method_name:
        top_left = min_loc
        score = min_val
    else:
        top_left = max_loc
        score = max_val
    
    results.append((method_name, score, top_left))
    
    # 결과 출력
    print(f"{method_name:15} → score={score:.4f}, top_left={top_left}")

# 최고 점수 방법 표시
best_method, best_score, best_loc = max(results, key=lambda x: x[1] if 'SQDIFF' not in x[0] else -x[1])
print(f"\n최고 성능: {best_method} (score={best_score:.4f})")
