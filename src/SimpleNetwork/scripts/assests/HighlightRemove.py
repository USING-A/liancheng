#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cv2
import numpy as np
import SimpleITK as sitk


# 盲解反卷积
def tikhonov_deblur(image, r, sz):
    kern = np.zeros((sz, sz), np.uint8)
    cv2.circle(kern, (sz, sz), r, 255, -1, cv2.LINE_AA, shift=2)
    kern = np.float32(kern) / 255
    psf = kern.astype(np.uint8)
    tkfilter = sitk.TikhonovDeconvolutionImageFilter()
    tkfilter.SetRegularizationConstant(0.06)
    tkfilter.SetNormalize(True)
    im_res_TK = sitk.GetArrayFromImage(
        tkfilter.Execute(sitk.GetImageFromArray(image[:, :, 0]), sitk.GetImageFromArray(psf)))
    im_res_TK1 = sitk.GetArrayFromImage(
        tkfilter.Execute(sitk.GetImageFromArray(image[:, :, 1]), sitk.GetImageFromArray(psf)))
    im_res_TK2 = sitk.GetArrayFromImage(
        tkfilter.Execute(sitk.GetImageFromArray(image[:, :, 2]), sitk.GetImageFromArray(psf)))
    repaired_image = image.copy()
    repaired_image[:, :, 0] = im_res_TK
    repaired_image[:, :, 1] = im_res_TK1
    repaired_image[:, :, 2] = im_res_TK2
    return repaired_image


# 直方图均衡化
def histgram(image, flag):
    """
    :param image:
    :param flag: 0表示全局，1表示局部
    :return:
    """
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    if flag == 0:
        equalized_value = cv2.equalizeHist(hsv_image[:, :, 2])
    else:
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(10, 10))
        equalized_value = clahe.apply(hsv_image[:, :, 2])
    equalized_hsv = hsv_image.copy()
    equalized_hsv[:, :, 2] = equalized_value
    equalized_image = cv2.cvtColor(equalized_hsv, cv2.COLOR_HSV2BGR)
    return equalized_image


# 高光消除
def highlight_remove(image):
    # image = histgram(image, 0)
    B = image[:, :, 0] + 1e-8
    G = image[:, :, 1] + 1e-8
    R = image[:, :, 2] + 1e-8
    I_sum = R + G + B
    I_minal = np.minimum(np.minimum(R, G), B)
    I_mean = np.mean(I_minal.flatten())
    I_std = np.std(I_minal.flatten())
    if I_mean > I_std:
        k = 1.35
    else:
        k = 0.6
    T = I_mean + k * I_std
    mask = np.array(np.where(I_minal < T, 255, 0), dtype=np.uint8)
    diffuse = histgram(cv2.bitwise_and(image, image, mask=mask), 1)
    diffuse = cv2.bitwise_and(diffuse, diffuse, mask=mask)
    sigma_r = R / I_sum
    sigma_g = G / I_sum
    sigma_b = B / I_sum
    sigma_minal = np.minimum(np.minimum(sigma_r, sigma_g), sigma_b)
    gama_r = sigma_r - sigma_minal
    gama_g = sigma_g - sigma_minal
    gama_b = sigma_b - sigma_minal
    msf = image.copy()
    msf[:, :, 0] = np.clip(gama_b * I_sum + T, 0, 255)
    msf[:, :, 1] = np.clip(gama_g * I_sum + T, 0, 255)
    msf[:, :, 2] = np.clip(gama_r * I_sum + T, 0, 255)
    specular = cv2.bitwise_and(msf, msf, mask=cv2.bitwise_not(mask))
    before_repair = cv2.inpaint(diffuse + specular, cv2.bitwise_not(mask), 1, cv2.INPAINT_TELEA)
    kernel1 = np.array([[0.073235, 0.176765, 0.073235],
                        [0.176765, 0, 0.176765],
                        [0.073235, 0.176765, 0.073235]], dtype=np.float32)
    kernel2 = np.array([[0.125, 0.125, 0.125],
                        [0.125, 0, 0.125],
                        [0.125, 0.125, 0.125]], dtype=np.float32)
    filtered_image = cv2.filter2D(before_repair, -1, kernel1)
    filtered_image = cv2.filter2D(filtered_image, -1, kernel2)
    after_repair = cv2.bitwise_and(filtered_image, filtered_image, mask=cv2.bitwise_not(mask))
    # gray_image = cv2.cvtColor(after_repair, cv2.COLOR_BGR2GRAY)
    # _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)
    # contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # mask1 = cv2.bitwise_not(mask)
    # for contour in contours:
    #     p = np.zeros_like(after_repair)
    #     cv2.drawContours(p, [contour], -1, 255, -1)
    #     a = np.where(p == 255)[0].reshape(-1, 1)
    #     b = np.where(p == 255)[1].reshape(-1, 1)
    #     coordinate = np.concatenate([a, b], axis=1).tolist()
    #     part1 = np.array([after_repair[x[0]][x[1]] for x in coordinate])
    #     # part2 = np.array([specular[x[0]][x[1]] for x in coordinate])
    #     if not (np.min(part1, axis=1) < 100 and np.max(part1, axis=1) < 200):
    #         for x in coordinate:
    #             mask1[x[0]][x[1]] = 0
    # res = diffuse + cv2.bitwise_and(after_repair, after_repair, mask=mask1)
    res = diffuse + after_repair
    return res


img = cv2.imread('assets/2024_01_26_16_23_29/Color/3.jpg')
# img = cv2.resize(img, None, fx=0.4, fy=0.4)
res = highlight_remove(img)

# 显示拼接后的图像
cv2.imshow('Combined sigmamage', res)
cv2.waitKey(0)
cv2.destroyAllWindows()
