# 码率控制 (Rate Control)

## 1. 简介

码率控制决定编码器的量化参数，在给定带宽/存储限制下优化视频质量。

## 2. 码率控制模式

| 模式 | 说明 | 应用 |
|------|------|------|
| CQP | 固定QP | 质量优先 |
| CBR | 恒定码率 | 直播 |
| VBR | 可变码率 | 存储 |
| CRF | 恒定质量 | x264/x265 |

## 3. QP确定方法

### 3.1 CQP (Constant QP)

```
所有帧使用相同QP
简单但码率波动大
```

### 3.2 CRF (Constant Rate Factor)

```
QP = base_QP + CRF_offset

CRF值:
- 18: 视觉无损
- 23: 默认
- 28: 可接受质量
- 51: 最差质量

考虑因素:
- 帧复杂度 (通过SATD估计)
- 视觉掩蔽效应
```

## 4. 码率分配

### 4.1 GOP级别

```
Total_Bits = Target_Bitrate × GOP_Length

分配到各帧:
I帧: 分配更多比特 (关键帧)
P帧: 中等
B帧: 分配较少
```

### 4.2 帧级别

```
frame_bits = target_bits × complexity_ratio

complexity_ratio = current_SATD / average_SATD
```

### 4.3 CTU/宏块级别

```
根据局部复杂度调整QP:
- 高复杂区域: 降低QP
- 低复杂区域: 增大QP
```

## 5. 码率模型

### 5.1 R-Q模型

```
R = α × QP^(-β)

R: 编码比特数
α, β: 模型参数 (通过训练更新)
```

### 5.2 ρ域模型

```
R = θ × (1 - ρ)

ρ: 零系数比例
θ: 模型参数
```

### 5.3 模型更新

```
编码后更新模型参数:
α_new = α_old × 0.9 + α_measured × 0.1
```

## 6. 缓冲区管理

### 6.1 漏桶模型

```
        ┌─────────────┐
  入 →  │   Buffer    │ → 出 (恒定码率)
        │  [========] │
        └─────────────┘
          ↑
        水位控制

水位高 → 增大QP
水位低 → 降低QP
```

### 6.2 HRD (Hypothetical Reference Decoder)

```
定义:
- 最大缓冲区大小
- 初始缓冲区充满度
- 比特移除时间

确保码流可被解码
```

## 7. 自适应码率控制

### 7.1 场景检测

```
场景切换时:
- 重置码率模型
- 分配更多比特
- 可能插入I帧
```

### 7.2 内容感知

```
内容类型:
- 运动: 需要更多比特
- 静止: 需要较少比特
- 文字: 需要高质量
```

## 8. x264/x265实现

### 8.1 CRF模式

```
x264_param_t param;
param.rc.i_rc_method = X264_RC_CRF;
param.rc.f_rf_constant = 23.0;  // CRF值
```

### 8.2 ABR模式

```
param.rc.i_rc_method = X264_RC_ABR;
param.rc.i_bitrate = 4000;  // kbps
param.rc.i_vbv_max_bitrate = 5000;
param.rc.i_vbv_buffer_size = 8000;
```

## 9. 率失真优化

### 9.1 RDO框架

```
min Cost = D + λ × R

λ 由 QP 决定:
λ = 0.85 × 2^((QP-12)/3)
```

### 9.2 模式选择中的RC

```
选择最优模式 = argmin(D + λ × R)

考虑:
- 编码比特
- 失真度量
- 量化参数
```

## 10. 代码示例

见 `demo.py`

## 11. 参考资料

- H.264 Rate Control
- x264 Rate Control
- Rate-Distortion Optimized Video Communication
