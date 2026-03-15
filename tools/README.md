# LearnAI

AI 学习笔记与示例代码。

## 快速开始

**是否需要初始化？**

| 情况 | 是否需要执行 `0.init.sh` |
|------|-------------------------|
| 使用 matplotlib 中文显示等功能 | ✅ 需要 |
| 新电脑首次克隆项目 | ✅ 需要 |
| 只运行不依赖 tools 的 demo | ❌ 不需要 |

**初始化命令：**

```bash
cd /path/to/LearnAI
./0.init.sh
```

## 目录结构

```
LearnAI/
├── 0.init.sh              # 初始化脚本
├── tools/                 # 工具模块（独立子项目）
│   ├── pyproject.toml     # 包配置
│   ├── t01_mpl/           # matplotlib 相关工具
│   │   └── chinese_font.py
│   └── eigen/             # eigen 矩阵库
├── 1.BasicAlgo/           # 基础算法
├── 2.GenAlgorithm/        # 通用算法
├── 3.Classical/           # 经典方法
├── 4.ML/                  # 机器学习
├── 5.DL/                  # 深度学习
└── 6.Vcodec/              # 视频编码
```

## tools/pyproject.toml 说明

`pyproject.toml` 是 Python 项目的现代配置文件（PEP 518/621），用于替代传统的 `setup.py`。

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "learnai-tools"
version = "0.1.0"

[tool.setuptools.packages.find]
where = ["."]
include = ["*"]
```

| 字段 | 作用 |
|------|------|
| `[build-system]` | 声明使用 setuptools 构建 |
| `[project]` | 包名和版本 |
| `[tool.setuptools.packages.find]` | 当前目录所有模块可导入 |

运行 `pip install -e .` 后（在 tools 目录下），Python 就能在任何位置识别这些模块。

## 工具模块

### chinese_font (tools/t01_mpl/)

解决 matplotlib 中文显示问题：

```python
from t01_mpl import chinese_font  # 自动配置中文字体
import matplotlib.pyplot as plt

plt.title("中文标题")  # 正常显示
```
