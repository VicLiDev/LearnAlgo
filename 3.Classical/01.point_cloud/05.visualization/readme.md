# 点云加载与可视化Demo

## 功能

- 加载多种格式的点云文件（PLY、XYZ等）
- 交互式3D可视化（基于Open3D，硬件加速渲染）
- 支持多幅点云在同一窗口中同时显示
- 辅助元素：自适应坐标轴、包围盒、地面网格
- 命令行打印所有辅助元素的详细参数
- 显示点云基本信息（点数、边界框、质心等）
- 生成随机测试点云（球、立方体、环面）
- 多视角可视化（俯视、仰视、正视、侧视）
- 点云保存功能

## 依赖

```bash
pip install numpy open3d
```

> 注意：Open3D 需要 NumPy 2.x 兼容的 pyarrow，如遇 `_ARRAY_API not found` 错误，执行 `pip install --upgrade pyarrow`。

## 使用方法

### 1. 加载并可视化点云文件

```bash
# 单幅点云（高度渐变彩色）
python demo.py <点云文件路径>

# 多幅点云同时显示（自动用不同颜色区分）
python demo.py <文件1> <文件2> <文件3>
```

### 2. 演示模式（无需文件）

```bash
python demo.py
```

会依次演示：单幅球形点云、多视角环面点云、多幅点云同屏显示。

## 交互控制

| 操作 | 功能 |
|------|------|
| 鼠标左键拖动 | 旋转视角 |
| 滚轮 | 缩放 |
| Shift + 左键拖动 | 平移 |
| ESC / Q | 退出 |

## API使用

```python
from demo import PointCloudViewer

viewer = PointCloudViewer()

# --- 单幅点云 ---

viewer.load_point_cloud("path/to/cloud.ply")
# 或创建随机点云
viewer.create_random_point_cloud(n_points=3000, shape='sphere', radius=2.0)

viewer.print_info()

# 可视化（单幅，高度渐变彩色）
viewer.visualize(
    title="My Point Cloud",
    point_size=2,
    color_mode='height',   # 'height', 'original', 'random'
    show_axes=True,        # 坐标轴 + 刻度线
    show_grid=True,        # 地面网格
    show_bbox=True,        # 包围盒
)

# 多视角可视化
viewer.visualize_multi_view(title="Multi View")

# --- 多幅点云 ---

viewer.load_multiple(["cloud1.ply", "cloud2.xyz"])
# 或手动添加
viewer.add_cloud("my_cloud", points_array, colors_array)

# 多幅同屏显示
viewer.visualize_multi_cloud(
    color_mode='palette',  # 'palette'(按颜色区分), 'original', 'height'
    point_size=2,
    show_axes=True,
    show_grid=True,
    show_bbox=True,        # 每幅点云单独的彩色包围盒
)

# 保存
viewer.save_xyz("output.xyz")
```

## 可视化辅助元素

| 元素 | 说明 |
|------|------|
| RGB 坐标轴 | 红=X, 绿=Y, 蓝=Z，大小自适应点云范围，带刻度线 |
| 延长轴线 | 穿过原点的三色轴线，辅助判断方向 |
| 包围盒 | 灰色线框标注 AABB 范围；多幅模式时用调色板颜色区分 |
| 地面网格 | XY 平面 11x11 网格，辅助空间定位 |

所有辅助元素的参数（坐标范围、标尺长度、网格间距、质心等）会在命令行同步打印。

## 支持的文件格式

- PLY (.ply) - ASCII / Binary 格式
- XYZ (.xyz, .txt, .pts) - ASCII 点云格式

## 命令行输出示例

```
==================================================
点云信息
==================================================
文件路径: model.ply
点数量: 6700
是否有颜色: False

坐标范围:
  X: [-55.1494, 174.8510]
  Y: [-191.3260, 71.3345]
  Z: [-686.0190, -582.9920]

边界框大小:
  230.0004 x 262.6605 x 103.0270

质心位置:
  (12.1772, -21.4604, -630.7647)
==================================================

--------------------------------------------------
辅助元素
--------------------------------------------------
  坐标轴 (RGB):
    X (红) 范围 [-55.149, 174.851], 轴长 230.000
    Y (绿) 范围 [-191.326, 71.335], 轴长 262.661
    Z (蓝) 范围 [-686.019, -582.992], 轴长 103.027
    原点位于: (-55.149, -191.326, -686.019), 标尺长度 182.165
  包围盒:
    Min: (-55.149, -191.326, -686.019)
    Max: (174.851, 71.335, -582.992)
    尺寸: 230.000 x 262.661 x 103.027
  地面网格 (XY平面):
    范围 [-220.765, 220.765] x [-220.765, 220.765]
    网格间距: 44.153, 共 11x11 条线
  质心: (12.177, -21.460, -630.765)
  对角线长度: 728.660
--------------------------------------------------
```
