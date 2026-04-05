#!/usr/bin/env python
#########################################################################
# File Name: up_down_sample.py
# Author: LiHongjin
# mail: 872648180@qq.com
# Created Time: Wed  4 Sep 12:28:31 2024
#########################################################################

# 代码说明：
# 原始图像：2x2的小图像，用于展示采样效果。
# 上采样部分：
#   最近邻插值 (Upsample Nearest)
#   双线性插值 (Upsample Bilinear)
#   双三次插值 (Upsample Bicubic)
#   拉普拉斯金字塔插值 (Upsample Laplacian)
# 下采样部分：
#   最近邻插值 (Downsample Nearest)
#   双线性插值 (Downsample Bilinear)
#   区域插值 (Downsample Area)
#   高斯金字塔 (Downsample Gaussian)
# 运行效果：
# 该代码运行后，会生成一个包含8个子图的图像，每个子图展示了不同采样算法的效果，便于直观比较。

import numpy as np
import cv2
import matplotlib.pyplot as plt

# 生成一个简单的2x2图像
img = np.array([[0, 255], [255, 0]], dtype=np.uint8)

# 上采样算法
upsampled_nearest = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
upsampled_bilinear = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
upsampled_bicubic = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# 拉普拉斯金字塔上采样
# 1. 先下采样
downsampled = cv2.pyrDown(img)
# 2. 再上采样
upsampled_laplacian = cv2.pyrUp(downsampled)

# 下采样算法
downsampled_nearest = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
downsampled_bilinear = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
downsampled_area = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
downsampled_gaussian = cv2.pyrDown(img)

# 将所有结果绘制到一张图中
fig, axs = plt.subplots(2, 4, figsize=(12, 6))

# 原始图像
axs[0, 0].imshow(img, cmap='gray')
axs[0, 0].set_title('Original Image')
axs[0, 0].axis('off')

# 上采样结果
axs[0, 1].imshow(upsampled_nearest, cmap='gray')
axs[0, 1].set_title('Upsample Nearest')
axs[0, 1].axis('off')

axs[0, 2].imshow(upsampled_bilinear, cmap='gray')
axs[0, 2].set_title('Upsample Bilinear')
axs[0, 2].axis('off')

axs[0, 3].imshow(upsampled_bicubic, cmap='gray')
axs[0, 3].set_title('Upsample Bicubic')
axs[0, 3].axis('off')

# 下采样结果
axs[1, 0].imshow(downsampled_nearest, cmap='gray')
axs[1, 0].set_title('Downsample Nearest')
axs[1, 0].axis('off')

axs[1, 1].imshow(downsampled_bilinear, cmap='gray')
axs[1, 1].set_title('Downsample Bilinear')
axs[1, 1].axis('off')

axs[1, 2].imshow(downsampled_area, cmap='gray')
axs[1, 2].set_title('Downsample Area')
axs[1, 2].axis('off')

axs[1, 3].imshow(downsampled_gaussian, cmap='gray')
axs[1, 3].set_title('Downsample Gaussian')
axs[1, 3].axis('off')

# 添加拉普拉斯金字塔上采样的图像
fig.add_subplot(2, 4, 8)  # 明确指定最后一个子图的位置
plt.imshow(upsampled_laplacian, cmap='gray')
plt.title('Upsample Laplacian')
plt.axis('off')

plt.tight_layout()
plt.show()
