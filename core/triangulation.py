# -*- coding: utf-8 -*-
# @Time    : 2018/05/18 13:40
# @Author  : Tony Wang

import cv2
import numpy as np


def draw_point(img, p, color):
    cv2.circle(img, (p[0], p[1]), 2, color, cv2.FILLED, cv2.LINE_AA, 0)


def rect_contains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True


def measure_triangle(image, points):
    rect = (0, 0, image.shape[1], image.shape[0])
    sub_div = cv2.Subdiv2D(rect)

    for p in points:
        sub_div.insert(p)

    triangle_list = sub_div.getTriangleList()

    triangle = []
    pt = []

    for t in triangle_list:
        pt.append((t[0], t[1]))
        pt.append((t[2], t[3]))
        pt.append((t[4], t[5]))

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if rect_contains(rect, pt1) and rect_contains(rect, pt2) and rect_contains(rect, pt3):
            ind = []
            for j in range(0, 3):
                for k in range(0, len(points)):
                    if abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0:
                        ind.append(k)
            if len(ind) == 3:
                triangle.append((ind[0], ind[1], ind[2]))

        pt = []

    return triangle


def morph_triangle(src, dst, img, t_src, t_dst, t, alpha):
    r1 = cv2.boundingRect(np.float32([t_src]))
    r2 = cv2.boundingRect(np.float32([t_dst]))
    r = cv2.boundingRect(np.float32([t]))

    t1_rect = []
    t2_rect = []
    t_rect = []

    for i in range(0, 3):
        t_rect.append(((t[i][0] - r[0]), (t[i][1] - r[1])))
        t1_rect.append(((t_src[i][0] - r1[0]), (t_src[i][1] - r1[1])))
        t2_rect.append(((t_dst[i][0] - r2[0]), (t_dst[i][1] - r2[1])))

    mask = np.zeros((r[3], r[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t_rect), (1.0, 1.0, 1.0), 16, 0)

    img1_rect = src[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2_rect = dst[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])

    warp_img1 = affine_transform(img1_rect, t1_rect, t_rect, size)
    warp_img2 = affine_transform(img2_rect, t2_rect, t_rect, size)

    img_rect = (1.0 - alpha) * warp_img1 + alpha * warp_img2

    img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] = img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] * (1 - mask) + img_rect * mask


def affine_triangle(src, dst, t_src, t_dst):
    r1 = cv2.boundingRect(np.float32([t_src]))
    r2 = cv2.boundingRect(np.float32([t_dst]))

    t1_rect = []
    t2_rect = []
    t2_rect_int = []

    for i in range(0, 3):
        t1_rect.append((t_src[i][0] - r1[0], t_src[i][1] - r1[1]))
        t2_rect.append((t_dst[i][0] - r2[0], t_dst[i][1] - r2[1]))
        t2_rect_int.append((t_dst[i][0] - r2[0], t_dst[i][1] - r2[1]))

    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2_rect_int), (1.0, 1.0, 1.0), 16, 0)

    img1_rect = src[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]

    size = (r2[2], r2[3])

    img2_rect = affine_transform(img1_rect, t1_rect, t2_rect, size)
    img2_rect = img2_rect * mask

    dst[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = dst[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] * (
        (1.0, 1.0, 1.0) - mask)

    dst[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = dst[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] + img2_rect


def affine_transform(src, src_tri, dst_tri, size):
    warp_mat = cv2.getAffineTransform(np.float32(src_tri), np.float32(dst_tri))

    dst = cv2.warpAffine(src, warp_mat, (size[0], size[1]),
                         None,
                         flags=cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_REFLECT_101)

    return dst
