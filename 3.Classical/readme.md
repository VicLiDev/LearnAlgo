# 经典应用算法 (Classical Application Algorithms)

本目录包含 AI 时代之前的经典应用算法，分为点云处理和图像处理两大类。

> **定位**: 这些是能解决具体实际问题的算法，而非抽象的理论知识。

## 目录结构

```
3.Classical/
├── readme.md                       # 本文件
│
├── 01.point_cloud/                 # 点云相关算法
│   ├── 01.preprocessing/           # 点云预处理
│   ├── 02.icp/                     # ICP 点云配准
│   ├── 03.ndt/                     # NDT 正态分布变换
│   └── 04.ppf/                     # PPF 6D姿态估计
│
└── 02.classical_cv/                # 传统计算机视觉 (2D图像)
    ├── 01.basic_filtering/         # 基础滤波与边缘检测
    ├── 02.corner_detection/        # 角点检测
    ├── 03.feature_detection/       # 特征检测 (SIFT/ORB)
    ├── 04.feature_descriptor/      # 特征描述子 (HOG/LBP)
    └── 05.optical_flow/            # 光流法
```

---

## 01. 点云算法 (Point Cloud Algorithms)

### 01.preprocessing - 预处理

**难度**: ★★☆☆☆

| 方法 | 说明 |
|------|------|
| 体素滤波 | 降采样，减少数据量 |
| 统计离群点移除 | 基于邻域距离去噪 |
| 法向量估计 | PCA方法 |

```bash
cd 01.point_cloud/01.preprocessing && python demo.py
```

---

### 02.icp - ICP配准

**难度**: ★★★☆☆

- Point-to-Point / Point-to-Plane
- SVD求解刚体变换

```bash
cd 01.point_cloud/02.icp && python demo.py
```

---

### 03.ndt - NDT配准

**难度**: ★★★☆☆

- 概率点云配准，对噪声鲁棒

```bash
cd 01.point_cloud/03.ndt && python demo.py
```

---

### 04.ppf - 6D姿态估计

**难度**: ★★★★☆

- 物体识别 + 姿态估计

```bash
cd 01.point_cloud/04.ppf && cat readme.md
```

---

## 02. 传统计算机视觉 (Classical Computer Vision)

### 01.basic_filtering - 基础滤波

**难度**: ★☆☆☆☆

| 内容 | 说明 |
|------|------|
| 线性滤波 | 均值、高斯、双边 |
| 边缘检测 | Sobel, Canny |

```bash
cd 02.classical_cv/01.basic_filtering && python demo.py
```

---

### 02.corner_detection - 角点检测

**难度**: ★★☆☆☆

| 算法 | 速度 | 特点 |
|------|------|------|
| Harris | 中等 | 经典角点检测 |
| Shi-Tomasi | 中等 | Harris改进 |
| FAST | 快 | 实时检测 |

```bash
cd 02.classical_cv/02.corner_detection && python demo.py
```

---

### 03.feature_detection - 特征检测

**难度**: ★★★☆☆

| 算法 | 尺度不变 | 旋转不变 | 速度 |
|------|----------|----------|------|
| SIFT | ✓ | ✓ | 慢 |
| SURF | ✓ | ✓ | 中 |
| ORB | ✓ | ✓ | 快 |

```bash
cd 02.classical_cv/03.feature_detection && python demo.py
```

---

### 04.feature_descriptor - 特征描述子

**难度**: ★★★☆☆

| 描述子 | 应用 |
|--------|------|
| HOG | 行人检测 |
| LBP | 人脸/纹理识别 |

```bash
cd 02.classical_cv/04.feature_descriptor && python demo.py
```

---

### 05.optical_flow - 光流法

**难度**: ★★★★☆

| 方法 | 类型 | 特点 |
|------|------|------|
| Lucas-Kanade | 稀疏 | 特定点跟踪 |
| Horn-Schunck | 稠密 | 全像素运动 |
| Farneback | 稠密 | OpenCV实现 |

```bash
cd 02.classical_cv/05.optical_flow && python demo.py
```

---

## 算法分类总览

### 按任务分类

| 任务 | 点云算法 | 图像算法 |
|------|----------|----------|
| 预处理 | 体素滤波, 去噪 | 滤波, 边缘检测 |
| 特征提取 | 法向量, 曲率 | 角点, SIFT, ORB |
| 配准 | ICP, NDT | 特征匹配 |
| 检测 | PPF | HOG + SVM |
| 跟踪 | - | 光流法 |

### 按难度分类

```
★☆☆☆☆  基础滤波
★★☆☆☆  角点检测, 点云预处理
★★★☆☆  ICP, NDT, SIFT, ORB, 光流
★★★★☆  PPF, HOG, 稠密光流
```

---

## 学习路径

### 点云方向

```
01.preprocessing (去噪、降采样)
    ↓
02.icp (经典配准)
    ↓
03.ndt (概率方法)
    ↓
04.ppf (识别+姿态)
```

### 图像方向

```
01.basic_filtering (滤波、边缘)
    ↓
02.corner_detection (角点)
    ↓
03.feature_detection (SIFT/ORB)
    ↓
04.feature_descriptor (HOG/LBP)
    ↓
05.optical_flow (运动估计)
```

---

## 参考资料

### 书籍
- 《计算机视觉：算法与应用》- Richard Szeliski
- 《点云库PCL教程》
- 《Learning OpenCV》

### 在线资源
- [OpenCV 文档](https://docs.opencv.org/)
- [PCL](https://pointclouds.org/)
- [Open3D](http://www.open3d.org/)

---

## 许可证

MIT License
