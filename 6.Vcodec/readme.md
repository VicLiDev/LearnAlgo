# 视频编解码 (Video Codec)

本目录包含视频编解码的核心技术，涵盖熵编码、变换编码、预测编码、运动估计等关键模块。

## 目录结构

```
6.Vcodec/
├── readme.md                       # 本文件
│
├── 01.entropy_coding/              # 熵编码
│   ├── 01.huffman/                 # Huffman编码
│   ├── 02.arithmetic_coding/       # 算术编码
│   └── 03.cabac/                   # CABAC (H.264/HEVC)
│
├── 02.transform_coding/            # 变换编码
│   └── readme.md                   # DCT, 整数变换, DWT
│
├── 03.prediction/                  # 预测编码
│   └── readme.md                   # 帧内/帧间预测
│
├── 04.motion_estimation/           # 运动估计
│   └── readme.md                   # 块匹配, 亚像素插值
│
├── 05.quantization/                # 量化
│   └── readme.md                   # 标量量化, 矩阵量化
│
├── 06.inloop_filter/               # 环路滤波
│   └── readme.md                   # 去块滤波, SAO, ALF
│
└── 07.rate_control/                # 码率控制
    └── readme.md                   # CRF, ABR, CBR
```

---

## 视频编码流程

```
输入帧
    ↓
┌─────────────────────────────────────┐
│  预测编码                            │
│  ┌─────────────┐  ┌─────────────┐   │
│  │ 帧内预测    │  │ 帧间预测    │   │
│  │ (I帧)       │  │ (P/B帧)     │   │
│  └─────────────┘  └─────────────┘   │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  变换 + 量化                         │
│  残差 → DCT → QP量化                 │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  熵编码                              │
│  系数 → CABAC → 码流                 │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  环路滤波                            │
│  去块 → SAO → ALF                    │
└─────────────────────────────────────┘
    ↓
重建帧 (作为参考)
```

---

## 模块详解

### 01. 熵编码 (Entropy Coding)

**难度**: ★★★☆☆

| 方法 | 原理 | 应用 |
|------|------|------|
| Huffman | 变长编码，高频符号短码 | JPEG, MPEG-2 |
| 算术编码 | 区间编码，更高效 | H.263, MPEG-4 |
| CABAC | 上下文自适应算术编码 | H.264, HEVC |

```bash
cd 01.entropy_coding/03.cabac && python demo.py
```

---

### 02. 变换编码 (Transform Coding)

**难度**: ★★★☆☆

| 变换 | 特点 | 应用 |
|------|------|------|
| DCT | 能量集中，快速算法 | JPEG, H.261/2/3 |
| 整数DCT | 无精度损失 | H.264, HEVC |
| DWT | 多分辨率 | JPEG2000 |
| Hadamard | 简单快速 | H.264 intra DC |

---

### 03. 预测编码 (Prediction)

**难度**: ★★★☆☆

| 类型 | 参考帧 | 压缩效率 |
|------|--------|----------|
| 帧内预测 | 无 | 低 |
| 帧间预测(P) | 前向 | 中 |
| 帧间预测(B) | 双向 | 高 |

**帧内预测模式**:
- Planar: 平滑区域
- DC: 均匀区域
- Angular: 方向纹理

---

### 04. 运动估计 (Motion Estimation)

**难度**: ★★★★☆

| 算法 | 搜索点数 | 质量 |
|------|----------|------|
| 全搜索 | (2R+1)² | 最优 |
| 菱形搜索 | ~15 | 良好 |
| UMHexagonS | ~30 | 优秀 |

**亚像素精度**:
- 1/2像素: 6抽头滤波器
- 1/4像素: 双线性插值

---

### 05. 量化 (Quantization)

**难度**: ★★☆☆☆

```
量化: Q(x) = round(x / QP)
反量化: Q⁻¹(y) = y × QP
```

| QP | 质量 | 压缩比 |
|----|------|--------|
| 18 | 视觉无损 | 低 |
| 23 | 默认 | 中 |
| 28 | 可接受 | 中高 |
| 51 | 最差 | 高 |

---

### 06. 环路滤波 (In-Loop Filter)

**难度**: ★★★★☆

| 滤波器 | 作用 | 标准支持 |
|--------|------|----------|
| Deblocking | 去块效应 | H.264+ |
| SAO | 样点自适应偏移 | HEVC |
| ALF | 自适应环路滤波 | VVC |

---

### 07. 码率控制 (Rate Control)

**难度**: ★★★★☆

| 模式 | 说明 | 应用 |
|------|------|------|
| CQP | 固定QP | 研究/测试 |
| CRF | 质量优先 | x264/x265默认 |
| CBR | 恒定码率 | 直播 |
| ABR | 平均码率 | 点播 |
| VBR | 可变码率 | 存储 |

**CRF值参考**:
- 18: 视觉无损
- 23: 默认
- 28: 可接受
- 51: 最差

---

## 编码标准演进

```
H.261 (1990) → MPEG-1 (1993) → MPEG-2/H.262 (1995)
                                  ↓
H.263 (1996) → MPEG-4 (1999) → H.264/AVC (2003)
                                  ↓
                           HEVC/H.265 (2013)
                                  ↓
                            VVC/H.266 (2020)
```

### 压缩效率对比

| 标准 | 分辨率 | 相对效率 |
|------|--------|----------|
| MPEG-2 | 1080p | 1× |
| H.264 | 1080p | 2× |
| HEVC | 4K | 2× H.264 |
| VVC | 8K | 1.5× HEVC |

---

## 学习路径

```
入门:
01.entropy_coding → 理解无损压缩
    ↓
基础:
02.transform_coding → 理解频域变换
03.prediction → 理解预测编码
    ↓
核心:
04.motion_estimation → 理解时间冗余消除
05.quantization → 理解有损压缩
    ↓
高级:
06.inloop_filter → 理解图像质量优化
07.rate_control → 理解码率-质量平衡
```

---

## 实践工具

### 编码器

| 编码器 | 标准 | 特点 |
|--------|------|------|
| x264 | H.264 | 最成熟，速度快 |
| x265 | HEVC | 压缩率高 |
| SVT-AV1 | AV1 | 开源免费 |
| VVenC | VVC | 最新标准 |

### 分析工具

```bash
# 码流分析
FFprobe -show_frames input.mp4

# 编码质量评估
VMAF -r ref.yuv -d dis.yuv -w 1920 -h 1080

# 码率曲线
ffprobe -show_entries frame=pkt_size -of csv input.mp4
```

### FFmpeg常用命令

```bash
# CRF编码
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4

# 两遍编码 (ABR)
ffmpeg -i input.mp4 -c:v libx264 -b:v 4M -pass 1 -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 4M -pass 2 output.mp4

# HEVC编码
ffmpeg -i input.mp4 -c:v libx265 -crf 28 output.mp4
```

---

## 参考资料

### 书籍
- 《Video Demystified》
- 《High Efficiency Video Coding (HEVC)》
- 《Video Compression Handbook》

### 标准
- ITU-T H.264 / ISO/IEC 14496-10
- ITU-T H.265 / ISO/IEC 23008-2
- ITU-T H.266 / ISO/IEC 23090-3

### 在线资源
- [FFmpeg 文档](https://ffmpeg.org/documentation.html)
- [x264 论文](https://developers.google.com/media/x264/)
- [VVC 介绍](https://jvet.hhi.fraunhofer.de/)

---

## 许可证

MIT License
