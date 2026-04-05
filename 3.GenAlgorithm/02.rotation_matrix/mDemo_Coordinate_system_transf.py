#!/usr/bin/env python
#########################################################################
# File Name: 3.Rotation_Matrix/mDemo_Coordinate_system_transf.py
# Author: LiHongjin
# mail: 872648180@qq.com
# Created Time: Mon  9 Jun 09:23:03 2025
#########################################################################

# 功能说明
# 1. 定义两个坐标系：
#     * 世界坐标系A：固定坐标系，基向量为
#       X_a=(1,0,0)、
#       Y_a=(0,1,0)、
#       Z_a=(0,0,1)，
#       原点为
#       O_a=(0,0,0)。
#     * 局部坐标系B：可动态变换的坐标系，通过平移、旋转参数控制其位置和姿态。
#
# 2. 可视化效果：
#     * 用红色箭头表示坐标系A的基向量。
#     * 用蓝色箭头表示坐标系B的基向量。
#     * 用绿色虚线表示从坐标系A到坐标系B原点的平移向量。
#
# 3. 交互控制：
#     * 通过滑块调整坐标系B的平移和旋转参数。


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 初始化图形和3D坐标轴
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
plt.subplots_adjust(bottom=0.4)  # 调整布局以放置控件

# 定义世界坐标系A的基向量和原点（红色）
A_origin = np.array([0, 0, 0, 1])  # 齐次坐标
A_x = np.array([1, 0, 0, 1])
A_y = np.array([0, 1, 0, 1])
A_z = np.array([0, 0, 1, 1])

# 定义局部坐标系B的初始基向量和原点（蓝色）
B_origin = np.array([0, 0, 0, 1])
B_x = np.array([1, 0, 0, 1])
B_y = np.array([0, 1, 0, 1])
B_z = np.array([0, 0, 1, 1])

# 变换矩阵函数
def get_translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def get_rotation_matrix(rx, ry, rz):
    # 绕X轴旋转
    Rx = np.array([
        [1, 0, 0, 0],
        [0, np.cos(rx), -np.sin(rx), 0],
        [0, np.sin(rx), np.cos(rx), 0],
        [0, 0, 0, 1]
    ])
    # 绕Y轴旋转
    Ry = np.array([
        [np.cos(ry), 0, np.sin(ry), 0],
        [0, 1, 0, 0],
        [-np.sin(ry), 0, np.cos(ry), 0],
        [0, 0, 0, 1]
    ])
    # 绕Z轴旋转
    Rz = np.array([
        [np.cos(rz), -np.sin(rz), 0, 0],
        [np.sin(rz), np.cos(rz), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    return Rz @ Ry @ Rx  # 组合旋转

# 更新函数
def update(val):
    ax.cla()
    # 获取滑块值
    tx, ty, tz = slider_tx.val, slider_ty.val, slider_tz.val
    rx, ry, rz = slider_rx.val, slider_ry.val, slider_rz.val

    # 计算坐标系B的变换矩阵（先旋转后平移）
    T = get_translation_matrix(tx, ty, tz)
    R = get_rotation_matrix(rx, ry, rz)
    M = T @ R  # 组合变换

    # 应用变换到坐标系B的基向量和原点
    B_origin_transformed = M @ B_origin
    B_x_transformed = M @ B_x
    B_y_transformed = M @ B_y
    B_z_transformed = M @ B_z

    # 绘制坐标系A（红色）
    ax.quiver(A_origin[0], A_origin[1], A_origin[2],
              A_x[0], A_x[1], A_x[2], color='r', label='A-X', arrow_length_ratio=0.1)
    ax.quiver(A_origin[0], A_origin[1], A_origin[2],
              A_y[0], A_y[1], A_y[2], color='r', label='A-Y', arrow_length_ratio=0.1)
    ax.quiver(A_origin[0], A_origin[1], A_origin[2],
              A_z[0], A_z[1], A_z[2], color='r', label='A-Z', arrow_length_ratio=0.1)

    # 绘制坐标系B（蓝色）
    ax.quiver(B_origin_transformed[0], B_origin_transformed[1], B_origin_transformed[2],
              B_x_transformed[0] - B_origin_transformed[0],
              B_x_transformed[1] - B_origin_transformed[1],
              B_x_transformed[2] - B_origin_transformed[2],
              color='b', label='B-X', arrow_length_ratio=0.1)
    ax.quiver(B_origin_transformed[0], B_origin_transformed[1], B_origin_transformed[2],
              B_y_transformed[0] - B_origin_transformed[0],
              B_y_transformed[1] - B_origin_transformed[1],
              B_y_transformed[2] - B_origin_transformed[2],
              color='b', label='B-Y', arrow_length_ratio=0.1)
    ax.quiver(B_origin_transformed[0], B_origin_transformed[1], B_origin_transformed[2],
              B_z_transformed[0] - B_origin_transformed[0],
              B_z_transformed[1] - B_origin_transformed[1],
              B_z_transformed[2] - B_origin_transformed[2],
              color='b', label='B-Z', arrow_length_ratio=0.1)

    # 绘制从A到B的平移向量（绿色虚线）
    ax.plot([A_origin[0], B_origin_transformed[0]],
            [A_origin[1], B_origin_transformed[1]],
            [A_origin[2], B_origin_transformed[2]],
            'g--', label='Translation')

    # 设置坐标轴范围和标签
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

# 创建滑块控件
ax_tx = plt.axes([0.1, 0.30, 0.65, 0.03])
slider_tx = Slider(ax_tx, 'Translate X', -2, 2, valinit=0)
ax_ty = plt.axes([0.1, 0.25, 0.65, 0.03])
slider_ty = Slider(ax_ty, 'Translate Y', -2, 2, valinit=0)
ax_tz = plt.axes([0.1, 0.20, 0.65, 0.03])
slider_tz = Slider(ax_tz, 'Translate Z', -2, 2, valinit=0)

ax_rx = plt.axes([0.1, 0.15, 0.65, 0.03])
slider_rx = Slider(ax_rx, 'Rotate X (rad)', -np.pi, np.pi, valinit=0)
ax_ry = plt.axes([0.1, 0.10, 0.65, 0.03])
slider_ry = Slider(ax_ry, 'Rotate Y (rad)', -np.pi, np.pi, valinit=0)
ax_rz = plt.axes([0.1, 0.05, 0.65, 0.03])
slider_rz = Slider(ax_rz, 'Rotate Z (rad)', -np.pi, np.pi, valinit=0)

# 绑定滑块事件
for slider in [slider_tx, slider_ty, slider_tz, slider_rx, slider_ry, slider_rz]:
    slider.on_changed(update)

update(None)  # 初始绘制
plt.show()
