# 传统计算机视觉 (Classical Computer Vision)

## 1. 简介

传统计算机视觉是指在深度学习流行之前，用于图像处理和特征提取的经典算法。这些算法在嵌入式设备、实时系统等场景中仍然广泛应用。

## 2. 目录

| 算法 | 类型 | 难度 | 特点 |
|------|------|------|------|
| Harris | 角点检测 | ★★☆☆☆ | 简单快速 |
| SIFT | 特征检测/描述 | ★★★★☆ | 尺度不变 |
| SURF | 特征检测/描述 | ★★★☆☆ | SIFT加速版 |
| ORB | 特征检测/描述 | ★★★☆☆ | 快速、免费 |
| HOG | 特征描述 | ★★★☆☆ | 物体检测 |
| LBP | 特征描述 | ★★☆☆☆ | 纹理特征 |
| Canny | 边缘检测 | ★★☆☆☆ | 经典边缘检测 |
| Lucas-Kanade | 光流法 | ★★★☆☆ | 稀疏光流 |
| Horn-Schunck | 光流法 | ★★★★☆ | 稠密光流 |

---

## 3. 角点检测

### 3.1 Harris角点检测

**原理**: 角点是两个边缘的交点，在两个方向上梯度都很大。

**公式**:
```
M = Σ w(x,y) [Ix²   IxIy]
              [IxIy  Iy² ]

R = det(M) - k·trace(M)²
```

**特点**:
- 对旋转不变
- 对光照变化鲁棒
- 计算简单

### 3.2 Shi-Tomasi角点
Harris的改进版，使用最小特征值作为响应：
```
R = min(λ1, λ2)
```

---

## 4. 特征检测与描述

### 4.1 SIFT (Scale-Invariant Feature Transform)

**难度**: ★★★★☆

**原理**: 在不同尺度空间上查找关键点，生成具有尺度、旋转不变性的描述子。

**流程**:
```
1. 尺度空间构建 (DoG金字塔)
2. 关键点定位 (极值检测)
3. 方向分配
4. 描述子生成 (128维)
```

**DoG (Difference of Gaussian)**:
```
D(x,y,σ) = (G(x,y,kσ) - G(x,y,σ)) * I(x,y)
```

**特点**:
- 尺度不变
- 旋转不变
- 光照不变
- 计算量大
- **专利已过期** (2020年)

**适用场景**: 图像匹配、全景拼接、物体识别

---

### 4.2 SURF (Speeded-Up Robust Features)

**难度**: ★★★☆☆

**原理**: SIFT的加速版本，使用Haar小波和积分图像加速计算。

**改进**:
- 用盒式滤波器近似高斯
- 使用积分图像加速
- 描述子为64维 (可扩展到128维)

**速度对比**: SURF比SIFT快3-10倍

**专利状态**: 专利已过期 (2020年)

---

### 4.3 ORB (Oriented FAST and Rotated BRIEF)

**难度**: ★★★☆☆

**原理**: 结合FAST角点检测和BRIEF描述子，添加方向和旋转不变性。

**组成**:
- **oFAST**: 带方向的FAST角点
- **rBRIEF**: 旋转不变的BRIEF描述子

**特点**:
- 极快 (比SIFT快100倍)
- 免费、无专利限制
- 二进制描述子 (匹配快)
- 部分尺度和旋转不变

**适用场景**: 实时应用、移动设备、SLAM

---

## 5. 特征描述子

### 5.1 HOG (Histogram of Oriented Gradients)

**原理**: 统计图像局部区域的梯度方向直方图。

**流程**:
```
1. 计算梯度 (Sobel)
2. 划分cell (如8x8)
3. 计算cell内的梯度方向直方图
4. 块归一化
5. 拼接所有块的直方图
```

**参数**:
- Cell大小: 8×8 像素
- Block大小: 2×2 cells
- 梯度方向bins: 9

**特点**:
- 对光照、阴影鲁棒
- 适合行人检测
- 不具备旋转不变性

**应用**: 行人检测、物体识别

### 5.2 LBP (Local Binary Pattern)

**原理**: 比较中心像素与邻域像素的灰度值。

**公式**:
```
LBP = Σ 2^i · s(neighbor_i - center)
s(x) = 1 if x ≥ 0, else 0
```

**特点**:
- 计算极快
- 灰度不变
- 旋转可变 (有旋转不变版本)

**应用**: 人脸识别、纹理分类

---

## 6. 边缘检测

### 6.1 Canny边缘检测

**流程**:
```
1. 高斯滤波降噪
2. Sobel计算梯度
3. 非极大值抑制
4. 双阈值检测
5. 边缘连接
```

**参数**:
- 低阈值: 约为高阈值的0.4-0.5倍
- 高阈值: 根据梯度分布确定

### 6.2 Sobel算子

```
Gx = [-1 0 1]    Gy = [-1 -2 -1]
     [-2 0 2]         [ 0  0  0]
     [-1 0 1]         [ 1  2  1]
```

---

## 7. 算法对比

### 7.1 特征检测对比

| 特性 | SIFT | SURF | ORB |
|------|------|------|-----|
| 速度 | 慢 | 中 | 快 |
| 尺度不变 | ✓ | ✓ | 部分 |
| 旋转不变 | ✓ | ✓ | ✓ |
| 专利 | 无 | 无 | 无 |
| 描述子维度 | 128 | 64/128 | 256(二进制) |
| 适用场景 | 高精度 | 平衡 | 实时 |

### 7.2 特征描述子对比

| 特性 | SIFT | HOG | LBP |
|------|------|-----|-----|
| 维度 | 128 | ~3780 | 256 |
| 计算速度 | 慢 | 中 | 快 |
| 光照鲁棒 | 好 | 好 | 一般 |
| 应用 | 匹配 | 检测 | 纹理 |

---

## 8. 代码示例

### OpenCV特征检测

```python
import cv2

# SIFT
sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(img, None)

# SURF (需要opencv-contrib)
surf = cv2.xfeatures2d.SURF_create()
keypoints, descriptors = surf.detectAndCompute(img, None)

# ORB
orb = cv2.ORB_create()
keypoints, descriptors = orb.detectAndCompute(img, None)

# 特征匹配
bf = cv2.BFMatcher(cv2.NORM_L2)
matches = bf.knnMatch(des1, des2, k=2)

# 筛选好匹配
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m])
```

---

## 9. 应用场景

| 应用 | 推荐算法 |
|------|---------|
| 全景拼接 | SIFT/SURF/ORB |
| 物体识别 | SIFT + BoW |
| 行人检测 | HOG + SVM |
| 人脸识别 | LBP/HOG + SVM |
| SLAM | ORB |
| 实时跟踪 | ORB |
| 运动估计 | Lucas-Kanade/Horn-Schunck |
| 目标跟踪 | KCF + 光流 |

---

## 10. 子目录链接

| 子目录 | 描述 |
|--------|------|
| [01.basic_filtering](./01.basic_filtering/readme.md) | 基本滤波算法 |
| [02.corner_detection](./02.corner_detection/readme.md) | 角点检测算法 |
| [03.feature_detection](./03.feature_detection/readme.md) | 特征检测算法 |
| [04.feature_descriptor](./04.feature_descriptor/readme.md) | 特征描述子算法 |
| [05.optical_flow](./05.optical_flow/readme.md) | 光流法算法 |

---

## 11. 示例代码

见 `demo.py`，包含：
- Harris角点检测
- SIFT特征检测与匹配
- ORB特征检测与匹配
- HOG特征提取
- Canny边缘检测

---

## 参考资料

- Lowe, D. G. (2004). Distinctive Image Features from Scale-Invariant Keypoints
- Bay, H., et al. (2006). SURF: Speeded Up Robust Features
- Rublee, E., et al. (2011). ORB: an efficient alternative to SIFT or SURF
- Dalal, N., & Triggs, B. (2005). Histograms of Oriented Gradients for Human Detection
- OpenCV文档: https://docs.opencv.org/
