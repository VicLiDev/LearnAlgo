#!/usr/bin/env python
#########################################################################
# File Name: mDemo3D.py
# Author: LiHongjin
# mail: 872648180@qq.com
# Created Time: Mon 26 Aug 20:09:26 2024
#########################################################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# 创建滑杆
ax_slider_x = plt.axes([0.1, 0.3, 0.8, 0.03])  # 滑杆位置 [left, bottom, width, height]
slider_x = Slider(ax_slider_x, 'r_x', - 2 * np.pi, 2 * np.pi, valinit=0)
ax_slider_y = plt.axes([0.1, 0.2, 0.8, 0.03])  # 滑杆位置 [left, bottom, width, height]
slider_y = Slider(ax_slider_y, 'r_y', - 2 * np.pi, 2 * np.pi, valinit=0)
ax_slider_z = plt.axes([0.1, 0.1, 0.8, 0.03])  # 滑杆位置 [left, bottom, width, height]
slider_z = Slider(ax_slider_z, 'r_z', - 2 * np.pi, 2 * np.pi, valinit=0)

def rotition_x(val):
    # 旋转角度
    theta = val

    # Create vector
    org_beg = np.array([0, 0, 0])
    org_end = np.array([1, 1, 1])
    dst_beg = np.array([0, 0, 0])
    dst_end = np.array([1, 1, 1])

    # 旋转矩阵
    R_x = np.array([[1,             0,              0],
                    [0, np.cos(theta), -np.sin(theta)],
                    [0, np.sin(theta), np.cos(theta)]])

    dst_end = np.dot(R_x, org_end)

    # fig.clf() #清除整个图形
    ax.cla() #清除当前轴
    # Add the vector to the plot
    # Make the direction data for the arrows
    # normallize: 归一化，False可以让变量保持正常大小
    ax.quiver(org_beg[0], org_beg[1], org_beg[2], org_end[0], org_end[1], org_end[2],
              normalize=False, arrow_length_ratio=0.1)
    ax.quiver(dst_beg[0], dst_beg[1], dst_beg[2], dst_end[0], dst_end[1], dst_end[2],
              normalize=False, arrow_length_ratio=0.1)

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    # ax.relim()  # 重新计算轴限制
    ax.autoscale_view()  # 自动调整视图
    fig.canvas.draw_idle()  # 安排重绘，空闲时重绘
    fig.canvas.draw()  # 安排重绘

def rotition_y(val):
    # 旋转角度
    theta = val

    # Create vector
    org_beg = np.array([0, 0, 0])
    org_end = np.array([1, 1, 1])
    dst_beg = np.array([0, 0, 0])
    dst_end = np.array([1, 1, 1])

    # 旋转矩阵
    R_y = np.array([[np.cos(theta), 0, -np.sin(theta)],
                    [0,             1,              0],
                    [np.sin(theta), 0, np.cos(theta)]])

    dst_end = np.dot(R_y, org_end)

    # fig.clf() #清除整个图形
    ax.cla() #清除当前轴
    # Add the vector to the plot
    # Make the direction data for the arrows
    # normallize: 归一化，False可以让变量保持正常大小
    ax.quiver(org_beg[0], org_beg[1], org_beg[2], org_end[0], org_end[1], org_end[2],
              normalize=False, arrow_length_ratio=0.1)
    ax.quiver(dst_beg[0], dst_beg[1], dst_beg[2], dst_end[0], dst_end[1], dst_end[2],
              normalize=False, arrow_length_ratio=0.1)

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    # ax.relim()  # 重新计算轴限制
    ax.autoscale_view()  # 自动调整视图
    fig.canvas.draw_idle()  # 安排重绘，空闲时重绘
    fig.canvas.draw()  # 安排重绘

def rotition_z(val):
    # 旋转角度
    theta = val

    # Create vector
    org_beg = np.array([0, 0, 0])
    org_end = np.array([1, 1, 1])
    dst_beg = np.array([0, 0, 0])
    dst_end = np.array([1, 1, 1])

    # 旋转矩阵
    R_z = np.array([[np.cos(theta), -np.sin(theta), 0],
                    [np.sin(theta), np.cos(theta),  0],
                    [0,             0,              1]])

    dst_end = np.dot(R_z, org_end)

    # fig.clf() #清除整个图形
    ax.cla() #清除当前轴
    # Add the vector to the plot
    # Make the direction data for the arrows
    # normallize: 归一化，False可以让变量保持正常大小
    ax.quiver(org_beg[0], org_beg[1], org_beg[2], org_end[0], org_end[1], org_end[2],
              normalize=False, arrow_length_ratio=0.1)
    ax.quiver(dst_beg[0], dst_beg[1], dst_beg[2], dst_end[0], dst_end[1], dst_end[2],
              normalize=False, arrow_length_ratio=0.1)

    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    # ax.relim()  # 重新计算轴限制
    ax.autoscale_view()  # 自动调整视图
    fig.canvas.draw_idle()  # 安排重绘，空闲时重绘
    fig.canvas.draw()  # 安排重绘

rotition_x(np.pi / 4)

# 连接滑杆和更新函数
slider_x.on_changed(rotition_x)
slider_y.on_changed(rotition_y)
slider_z.on_changed(rotition_z)

# 设置标签
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
