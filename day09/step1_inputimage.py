# 스텝 1 이미지 읽어오기

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
#plt.style.use('dark_background')

img_ori = cv2.imread('1.jpg') # 번호판을 읽어오는 것을 11단계로 진행

height, width, channel = img_ori.shape

plt.figure(figsize=(12, 10))
plt.imshow(img_ori, cmap='gray')
plt.show()

