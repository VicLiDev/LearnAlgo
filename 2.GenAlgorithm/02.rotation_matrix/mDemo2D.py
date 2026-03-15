#!/usr/bin/env python
#########################################################################
# File Name: mDemo.py
# Author: LiHongjin
# mail: 872648180@qq.com
# Created Time: Mon 26 Aug 18:09:50 2024
#########################################################################

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)  # 调整图表以留出空间放置滑杆

# 创建滑杆
ax_slider = plt.axes([0.1, 0.1, 0.8, 0.03])  # 滑杆位置 [left, bottom, width, height]
slider = Slider(ax_slider, 'rotition', - 2 * np.pi, 2 * np.pi, valinit=0)

def rotition(val):
    # 旋转角度
    theta = val

    # Create vector
    org_beg = np.array([0, 0])
    org_end = np.array([1, 0])
    dst_beg = np.array([0, 0])
    dst_end = np.array([1, 0])

    # 旋转矩阵，逆时针
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])

    dst_end = np.dot(R, org_end)

    # fig.clf() #清除整个图形
    ax.cla() #清除当前轴
    # Add the vector to the plot
    ax.quiver(org_beg[0], org_beg[1], org_end[0], org_end[1], angles='xy',
              scale_units='xy', scale=1, color='b')
    ax.quiver(dst_beg[0], dst_beg[1], dst_end[0], dst_end[1], angles='xy',
              scale_units='xy', scale=1, color='r')

    # Set the x-limits and y-limits of the plot
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    # ax.relim()  # 重新计算轴限制
    ax.autoscale_view()  # 自动调整视图
    fig.canvas.draw_idle()  # 安排重绘，空闲时重绘
    fig.canvas.draw()  # 安排重绘

rotition(0)

# 连接滑杆和更新函数
slider.on_changed(rotition)

# Show the plot along with the grid
plt.grid()
plt.show()
