#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import cv2
import numpy as np


class matchers:
    def __init__(self):
        self.surf = cv2.SIFT_create()
        index_params = dict(algorithm=0, trees=5)
        search_params = dict(checks=50)
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)

    def match(self, i1, i2, direction=None):
        imageSet1 = self.getSURFFeatures(i1)
        imageSet2 = self.getSURFFeatures(i2)
        print("Direction : ", direction)
        matches = self.flann.knnMatch(
            imageSet2['des'],
            imageSet1['des'],
            k=2
        )
        good = []
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:
                good.append((m.trainIdx, m.queryIdx))
        if len(good) > 4:
            pointsCurrent = imageSet2['kp']
            pointsPrevious = imageSet1['kp']
            matchedPointsCurrent = np.float32(
                [pointsCurrent[i].pt for (__, i) in good]
            )
            matchedPointsPrev = np.float32(
                [pointsPrevious[i].pt for (i, __) in good]
            )
            H, s = cv2.findHomography(matchedPointsCurrent, matchedPointsPrev, cv2.RANSAC, 4)
            return H
        return None

    def getSURFFeatures(self, im):
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        kp, des = self.surf.detectAndCompute(gray, None)
        return {'kp': kp, 'des': des}


class Stitch:
    def __init__(self, args):
        self.path = args
        filenames = sorted([os.path.join(self.path, each) for each in os.listdir(self.path)])
        self.images = [cv2.resize(cv2.imread(each), None, fx=0.4, fy=0.4) for each in filenames]
        self.count = len(self.images)
        self.left_list, self.right_list, self.center_im = [], [], None
        self.matcher_obj = matchers()
        self.prepare_lists()

    def prepare_lists(self):
        self.centerIdx = self.count / 2
        self.center_im = self.images[int(self.centerIdx)]
        for i in range(self.count):
            if (i <= self.centerIdx):
                self.left_list.append(self.images[i])
            else:
                self.right_list.append(self.images[i])

    def leftshift(self):
        a = self.left_list[0]
        for b in self.left_list[1:]:
            H = self.matcher_obj.match(a, b, 'left')
            xh = np.linalg.inv(H)
            f1 = np.dot(xh, np.array([0, 0, 1]))
            f1 = f1 / f1[-1]
            xh[0][-1] += abs(f1[0])
            xh[1][-1] += abs(f1[1])
            ds = np.dot(xh, np.array([a.shape[1], a.shape[0], 1]))
            offsety = abs(int(f1[1]))
            offsetx = abs(int(f1[0]))
            dsize = (int(ds[0]) + offsetx, int(ds[1]) + offsety)
            tmp = cv2.warpPerspective(a, xh, dsize)
            kk = tmp[offsety:b.shape[0] + offsety, offsetx:b.shape[1] + offsetx].shape
            if kk == b.shape:
                tmp[offsety:b.shape[0] + offsety, offsetx:b.shape[1] + offsetx] = b
            elif kk[0] < b.shape[0] and kk[1] < b.shape[1]:
                tmp[offsety:b.shape[0] + offsety, offsetx:b.shape[1] + offsetx] = b[:kk[0], :kk[1]]
            elif kk[1] < b.shape[1]:
                tmp[offsety:b.shape[0] + offsety, offsetx:b.shape[1] + offsetx] = b[:, :kk[1]]
            elif kk[0] < b.shape[0]:
                tmp[offsety:b.shape[0] + offsety, offsetx:b.shape[1] + offsetx] = b[:kk[0], :]
            a = tmp
        self.leftImage = tmp

    def rightshift(self):
        for each in self.right_list:
            H = self.matcher_obj.match(self.leftImage, each, 'right')
            txyz = np.dot(H, np.array([each.shape[1], each.shape[0], 1]))
            txyz = txyz / txyz[-1]
            dsize = (int(txyz[0]) + self.leftImage.shape[1], int(txyz[1]) + self.leftImage.shape[0])
            tmp = cv2.warpPerspective(each, H, dsize)
            tmp = self.mix_and_match(self.leftImage, tmp)
            self.leftImage = tmp

    def mix_and_match(self, leftImage, warpedImage):
        i1y, i1x = leftImage.shape[:2]
        for i in range(0, i1x):
            for j in range(0, i1y):
                try:
                    if (np.array_equal(leftImage[j, i], np.array([0, 0, 0])) and np.array_equal(warpedImage[j, i],
                                                                                                np.array([0, 0, 0]))):
                        warpedImage[j, i] = [0, 0, 0]
                    else:
                        if (np.array_equal(warpedImage[j, i], [0, 0, 0])):
                            warpedImage[j, i] = leftImage[j, i]
                        else:
                            if not np.array_equal(leftImage[j, i], [0, 0, 0]):
                                bl, gl, rl = leftImage[j, i]
                                warpedImage[j, i] = [bl, gl, rl]
                except:
                    pass
        return warpedImage


if __name__ == '__main__':
    s = Stitch('Assets/set')
    s.leftshift()
    s.rightshift()
    cv2.imshow("Assea", s.leftImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
