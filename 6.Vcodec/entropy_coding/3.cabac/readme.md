# CABAC

> **CABAC = 带上下文自适应的二值算术编码**

拆开就是全部算法：
* Context-Adaptive（上下文自适应）
* Binary（二值化）
* Arithmetic Coding（算术编码）

---

## 为什么视频编码一定要 CABAC？

视频里要编码的是：
* 预测模式
* 运动矢量
* 变换系数

这些东西有两个特点：
1. **分布极不均匀**（0 特别多）
2. **概率取决于上下文**（位置 / 邻块 / 模式）

Huffman 做不到
普通算术编码概率太粗
**CABAC 专门为此设计**

---

## CABAC 的完整算法框架（重点）

**CABAC 不是一步，是 4 步流水线：**
```
语法元素
  ↓
二值化（binarization）
  ↓
上下文建模（context modeling）
  ↓
二值算术编码（binary arithmetic coding）
```

下面逐步讲。

---

### Step 1：二值化（Binarization）

**为什么要二值化？**

算术编码最简单、最高效的形式是：
> **只编码 0 / 1**

但视频语法元素是整数：
```
0, 1, 2, 3, 4, ...
```

所以：先变成 bin 串

例（Unary）：
```
value = 0 → 0
value = 1 → 10
value = 2 → 110
value = 3 → 1110
```

**小值 → bin 少 → bit 少**

---

### Step 2：上下文（Context Modeling）

这是 CABAC 的灵魂。

#### 问题

同一个 bin：
* 在平坦区域：

  ```
  P(bin=0) ≈ 0.98
  ```
* 在纹理区域：
  ```
  P(bin=0) ≈ 0.5
  ```

概率必须“因地制宜”

---

#### Context 是什么？

> **Context = 一个概率模型**

在代码里通常是：
```
struct {
    pStateIdx;   // 概率状态
    MPS;         // Most Probable Symbol (0 or 1)
}
```

每个 context：
* 只负责 **一种 bin**
* 会被不断更新

---

### Step 3：二值算术编码（核心）

CABAC 使用的是 **range coder**（算术编码的整数版本）。

#### 核心状态变量
```
low   // 当前区间起点
range // 当前区间大小
```

---

#### 编码一个 bin 的逻辑（极简）

假设：
* MPS = 0
* LPS = 1
* LPS 概率较小
```
range = range - LPS_range   → MPS
range = LPS_range           → LPS
```
然后：
* 如果是 LPS：low += range
* 更新 context 概率状态
* renormalize（移位输出 bit）

---

## 为什么 CABAC 解码慢？

**因为它是严格串行的**：
* 下一个 bin 的区间，依赖上一个 bin
* context 状态不断变化
* 不能并行

这是 H.265 / H.266 的性能瓶颈

---

## 一个“教学级”CABAC Demo（纯 C）

见当前文件夹


**这份 demo 和“真正 CABAC”的对应关系**
| 真 CABAC     | Demo 中               |
| ----------- | ---------------------- |
| bin         | `int bin`              |
| context     | 用固定 `pLPS` 代替     |
| MPS/LPS     | bin=0 / bin=1          |
| range coder | `low + range`          |
| renormalize | while(range < QUARTER) |

