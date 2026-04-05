#!/usr/bin/env python
#########################################################################
# File Name: pointcloud_viewer.py
# Author: LiHongjin
# mail: 872648180@qq.com
# Created Time: Mon 01 Dec 2025 09:25:59 PM CST
#########################################################################

import argparse
import open3d as o3d
import numpy as np
import os
import sys


# ---------------------------------------------------------
# 工具函数：安全克隆（兼容旧版 Open3D）
# ---------------------------------------------------------
def safe_clone(pcd):
    if hasattr(pcd, "clone"):  # 新版本 Open3D
        return pcd.clone()
    else:  # 旧版本：手动构造
        new_pcd = o3d.geometry.PointCloud()
        if pcd.has_points():
            new_pcd.points = o3d.utility.Vector3dVector(np.asarray(pcd.points))
        if pcd.has_colors():
            new_pcd.colors = o3d.utility.Vector3dVector(np.asarray(pcd.colors))
        if pcd.has_normals():
            new_pcd.normals = o3d.utility.Vector3dVector(np.asarray(pcd.normals))
        return new_pcd


# ---------------------------------------------------------
# 加载点云
# ---------------------------------------------------------
def load_point_cloud_auto(path):
    if not os.path.exists(path):
        print(f"[ERROR] 文件不存在：{path}")
        sys.exit(1)

    ext = os.path.splitext(path)[1].lower()

    # Open3D 支持的格式
    if ext in [".pcd", ".ply", ".xyz", ".xyzn", ".xyzrgb", ".pts"]:
        print(f"[INFO] 使用 Open3D 加载：{path}")
        pcd = o3d.io.read_point_cloud(path)

        if pcd.is_empty():
            print("[ERROR] 文件存在，但读取点云为空！可能是文件损坏或格式不标准。")
            sys.exit(1)

        return pcd

    # 文本格式
    elif ext in [".txt", ".csv"]:
        print(f"[INFO] 加载文本点云：{path}")
        data = np.loadtxt(path)

        if data.shape[1] < 3:
            print("[ERROR] 文本文件 XYZ 列不足 3 列")
            sys.exit(1)

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(data[:, :3])

        if data.shape[1] >= 6:
            colors = data[:, 3:6]
            if colors.max() > 1.0:
                colors /= 255.0
            pcd.colors = o3d.utility.Vector3dVector(colors)

        return pcd

    else:
        print(f"[ERROR] 不支持的格式：{ext}")
        sys.exit(1)


# ---------------------------------------------------------
# 点云预处理
# ---------------------------------------------------------
def preprocess_point_cloud(pcd, voxel_size=None, estimate_normal=False):
    if pcd.is_empty():
        print("[ERROR] 空点云，无法处理")
        sys.exit(1)

    # 下采样
    if voxel_size:
        print(f"[INFO] 下采样：voxel_size = {voxel_size}")
        pcd = pcd.voxel_down_sample(voxel_size=voxel_size)

    # 法向量
    if estimate_normal:
        print("[INFO] 估计法向量...")
        pcd.estimate_normals(
            search_param=o3d.geometry.KDTreeSearchParamHybrid(
                radius=0.5, max_nn=30
            )
        )

    return pcd


# ---------------------------------------------------------
# 上色
# ---------------------------------------------------------
def colorize_point_cloud(pcd, mode="none"):
    if mode == "none":
        return pcd

    pcd = safe_clone(pcd)
    pts = np.asarray(pcd.points)

    # 按高度上色
    if mode == "height":
        z = pts[:, 2]
        z_norm = (z - z.min()) / (z.max() - z.min())
        colors = np.stack([z_norm, 1 - z_norm, 0.5 * np.ones_like(z_norm)], axis=1)
        pcd.colors = o3d.utility.Vector3dVector(colors)

    # 按法线方向上色
    elif mode == "normal":
        if not pcd.has_normals():
            print("[ERROR] 没有法向量，无法 normal 着色！请开启 estimate_normal=True")
            sys.exit(1)

        pcd.colors = o3d.utility.Vector3dVector(
            (np.asarray(pcd.normals) + 1) / 2
        )

    return pcd


# ---------------------------------------------------------
# 显示多个点云
# ---------------------------------------------------------
def show_point_clouds(pcd_list):
    print("[INFO] 显示多个点云...")
    o3d.visualization.draw_geometries(pcd_list)


# ---------------------------------------------------------
# 命令行参数处理（支持多文件）
# ---------------------------------------------------------
def proc_paras():
    parser = argparse.ArgumentParser(description="multiple point cloud viewer")
    parser.add_argument(
        "-i", "--input", nargs="+", help="input point cloud files", required=True
    )
    return parser.parse_args()


# ---------------------------------------------------------
# 主程序
# ---------------------------------------------------------
if __name__ == "__main__":
    args = proc_paras()

    pcd_list = []

    for path in args.input:
        print(f"[INFO] 正在加载：{path}")

        pcd = load_point_cloud_auto(path)

        pcd = preprocess_point_cloud(
            pcd,
            voxel_size=0.01,
            estimate_normal=True
        )

        pcd = colorize_point_cloud(
            pcd,
            mode="height"
        )

        pcd_list.append(pcd)

    # 显示多个点云
    show_point_clouds(pcd_list)

