# 上采样算法

上采样是指在保持信号原始频带的前提下，提高信号采样率的过程。

## 最近邻插值 (Nearest Neighbor Interpolation)

原理：将最近的一个像素的值直接赋值给新生成的像素。
代码示例：
```python
import numpy as np
import cv2
import matplotlib.pyplot as plt

# 生成一个简单的2x2图像
img = np.array([[0, 255], [255, 0]], dtype=np.uint8)

# 使用最近邻插值进行上采样，扩大2倍
upsampled_img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)

plt.imshow(upsampled_img, cmap='gray')
plt.show()
```

## 双线性插值 (Bilinear Interpolation)

原理：插值点的值由距离它最近的四个像素的值加权平均得到。
代码示例：
```python
upsampled_img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

plt.imshow(upsampled_img, cmap='gray')
plt.show()
```

## 双三次插值 (Bicubic Interpolation)

原理：利用16个邻近像素点的值进行插值，比双线性插值的效果更平滑。
代码示例：
```python
upsampled_img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

plt.imshow(upsampled_img, cmap='gray')
plt.show()
```

## 拉普拉斯金字塔插值 (Laplacian Pyramid Interpolation)

原理：基于多尺度金字塔的方法，将图像分解为多个尺度的表示，逐层上采样和重建。
代码示例：
```python
# 这里提供一个简化版本，通常拉普拉斯金字塔插值较复杂，需要多个步骤
G = img.copy()
gpA = [G]

# 构建高斯金字塔
for i in range(1):
    G = cv2.pyrDown(G)
    gpA.append(G)

# 反向上采样
G = gpA[1]
laplacian = cv2.pyrUp(G)

plt.imshow(laplacian, cmap='gray')
plt.show()
```

# 下采样算法

下采样是指在保持信号原始频带的前提下，降低信号采样率的过程。

## 最近邻插值 (Nearest Neighbor Interpolation)

原理：将一个区域内的像素点取最靠近新采样位置的像素值。
代码示例：
```python
downsampled_img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)

plt.imshow(downsampled_img, cmap='gray')
plt.show()
```

## 双线性插值 (Bilinear Interpolation)

原理：利用临近的四个像素点进行加权平均，适用于图像放大和缩小。
代码示例：
```python
downsampled_img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

plt.imshow(downsampled_img, cmap='gray')
plt.show()
```

## 区域插值 (Area Interpolation)

原理：通过计算区域内的像素值的平均值进行缩小操作，适用于下采样。
代码示例：
```python
downsampled_img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

plt.imshow(downsampled_img, cmap='gray')
plt.show()
```

## 高斯金字塔 (Gaussian Pyramid)

原理：通过先对图像进行模糊处理，然后进行下采样，减少伪影。
代码示例：
```python
downsampled_img = cv2.pyrDown(img)

plt.imshow(downsampled_img, cmap='gray')
plt.show()
```


