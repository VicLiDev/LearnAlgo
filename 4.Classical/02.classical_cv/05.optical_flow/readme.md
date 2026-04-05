# 光流法 (Optical Flow)

## 1. 简介

光流是像素在连续帧之间的运动矢量，用于运动估计、目标跟踪等。

## 2. 算法分类

| 类型 | 方法 | 特点 |
|------|------|------|
| 稀疏光流 | Lucas-Kanade | 特定点跟踪 |
| 稠密光流 | Horn-Schunck | 全像素运动 |
| 深度学习 | FlowNet, RAFT | 精度高 |

## 3. Lucas-Kanade

### 3.1 假设

1. **亮度恒定**: 同一点在连续帧亮度不变
2. **小运动**: 帧间位移小
3. **空间一致**: 邻域点运动相同

### 3.2 推导

```
I(x, y, t) = I(x+dx, y+dy, t+dt)

泰勒展开:
I_x * u + I_y * v + I_t = 0

其中 u=dx/dt, v=dy/dt 是光流
```

### 3.3 求解

对于邻域内n个点:

```
[Ix1  Iy1]   [u]   [-It1]
[Ix2  Iy2] * [v] = [-It2]
[...]  ...         [...]
```

最小二乘解:
```
[u]   [ΣIx²   ΣIxIy]^(-1)  [-ΣIxIt]
[v] = [ΣIxIy  ΣIy²  ]      [-ΣIyIt]
```

## 4. Horn-Schunck

### 4.1 目标函数

```
E = ∫∫ [(Ix*u + Iy*v + It)² + α²(|∇u|² + |∇v|²)] dx dy

第一项: 数据项 (光流约束)
第二项: 平滑项 (光流场平滑)
```

### 4.2 迭代求解

```
u^(k+1) = ū^(k) - Ix * (Ix*ū^(k) + Iy*v̄^(k) + It) / (α² + Ix² + Iy²)
v^(k+1) = v̄^(k) - Iy * (Ix*ū^(k) + Iy*v̄^(k) + It) / (α² + Ix² + Iy²)
```

## 5. OpenCV实现

### 5.1 稀疏光流

```python
# Lucas-Kanade
lk_params = dict(
    winSize=(15, 15),
    maxLevel=2,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
)
p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, next_gray, p0, None, **lk_params)
```

### 5.2 稠密光流

```python
# Farneback
flow = cv2.calcOpticalFlowFarneback(prev_gray, next_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
```

## 6. 代码示例

见 `demo.py`
