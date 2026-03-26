#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
点云加载与可视化Demo
功能：
1. 加载点云数据（支持PLY格式）
2. 交互式3D可视化（基于Open3D）
3. 点云基本信息显示
"""

import numpy as np
import open3d as o3d
import os
import sys


class PointCloudViewer:
    """点云可视化器"""

    # 多幅点云使用的调色板
    PALETTE = [
        [1.0, 0.3, 0.3],   # 红
        [0.3, 1.0, 0.3],   # 绿
        [0.3, 0.5, 1.0],   # 蓝
        [1.0, 1.0, 0.3],   # 黄
        [1.0, 0.3, 1.0],   # 品红
        [0.3, 1.0, 1.0],   # 青
        [1.0, 0.6, 0.2],   # 橙
        [0.6, 0.3, 1.0],   # 紫
    ]

    def __init__(self):
        self.points = None
        self.colors = None
        self.file_path = None
        # 多幅点云列表, 每项: {"name": str, "points": ndarray, "colors": ndarray|None}
        self.clouds = []

    def load_ply(self, file_path):
        """
        加载PLY格式点云文件

        Args:
            file_path: PLY文件路径

        Returns:
            bool: 加载是否成功
        """
        if not os.path.exists(file_path):
            print(f"错误: 文件不存在 - {file_path}")
            return False

        self.file_path = file_path

        try:
            pcd = o3d.io.read_point_cloud(file_path)
            if not pcd.has_points():
                print(f"加载失败: 文件中没有点云数据 - {file_path}")
                return False

            self.points = np.asarray(pcd.points)
            if pcd.has_colors():
                self.colors = np.asarray(pcd.colors)
            else:
                self.colors = None

            print(f"成功加载点云: {file_path}")
            self.clouds.append({"name": os.path.basename(file_path),
                                "points": self.points, "colors": self.colors})
            return True
        except Exception as e:
            print(f"加载失败: {e}")
            return False

    def load_xyz(self, file_path):
        """
        加载XYZ格式点云文件

        Args:
            file_path: XYZ文件路径

        Returns:
            bool: 加载是否成功
        """
        if not os.path.exists(file_path):
            print(f"错误: 文件不存在 - {file_path}")
            return False

        self.file_path = file_path

        try:
            pcd = o3d.io.read_point_cloud(file_path)
            if not pcd.has_points():
                # Open3D 解析失败时回退到 numpy 手动加载
                data = np.loadtxt(file_path)
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(data[:, :3])
                if data.shape[1] >= 6:
                    colors = data[:, 3:6]
                    if colors.max() > 1.0:
                        colors = colors / 255.0
                    pcd.colors = o3d.utility.Vector3dVector(colors)

            self.points = np.asarray(pcd.points)
            if pcd.has_colors():
                self.colors = np.asarray(pcd.colors)
            else:
                self.colors = None

            print(f"成功加载点云: {file_path}")
            self.clouds.append({"name": os.path.basename(file_path),
                                "points": self.points, "colors": self.colors})
            return True
        except Exception as e:
            print(f"加载失败: {e}")
            return False

    def load_point_cloud(self, file_path):
        """
        自动识别格式并加载点云

        Args:
            file_path: 点云文件路径

        Returns:
            bool: 加载是否成功
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.ply':
            return self.load_ply(file_path)
        elif ext in ['.xyz', '.txt', '.pts']:
            return self.load_xyz(file_path)
        else:
            print(f"不支持的文件格式: {ext}")
            return False

    def create_random_point_cloud(self, n_points=1000, shape='sphere', center=(0, 0, 0), radius=1.0):
        """
        创建随机测试点云

        Args:
            n_points: 点的数量
            shape: 形状类型 ('sphere', 'cube', 'torus')
            center: 中心坐标
            radius: 半径/大小
        """
        if shape == 'sphere':
            phi = np.random.uniform(0, 2 * np.pi, n_points)
            cos_theta = np.random.uniform(-1, 1, n_points)
            theta = np.arccos(cos_theta)

            x = radius * np.sin(theta) * np.cos(phi)
            y = radius * np.sin(theta) * np.sin(phi)
            z = radius * np.cos(theta)

        elif shape == 'cube':
            n_per_face = n_points // 6
            points_list = []
            for i in [-1, 1]:
                face = np.random.uniform(-radius, radius, (n_per_face, 3))
                face[:, 0] = i * radius
                points_list.append(face)
                face = np.random.uniform(-radius, radius, (n_per_face, 3))
                face[:, 1] = i * radius
                points_list.append(face)
                face = np.random.uniform(-radius, radius, (n_per_face, 3))
                face[:, 2] = i * radius
                points_list.append(face)
            points = np.vstack(points_list)
            x, y, z = points[:, 0], points[:, 1], points[:, 2]

        elif shape == 'torus':
            R, r = radius, radius * 0.3
            theta = np.random.uniform(0, 2 * np.pi, n_points)
            phi = np.random.uniform(0, 2 * np.pi, n_points)

            x = (R + r * np.cos(phi)) * np.cos(theta)
            y = (R + r * np.cos(phi)) * np.sin(theta)
            z = r * np.sin(phi)
        else:
            x = np.random.uniform(-radius, radius, n_points)
            y = np.random.uniform(-radius, radius, n_points)
            z = np.random.uniform(-radius, radius, n_points)

        self.points = np.column_stack([x, y, z])
        self.points += np.array(center)

        self.colors = self._height_based_colors()

        name = f"{shape}_{n_points}"
        self.clouds.append({"name": name, "points": self.points.copy(),
                            "colors": self.colors.copy()})

        print(f"创建随机点云: {n_points} 个点, 形状: {shape}")

    def _height_based_colors(self):
        """根据高度生成渐变颜色"""
        if self.points is None or len(self.points) == 0:
            return None

        z = self.points[:, 2]
        z_norm = (z - z.min()) / (z.max() - z.min() + 1e-8)

        colors = np.zeros((len(self.points), 3))
        colors[:, 0] = z_norm
        colors[:, 2] = 1 - z_norm
        return colors

    def print_info(self):
        """打印点云基本信息"""
        if self.points is None:
            print("未加载点云")
            return

        print("\n" + "=" * 50)
        print("点云信息")
        print("=" * 50)
        print(f"文件路径: {self.file_path if self.file_path else '内存生成'}")
        print(f"点数量: {len(self.points)}")
        print(f"是否有颜色: {self.colors is not None}")

        if len(self.points) > 0:
            print(f"\n坐标范围:")
            print(f"  X: [{self.points[:, 0].min():.4f}, {self.points[:, 0].max():.4f}]")
            print(f"  Y: [{self.points[:, 1].min():.4f}, {self.points[:, 1].max():.4f}]")
            print(f"  Z: [{self.points[:, 2].min():.4f}, {self.points[:, 2].max():.4f}]")

            bbox_size = self.points.max(axis=0) - self.points.min(axis=0)
            print(f"\n边界框大小:")
            print(f"  {bbox_size[0]:.4f} x {bbox_size[1]:.4f} x {bbox_size[2]:.4f}")

            centroid = self.points.mean(axis=0)
            print(f"\n质心位置:")
            print(f"  ({centroid[0]:.4f}, {centroid[1]:.4f}, {centroid[2]:.4f})")
        print("=" * 50 + "\n")

    def _build_o3d_pcd(self, color_mode='height'):
        """构建 Open3D PointCloud 对象"""
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(self.points)

        if color_mode == 'original' and self.colors is not None:
            pcd.colors = o3d.utility.Vector3dVector(
                np.clip(self.colors, 0, 1))
        elif color_mode == 'height':
            pcd.colors = o3d.utility.Vector3dVector(self._height_based_colors())
        else:
            pcd.colors = o3d.utility.Vector3dVector(np.random.rand(len(self.points), 3))

        return pcd

    def _build_coordinate_frame(self, origin=None, size=None):
        """构建自适应坐标轴，返回 (frame_mesh, tick_lineset) 元组"""
        if self.points is None:
            return o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0), None

        p_min = self.points.min(axis=0)
        p_max = self.points.max(axis=0)
        extent = p_max - p_min
        diag = np.linalg.norm(extent)

        if size is None:
            size = diag * 0.25
        if origin is None:
            origin = p_min

        frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=size)
        frame.translate(origin)

        # 在每个轴上添加刻度线
        n_ticks = 5
        tick_size = size * 0.05
        tick_points = []
        tick_lines = []
        tick_colors = []
        idx = 0

        axis_colors = {
            0: [1, 1, 1],       # X - 白色
            1: [0, 1, 0],       # Y - 绿色
            2: [0, 0.5, 1],     # Z - 蓝色
        }

        for i in range(n_ticks + 1):
            t = i / n_ticks
            for axis in range(3):
                tick_pos = origin.copy()
                tick_pos[axis] += size * t

                p1 = tick_pos.copy()
                p2 = tick_pos.copy()
                for other_axis in range(3):
                    if other_axis != axis:
                        p2[other_axis] += tick_size
                        break

                tick_points.append(p1)
                tick_points.append(p2)
                tick_lines.append([idx, idx + 1])
                tick_colors.append(axis_colors[axis])
                idx += 2

        tick_ls = o3d.geometry.LineSet()
        tick_ls.points = o3d.utility.Vector3dVector(np.array(tick_points))
        tick_ls.lines = o3d.utility.Vector2iVector(tick_lines)
        tick_ls.colors = o3d.utility.Vector3dVector(tick_colors)

        return frame, tick_ls

    def _build_bounding_box(self):
        """构建点云包围盒线框"""
        p_min = self.points.min(axis=0)
        p_max = self.points.max(axis=0)

        # 8个顶点
        corners = np.array([
            [p_min[0], p_min[1], p_min[2]],
            [p_max[0], p_min[1], p_min[2]],
            [p_max[0], p_max[1], p_min[2]],
            [p_min[0], p_max[1], p_min[2]],
            [p_min[0], p_min[1], p_max[2]],
            [p_max[0], p_min[1], p_max[2]],
            [p_max[0], p_max[1], p_max[2]],
            [p_min[0], p_max[1], p_max[2]],
        ])

        # 12条边
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # 底面
            [4, 5], [5, 6], [6, 7], [7, 4],  # 顶面
            [0, 4], [1, 5], [2, 6], [3, 7],  # 竖边
        ]

        bbox = o3d.geometry.LineSet()
        bbox.points = o3d.utility.Vector3dVector(corners)
        bbox.lines = o3d.utility.Vector2iVector(edges)
        bbox.colors = o3d.utility.Vector3dVector(
            [[0.5, 0.5, 0.5]] * len(edges))
        return bbox

    def _build_ground_grid(self, n_grid=11, color=(0.3, 0.3, 0.3)):
        """构建地面网格（XY平面）"""
        p_min = self.points.min(axis=0)
        p_max = self.points.max(axis=0)
        extent = p_max - p_min
        diag = np.linalg.norm(extent)
        half = diag * 0.6

        lines = []
        points = []
        idx = 0

        # X方向网格线
        for i in range(n_grid):
            t = -half + 2 * half * i / (n_grid - 1)
            points.append([t, -half, 0])
            points.append([t, half, 0])
            lines.append([idx, idx + 1])
            idx += 2

        # Y方向网格线
        for i in range(n_grid):
            t = -half + 2 * half * i / (n_grid - 1)
            points.append([-half, t, 0])
            points.append([half, t, 0])
            lines.append([idx, idx + 1])
            idx += 2

        grid = o3d.geometry.LineSet()
        grid.points = o3d.utility.Vector3dVector(np.array(points))
        grid.lines = o3d.utility.Vector2iVector(lines)
        grid.colors = o3d.utility.Vector3dVector([color] * len(lines))
        return grid

    def _build_axis_lines(self, length=None):
        """构建延长坐标轴线（穿过原点的 X/Y/Z 轴）"""
        if self.points is None:
            return o3d.geometry.LineSet()

        diag = np.linalg.norm(self.points.max(axis=0) - self.points.min(axis=0))
        if length is None:
            length = diag * 0.8

        points = np.array([
            [-length, 0, 0], [length, 0, 0],  # X轴 - 红
            [0, -length, 0], [0, length, 0],  # Y轴 - 绿
            [0, 0, -length], [0, 0, length],  # Z轴 - 蓝
        ])
        lines = [[0, 1], [2, 3], [4, 5]]
        colors = [[1, 0.3, 0.3], [0.3, 1, 0.3], [0.3, 0.3, 1]]

        axis_lines = o3d.geometry.LineSet()
        axis_lines.points = o3d.utility.Vector3dVector(points)
        axis_lines.lines = o3d.utility.Vector2iVector(lines)
        axis_lines.colors = o3d.utility.Vector3dVector(colors)
        return axis_lines

    def visualize(self, title="Point Cloud Viewer", point_size=2,
                  color_mode='height', show_axes=True, show_grid=True,
                  show_bbox=True, bg_color=(0.1, 0.1, 0.1)):
        """
        可视化点云

        Args:
            title: 窗口标题
            point_size: 点的大小
            color_mode: 颜色模式 ('height', 'original', 'random')
            show_axes: 是否显示坐标轴
            show_grid: 是否显示地面网格
            show_bbox: 是否显示包围盒
            bg_color: 背景颜色 (R, G, B)，范围 [0, 1]
        """
        if self.points is None:
            print("未加载点云，无法可视化")
            return

        pcd = self._build_o3d_pcd(color_mode=color_mode)

        p_min = self.points.min(axis=0)
        p_max = self.points.max(axis=0)
        extent = p_max - p_min
        diag = np.linalg.norm(extent)
        centroid = self.points.mean(axis=0)

        print("\n" + "-" * 50)
        print("辅助元素")
        print("-" * 50)

        if show_axes:
            frame_size = diag * 0.25
            print(f"  坐标轴 (RGB):")
            print(f"    X (红) 范围 [{p_min[0]:.3f}, {p_max[0]:.3f}], 轴长 {extent[0]:.3f}")
            print(f"    Y (绿) 范围 [{p_min[1]:.3f}, {p_max[1]:.3f}], 轴长 {extent[1]:.3f}")
            print(f"    Z (蓝) 范围 [{p_min[2]:.3f}, {p_max[2]:.3f}], 轴长 {extent[2]:.3f}")
            print(f"    原点位于: ({p_min[0]:.3f}, {p_min[1]:.3f}, {p_min[2]:.3f}), 标尺长度 {frame_size:.3f}")

        if show_bbox:
            print(f"  包围盒:")
            print(f"    Min: ({p_min[0]:.3f}, {p_min[1]:.3f}, {p_min[2]:.3f})")
            print(f"    Max: ({p_max[0]:.3f}, {p_max[1]:.3f}, {p_max[2]:.3f})")
            print(f"    尺寸: {extent[0]:.3f} x {extent[1]:.3f} x {extent[2]:.3f}")

        if show_grid:
            half = diag * 0.6
            step = 2 * half / 10
            print(f"  地面网格 (XY平面):")
            print(f"    范围 [{-half:.3f}, {half:.3f}] x [{-half:.3f}, {half:.3f}]")
            print(f"    网格间距: {step:.3f}, 共 11x11 条线")

        print(f"  质心: ({centroid[0]:.3f}, {centroid[1]:.3f}, {centroid[2]:.3f})")
        print(f"  对角线长度: {diag:.3f}")

        print("\n可视化控制说明:")
        print("  鼠标左键拖动: 旋转视角")
        print("  滚轮: 缩放")
        print("  Shift + 左键拖动: 平移")
        print("  按 ESC 或 Q: 退出")
        print("-" * 50 + "\n")

        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name=title, width=1280, height=960)
        vis.add_geometry(pcd)

        if show_axes:
            frame, ticks = self._build_coordinate_frame()
            vis.add_geometry(frame)
            if ticks is not None:
                vis.add_geometry(ticks)
            vis.add_geometry(self._build_axis_lines())

        if show_grid:
            vis.add_geometry(self._build_ground_grid())

        if show_bbox:
            vis.add_geometry(self._build_bounding_box())

        opt = vis.get_render_option()
        opt.point_size = point_size
        opt.background_color = np.array(bg_color)
        opt.light_on = True
        opt.show_coordinate_frame = False

        vis.run()
        vis.destroy_window()

    def visualize_multi_view(self, title="Point Cloud - Multi View"):
        """多视角可视化"""
        if self.points is None:
            print("未加载点云")
            return

        pcd = self._build_o3d_pcd(color_mode='height')

        views = [
            {"front": [0, 0, 1],   "lookat": [0, 0, 0], "up": [0, 1, 0], "zoom": 0.8,
             "name": "俯视图 (Top)"},
            {"front": [0, 0, -1],  "lookat": [0, 0, 0], "up": [0, 1, 0], "zoom": 0.8,
             "name": "仰视图 (Bottom)"},
            {"front": [1, 0, 0],   "lookat": [0, 0, 0], "up": [0, 1, 0], "zoom": 0.8,
             "name": "正视图 (Front)"},
            {"front": [0, 1, 0],   "lookat": [0, 0, 0], "up": [0, 0, 1], "zoom": 0.8,
             "name": "侧视图 (Side)"},
        ]

        for view in views:
            vis = o3d.visualization.Visualizer()
            vis.create_window(
                window_name=f"{title} - {view['name']}", width=640, height=480)
            vis.add_geometry(pcd)
            frame, ticks = self._build_coordinate_frame()
            vis.add_geometry(frame)
            if ticks is not None:
                vis.add_geometry(ticks)
            vis.add_geometry(self._build_axis_lines())
            vis.add_geometry(self._build_ground_grid())
            vis.add_geometry(self._build_bounding_box())

            opt = vis.get_render_option()
            opt.point_size = 2
            opt.background_color = np.array([0.1, 0.1, 0.1])

            ctr = vis.get_view_control()
            ctr.set_front(view["front"])
            ctr.set_lookat(view["lookat"])
            ctr.set_up(view["up"])
            ctr.set_zoom(view["zoom"])

            vis.run()
            vis.destroy_window()

    def load_multiple(self, file_paths):
        """
        加载多幅点云文件

        Args:
            file_paths: 点云文件路径列表

        Returns:
            list[bool]: 每个文件的加载结果
        """
        results = []
        for fp in file_paths:
            ok = self.load_point_cloud(fp)
            results.append(ok)
        print(f"\n共加载 {sum(results)}/{len(file_paths)} 幅点云")
        return results

    def add_cloud(self, name, points, colors=None):
        """
        手动添加一幅点云到列表

        Args:
            name: 点云名称
            points: Nx3 numpy 数组
            colors: Nx3 numpy 数组 (可选)
        """
        self.clouds.append({"name": name, "points": np.array(points),
                            "colors": np.array(colors) if colors is not None else None})
        print(f"添加点云: {name}, {len(points)} 个点")

    def visualize_multi_cloud(self, color_mode='palette', point_size=2,
                              show_axes=True, show_grid=True,
                              show_bbox=True, bg_color=(0.1, 0.1, 0.1),
                              title="Multi Cloud Viewer"):
        """
        在同一窗口中同时显示多幅点云

        Args:
            color_mode: 颜色模式
                'palette' - 每幅点云分配不同颜色
                'original' - 使用原始颜色
                'height' - 根据高度着色
            point_size: 点的大小
            show_axes: 是否显示坐标轴
            show_grid: 是否显示地面网格
            show_bbox: 是否显示每幅点云的包围盒
            bg_color: 背景颜色
            title: 窗口标题
        """
        if not self.clouds:
            print("未加载任何点云")
            return

        all_points = np.vstack([c["points"] for c in self.clouds])

        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name=title, width=1280, height=960)

        print("\n" + "-" * 50)
        print(f"多幅点云可视化 (共 {len(self.clouds)} 幅, "
              f"{len(all_points)} 个点)")
        print("-" * 50)

        for i, cloud in enumerate(self.clouds):
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(cloud["points"])

            if color_mode == 'palette':
                c = self.PALETTE[i % len(self.PALETTE)]
                pcd.colors = o3d.utility.Vector3dVector(
                    np.tile(c, (len(cloud["points"]), 1)))
            elif color_mode == 'original' and cloud["colors"] is not None:
                pcd.colors = o3d.utility.Vector3dVector(
                    np.clip(cloud["colors"], 0, 1))
            elif color_mode == 'height':
                z = cloud["points"][:, 2]
                z_norm = (z - z.min()) / (z.max() - z.min() + 1e-8)
                colors = np.zeros((len(cloud["points"]), 3))
                colors[:, 0] = z_norm
                colors[:, 2] = 1 - z_norm
                pcd.colors = o3d.utility.Vector3dVector(colors)
            else:
                pcd.colors = o3d.utility.Vector3dVector(
                    np.tile(self.PALETTE[i % len(self.PALETTE)],
                            (len(cloud["points"]), 1)))

            vis.add_geometry(pcd)

            # 每幅点云的信息
            p_min = cloud["points"].min(axis=0)
            p_max = cloud["points"].max(axis=0)
            extent = p_max - p_min
            label = self.PALETTE[i % len(self.PALETTE)]

            if color_mode == 'palette':
                mode_str = "palette"
            elif color_mode == 'original':
                mode_str = "original"
            else:
                mode_str = "height"

            print(f"  [{i}] {cloud['name']} ({len(cloud['points'])} 点)")
            print(f"      范围: X[{p_min[0]:.3f}, {p_max[0]:.3f}] "
                  f"Y[{p_min[1]:.3f}, {p_max[1]:.3f}] "
                  f"Z[{p_min[2]:.3f}, {p_max[2]:.3f}]")
            print(f"      尺寸: {extent[0]:.3f} x {extent[1]:.3f} x {extent[2]:.3f}")

            if color_mode == 'palette':
                print(f"      颜色: palette #{i} "
                      f"(R={label[0]:.1f} G={label[1]:.1f} B={label[2]:.1f})")

            # 单独的包围盒（颜色与调色板一致）
            if show_bbox:
                corners = np.array([
                    [p_min[0], p_min[1], p_min[2]],
                    [p_max[0], p_min[1], p_min[2]],
                    [p_max[0], p_max[1], p_min[2]],
                    [p_min[0], p_max[1], p_min[2]],
                    [p_min[0], p_min[1], p_max[2]],
                    [p_max[0], p_min[1], p_max[2]],
                    [p_max[0], p_max[1], p_max[2]],
                    [p_min[0], p_max[1], p_max[2]],
                ])
                edges = [
                    [0, 1], [1, 2], [2, 3], [3, 0],
                    [4, 5], [5, 6], [6, 7], [7, 4],
                    [0, 4], [1, 5], [2, 6], [3, 7],
                ]
                bbox = o3d.geometry.LineSet()
                bbox.points = o3d.utility.Vector3dVector(corners)
                bbox.lines = o3d.utility.Vector2iVector(edges)
                bbox.colors = o3d.utility.Vector3dVector(
                    np.tile(label, (len(edges), 1)))
                vis.add_geometry(bbox)

        # 全局辅助元素（基于所有点的合并范围）
        g_min = all_points.min(axis=0)
        g_max = all_points.max(axis=0)
        g_extent = g_max - g_min
        g_diag = np.linalg.norm(g_extent)
        g_centroid = all_points.mean(axis=0)

        if show_axes:
            frame_size = g_diag * 0.25
            frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
                size=frame_size)
            frame.translate(g_min)
            vis.add_geometry(frame)

            axis_length = g_diag * 0.8
            axis_pts = np.array([
                [-axis_length, 0, 0], [axis_length, 0, 0],
                [0, -axis_length, 0], [0, axis_length, 0],
                [0, 0, -axis_length], [0, 0, axis_length],
            ])
            axis_ls = o3d.geometry.LineSet()
            axis_ls.points = o3d.utility.Vector3dVector(axis_pts)
            axis_ls.lines = o3d.utility.Vector2iVector(
                [[0, 1], [2, 3], [4, 5]])
            axis_ls.colors = o3d.utility.Vector3dVector(
                [[1, 0.3, 0.3], [0.3, 1, 0.3], [0.3, 0.3, 1]])
            vis.add_geometry(axis_ls)

            print(f"\n  全局坐标轴 (RGB):")
            print(f"    X 范围 [{g_min[0]:.3f}, {g_max[0]:.3f}], 轴长 {g_extent[0]:.3f}")
            print(f"    Y 范围 [{g_min[1]:.3f}, {g_max[1]:.3f}], 轴长 {g_extent[1]:.3f}")
            print(f"    Z 范围 [{g_min[2]:.3f}, {g_max[2]:.3f}], 轴长 {g_extent[2]:.3f}")

        if show_grid:
            half = g_diag * 0.6
            grid_pts, grid_lines = [], []
            idx = 0
            for j in range(11):
                t = -half + 2 * half * j / 10
                grid_pts.extend([[t, -half, 0], [t, half, 0]])
                grid_lines.append([idx, idx + 1])
                idx += 2
                grid_pts.extend([[-half, t, 0], [half, t, 0]])
                grid_lines.append([idx, idx + 1])
                idx += 2
            grid = o3d.geometry.LineSet()
            grid.points = o3d.utility.Vector3dVector(np.array(grid_pts))
            grid.lines = o3d.utility.Vector2iVector(grid_lines)
            grid.colors = o3d.utility.Vector3dVector(
                [[0.3, 0.3, 0.3]] * len(grid_lines))
            vis.add_geometry(grid)

            step = 2 * half / 10
            print(f"  地面网格: [{-half:.3f}, {half:.3f}], 间距 {step:.3f}")

        print(f"  全局质心: ({g_centroid[0]:.3f}, {g_centroid[1]:.3f}, {g_centroid[2]:.3f})")
        print(f"  对角线长度: {g_diag:.3f}")

        print("\n可视化控制说明:")
        print("  鼠标左键拖动: 旋转视角")
        print("  滚轮: 缩放")
        print("  Shift + 左键拖动: 平移")
        print("  按 ESC 或 Q: 退出")
        print("-" * 50 + "\n")

        opt = vis.get_render_option()
        opt.point_size = point_size
        opt.background_color = np.array(bg_color)
        opt.light_on = True
        opt.show_coordinate_frame = False

        vis.run()
        vis.destroy_window()

    def save_xyz(self, output_path):
        """保存点云为XYZ格式"""
        if self.points is None:
            print("未加载点云")
            return False

        try:
            if self.colors is not None:
                data = np.hstack([self.points, self.colors])
            else:
                data = self.points
            np.savetxt(output_path, data, fmt='%.6f')
            print(f"点云已保存到: {output_path}")
            return True
        except Exception as e:
            print(f"保存失败: {e}")
            return False


def demo():
    """演示功能"""
    print("=" * 60)
    print("点云加载与可视化 Demo (Open3D)")
    print("=" * 60)

    viewer = PointCloudViewer()

    if len(sys.argv) > 1:
        file_paths = sys.argv[1:]
        if len(file_paths) == 1:
            viewer.load_point_cloud(file_paths[0])
            viewer.print_info()
            viewer.visualize(
                title=f"Point Cloud: {os.path.basename(file_paths[0])}")
        else:
            viewer.load_multiple(file_paths)
            viewer.visualize_multi_cloud(
                title="Multi Cloud: " + ", ".join(
                    os.path.basename(f) for f in file_paths))
    else:
        print("\n使用方法:")
        print("  python demo.py <文件1> [文件2] ...   # 同时查看多幅点云")
        print("  python demo.py                        # 演示模式")
        print()

        # 演示1: 单幅点云
        print("--- 演示1: 单幅球形点云 ---")
        viewer.create_random_point_cloud(n_points=3000, shape='sphere', radius=2.0)
        viewer.print_info()
        viewer.visualize(title="Demo: Sphere Point Cloud", point_size=5)

        # 演示2: 多视角
        print("\n--- 演示2: 多视角可视化 ---")
        viewer.clouds.clear()
        viewer.create_random_point_cloud(n_points=2000, shape='torus', radius=2.0)
        viewer.visualize_multi_view(title="Demo: Torus Point Cloud")

        # 演示3: 多幅点云同时显示
        print("\n--- 演示3: 多幅点云同时显示 ---")
        viewer.clouds.clear()
        viewer.create_random_point_cloud(n_points=1500, shape='sphere',
                                         center=(-4, 0, 0), radius=1.5)
        viewer.create_random_point_cloud(n_points=1500, shape='cube',
                                         center=(0, 0, 0), radius=1.5)
        viewer.create_random_point_cloud(n_points=1500, shape='torus',
                                         center=(4, 0, 0), radius=1.5)
        viewer.visualize_multi_cloud(color_mode='palette', point_size=4,
                                     title="Demo: Multi Cloud")


if __name__ == "__main__":
    demo()
