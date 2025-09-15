#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cv2


def calculate_brightness(img_path, count_percent):
    img = cv2.imread(img_path)
    # LAB空间转换，L表示亮度，完全黑暗是L=0，否则为255
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    # 将L缩放成 0-10
    l = l * (10 / 255)
    y, x, z = img.shape
    maxval = []
    # 选区划分
    count_percent = count_percent / 100
    row_percent = int(count_percent * x)
    column_percent = int(count_percent * y)
    for i in range(1, x - 1):
        if i % row_percent == 0:
            for j in range(1, y - 1):
                if j % column_percent == 0:
                    img_segment = l[i:i + 3, j:j + 3]
                    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(img_segment)
                    maxval.append(maxVal)
    lenmaxVal = 0
    for i, val in enumerate(maxval):
        if val == 0:
            lenmaxVal += 1
    lenmaxVal = len(maxval) - lenmaxVal
    if lenmaxVal > 0:
        avg_maxval = round(sum(maxval) / lenmaxVal)
    else:
        avg_maxval = 0
    print('平均亮度: {}'.format(avg_maxval))


calculate_brightness(r'D:\Desktop\AppleVision\Color\23.jpg',20)
