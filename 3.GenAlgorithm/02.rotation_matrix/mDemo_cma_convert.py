#!/usr/bin/env python
#########################################################################
# File Name: mDemo_cma_convert.py
# Author: LiHongjin
# mail: 872648180@qq.com
# Created Time: Mon  2 Sep 09:00:27 2024
#########################################################################

import numpy as np

def world_to_camera(point_world, R, t):
    """
    将世界坐标系中的点转换到相机坐标系。
    :param point_world: 世界坐标系中的点，形状为 (3, 1) 或 (3,)
    :param R: 旋转矩阵，形状为 (3, 3)
    :param t: 平移向量，形状为 (3, 1) 或 (3,)
    :return: 相机坐标系中的点，形状为 (3, 1)
    """
    point_world = np.array(point_world).reshape(3, 1)
    t = np.array(t).reshape(3, 1)
    point_camera = R @ point_world + t  # 旋转后平移
    return point_camera

def camera_to_image(point_camera, K):
    """
    将相机坐标系中的点投影到图像坐标系（归一化平面）。
    :param point_camera: 相机坐标系中的点，形状为 (3, 1) 或 (3,)
    :param K: 相机内参矩阵，形状为 (3, 3)
    :return: 图像坐标系中的点（归一化坐标），形状为 (2, 1)
    """
    point_camera = np.array(point_camera).reshape(3, 1)
    point_image_homogeneous = K @ point_camera  # 内参变换
    point_image = point_image_homogeneous[:2] / point_image_homogeneous[2]  # 归一化
    return point_image

def image_to_pixel(point_image):
    """
    将图像坐标系中的点转换到像素坐标系（直接取整）。
    :param point_image: 图像坐标系中的点，形状为 (2, 1) 或 (2,)
    :return: 像素坐标系中的点（整数坐标），形状为 (2,)
    """
    point_pixel = np.round(point_image).astype(int).flatten()
    return point_pixel

def world_to_pixel(point_world, R, t, K):
    """
    完整流程：世界坐标系 → 相机坐标系 → 图像坐标系 → 像素坐标系。
    :param point_world: 世界坐标系中的点，形状为 (3, 1) 或 (3,)
    :param R: 旋转矩阵，形状为 (3, 3)
    :param t: 平移向量，形状为 (3, 1) 或 (3,)
    :param K: 相机内参矩阵，形状为 (3, 3)
    :return: 像素坐标系中的点，形状为 (2,)
    """
    point_camera = world_to_camera(point_world, R, t)
    point_image = camera_to_image(point_camera, K)
    point_pixel = image_to_pixel(point_image)
    return point_pixel

# -------------------- 示例参数 --------------------
# 世界坐标系中的点（3D）
point_world = np.array([1, 0.5, 3])  # X, Y, Z

# 相机外参：旋转矩阵R和平移向量t（假设相机朝向世界坐标系的-Z方向）
R = np.array([[1, 0, 0],
              [0, 1, 0],
              [0, 0, 1]])  # 无旋转
t = np.array([0, 0, 0])    # 无平移

# 相机内参矩阵K（焦距fx=fy=1000，光心在图像中心320x240）
K = np.array([[1000, 0, 320],
              [0, 1000, 240],
              [0, 0, 1]])

# -------------------- 转换流程 --------------------
print("世界坐标系中的点:", point_world)
point_camera = world_to_camera(point_world, R, t)
print("相机坐标系中的点:", point_camera.flatten())
point_image = camera_to_image(point_camera, K)
print("图像坐标系中的点（归一化）:", point_image.flatten())
point_pixel = image_to_pixel(point_image)
print("像素坐标系中的点:", point_pixel)

# 直接调用完整流程
point_pixel_final = world_to_pixel(point_world, R, t, K)
print("完整流程最终像素坐标:", point_pixel_final)
