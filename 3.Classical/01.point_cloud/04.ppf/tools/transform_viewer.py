#!/usr/bin/env python
#########################################################################
# File Name: viewer_conv.py
# Author: LiHongjin
# mail: 872648180@qq.com
# Created Time: Mon 01 Dec 2025 10:02:38 PM CST
#########################################################################


import argparse
import open3d as o3d
import numpy as np
import os
import sys
from open3d.visualization import gui, rendering


# ============================================================
# Safe clone for old Open3D versions
# ============================================================
def safe_clone(pcd):
    if hasattr(pcd, "clone"):
        return pcd.clone()

    new_pcd = o3d.geometry.PointCloud()
    if pcd.has_points():
        new_pcd.points = o3d.utility.Vector3dVector(np.asarray(pcd.points))
    if pcd.has_colors():
        new_pcd.colors = o3d.utility.Vector3dVector(np.asarray(pcd.colors))
    if pcd.has_normals():
        new_pcd.normals = o3d.utility.Vector3dVector(np.asarray(pcd.normals))
    return new_pcd


# ============================================================
# Auto load point cloud based on file extension
# ============================================================
def load_point_cloud_auto(path):
    if not os.path.exists(path):
        print(f"[ERROR] File not found: {path}")
        sys.exit(1)

    ext = os.path.splitext(path)[1].lower()

    if ext in [".ply", ".pcd", ".xyz", ".xyzn", ".xyzrgb", ".pts"]:
        print(f"[INFO] Loading point cloud with Open3D: {path}")
        pcd = o3d.io.read_point_cloud(path)
        if pcd.is_empty():
            print("[ERROR] Point cloud is empty or invalid format")
            sys.exit(1)
        return pcd

    elif ext in [".txt", ".csv"]:
        print(f"[INFO] Loading text point cloud: {path}")
        data = np.loadtxt(path)
        if data.shape[1] < 3:
            print("[ERROR] Text point cloud must have at least XYZ columns")
            sys.exit(1)

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(data[:, :3])

        if data.shape[1] >= 6:
            colors = data[:, 3:6]
            if colors.max() > 1.0:
                colors /= 255.0
            pcd.colors = o3d.utility.Vector3dVector(colors)
        return pcd

    print(f"[ERROR] Unsupported input format: {ext}")
    sys.exit(1)


# ============================================================
# Safe redraw for different backends
# ============================================================
def safe_redraw(widget):
    try:
        widget.force_redraw()    # New SceneWidget
    except:
        try:
            widget.scene.force_redraw()  # GPU backend
        except:
            pass


# ============================================================
# Transform Viewer Class
# ============================================================
class TransformViewer:
    def __init__(self, file1, file2):
        self.pcd1 = load_point_cloud_auto(file1)
        self.pcd2_orig = load_point_cloud_auto(file2)
        self.pcd2 = safe_clone(self.pcd2_orig)

        self.normalize_point_clouds()

        gui.Application.instance.initialize()
        self.window = gui.Application.instance.create_window(
            "PointCloud Transform Viewer", 1280, 720
        )

        # SceneWidget
        self.scene = gui.SceneWidget()
        self.scene.scene = rendering.Open3DScene(self.window.renderer)

        # Material
        self.mat = rendering.MaterialRecord()
        self.mat.shader = "defaultUnlit"
        self.mat.point_size = 5.0

        # Add coordinate frame
        axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.2)
        self.scene.scene.add_geometry("axis", axis, self.mat)

        # Add point clouds
        self.scene.scene.add_geometry("pcd1", self.pcd1, self.mat)
        self.scene.scene.add_geometry("pcd2", self.pcd2, self.mat)

        # Black background and camera
        self.scene.scene.set_background([0.0, 0.0, 0.0, 1.0])
        bbox = self.pcd1.get_axis_aligned_bounding_box()
        self.scene.setup_camera(60, bbox, bbox.get_center() + np.array([0, 0, 2]))
        safe_redraw(self.scene)

        # UI panel
        self.panel = gui.Vert(10, gui.Margins(10))
        self.add_sliders()
        self.add_buttons()
        self.add_style_controls()

        # Layout
        self.window.set_on_layout(self.on_layout)
        self.window.add_child(self.scene)
        self.window.add_child(self.panel)

    # ------------------------------------------------------------
    def normalize_point_clouds(self):
        """Auto scale point clouds to fit the view"""
        pts = np.vstack((np.asarray(self.pcd1.points),
                         np.asarray(self.pcd2.points)))

        max_range = np.ptp(pts, axis=0).max()
        scale = 1.0 / max_range

        self.pcd1.scale(scale, center=(0, 0, 0))
        self.pcd2_orig.scale(scale, center=(0, 0, 0))
        self.pcd2 = safe_clone(self.pcd2_orig)

    # ------------------------------------------------------------
    def add_sliders(self):
        def slider(name, minv, maxv, cb):
            label = gui.Label(name)
            s = gui.Slider(gui.Slider.DOUBLE)
            s.set_limits(minv, maxv)
            s.set_on_value_changed(cb)
            self.panel.add_child(label)
            self.panel.add_child(s)
            return s

        self.rx = slider("Rotate X", -180, 180, self.on_transform)
        self.ry = slider("Rotate Y", -180, 180, self.on_transform)
        self.rz = slider("Rotate Z", -180, 180, self.on_transform)
        self.tx = slider("Translate X", -1.0, 1.0, self.on_transform)
        self.ty = slider("Translate Y", -1.0, 1.0, self.on_transform)
        self.tz = slider("Translate Z", -1.0, 1.0, self.on_transform)

    # ------------------------------------------------------------
    def add_buttons(self):
        btn_reset = gui.Button("Reset Transform")
        btn_reset.set_on_clicked(self.reset_transform)
        self.panel.add_child(btn_reset)

        btn_save = gui.Button("Save Transformed PointCloud")
        btn_save.set_on_clicked(self.save_transformed)
        self.panel.add_child(btn_save)

        btn_print = gui.Button("Print Transform Matrix")
        btn_print.set_on_clicked(self.print_matrix)
        self.panel.add_child(btn_print)

    # ------------------------------------------------------------
    def add_style_controls(self):
        label = gui.Label("Point Size")
        self.point_size_slider = gui.Slider(gui.Slider.DOUBLE)
        self.point_size_slider.set_limits(1, 15)
        self.point_size_slider.set_on_value_changed(self.change_style)
        self.point_size_slider.double_value = 5

        self.panel.add_child(label)
        self.panel.add_child(self.point_size_slider)

    # ------------------------------------------------------------
    def on_layout(self, layout_context):
        r = self.window.content_rect
        self.scene.frame = gui.Rect(r.x, r.y, r.width - 250, r.height)
        self.panel.frame = gui.Rect(r.get_right() - 240, r.y, 240, r.height)

    # ------------------------------------------------------------
    def on_transform(self, value):
        rx = np.radians(self.rx.double_value)
        ry = np.radians(self.ry.double_value)
        rz = np.radians(self.rz.double_value)

        R = self.Rz(rz) @ self.Ry(ry) @ self.Rx(rx)
        t = np.array([self.tx.double_value,
                      self.ty.double_value,
                      self.tz.double_value])

        self.pcd2 = safe_clone(self.pcd2_orig)
        self.pcd2.rotate(R, center=(0, 0, 0))
        self.pcd2.translate(t)

        self.scene.scene.remove_geometry("pcd2")
        self.scene.scene.add_geometry("pcd2", self.pcd2, self.mat)
        safe_redraw(self.scene)

    # ------------------------------------------------------------
    def reset_transform(self):
        self.pcd2 = safe_clone(self.pcd2_orig)
        self.scene.scene.remove_geometry("pcd2")
        self.scene.scene.add_geometry("pcd2", self.pcd2, self.mat)
        safe_redraw(self.scene)

    # ------------------------------------------------------------
    def change_style(self, value):
        self.mat.point_size = value
        self.scene.scene.modify_geometry_material("pcd1", self.mat)
        self.scene.scene.modify_geometry_material("pcd2", self.mat)
        safe_redraw(self.scene)

    # ------------------------------------------------------------
    def save_transformed(self):
        o3d.io.write_point_cloud("transformed.ply", self.pcd2)
        print("[INFO] Saved: transformed.ply")

    # ------------------------------------------------------------
    def print_matrix(self):
        rx = np.radians(self.rx.double_value)
        ry = np.radians(self.ry.double_value)
        rz = np.radians(self.rz.double_value)
        R = self.Rz(rz) @ self.Ry(ry) @ self.Rx(rx)
        t = np.array([self.tx.double_value,
                      self.ty.double_value,
                      self.tz.double_value])
        print("Rotation matrix R =\n", R)
        print("Translation t = ", t)

    # ------------------------------------------------------------
    @staticmethod
    def Rx(a):
        return np.array([[1, 0, 0],
                         [0, np.cos(a), -np.sin(a)],
                         [0, np.sin(a), np.cos(a)]])

    @staticmethod
    def Ry(a):
        return np.array([[np.cos(a), 0, np.sin(a)],
                         [0, 1, 0],
                         [-np.sin(a), 0, np.cos(a)]])

    @staticmethod
    def Rz(a):
        return np.array([[np.cos(a), -np.sin(a), 0],
                         [np.sin(a), np.cos(a), 0],
                         [0, 0, 1]])


# ============================================================
# Main entry
# ============================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", nargs=2, required=True,
                        help="Two input point cloud files")
    args = parser.parse_args()

    viewer = TransformViewer(args.input[0], args.input[1])
    gui.Application.instance.run()

