#!/root/archiconda3/envs/apple/bin/python
# -*- coding: utf-8 -*-
"""
AUTHOR: Luo Hefei
Copyright (C) 2023, Luo Hefei. All right reserved.
"""

import argparse
import datetime
import json
import os
import cv2
import numpy as np
import pyrealsense2 as rs
import open3d as o3d


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default='', help="images save path")
    parser.add_argument("--mode", type=int, default=1, help="0(auto) or 1(manual)")
    parser.add_argument("--image_format", type=int, default=0, help="option: 0->jpg 1->png")
    parser.add_argument("--image_width", type=int, default=640, help="width of the image, recommended 1280 or 640")
    parser.add_argument("--image_height", type=int, default=480, help="height of the image, recommended 720 or 480")
    parser.add_argument("--choose_pc", type=bool, default=False, help="whether to save point cloud")
    parser.add_argument("--show_pc", type=bool, default=False, help="whether to save point cloud")
    parser.add_argument("--fps", type=int, default=30, help="frame rate of shooting")
    opt = parser.parse_args()
    return opt


# 创建图像文件夹
def mkdir_images(opt):
    now = datetime.datetime.now()
    n = 0
    if os.path.exists(os.path.join(opt.path, 'images')):
        dirname = opt.path
        if len(os.listdir(os.path.join(opt.path, 'images'))):
            li = sorted(os.listdir(os.path.join(opt.path, 'images')), key=lambda x: eval(x.split('.')[0]))
            n = eval(li[-1].split('.')[0])
    elif opt.path == '':
        dirname = os.path.join(r'./', now.strftime("%Y_%m_%d_%H_%M_%S"))
    else:
        dirname = os.path.join(opt.path)
    color_dir = os.path.join(dirname, 'Color')
    depth_dir = os.path.join(dirname, 'Depth')
    depth_color_dir = os.path.join(dirname, 'DepthColormap')
    depth_npy_dir = os.path.join(dirname, 'DepthNpy')
    point_cloud_dir = os.path.join(dirname, 'PointCloud')
    if not os.path.exists(dirname):
        os.mkdir(dirname)
        os.mkdir(color_dir)
        os.mkdir(depth_dir)
        os.mkdir(depth_color_dir)
        os.mkdir(depth_npy_dir)
        if opt.choose_pc:
            os.mkdir(point_cloud_dir)
    return color_dir, depth_dir, depth_color_dir, depth_npy_dir, point_cloud_dir, dirname, n


def show_result(depth_rgb, rgb, n):
    global opt
    depth_colormap_dim = depth_rgb.shape
    color_colormap_dim = rgb.shape
    if depth_colormap_dim != color_colormap_dim:
        resized_color_image = cv2.resize(rgb, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]),
                                         interpolation=cv2.INTER_AREA)
    else:
        resized_color_image = rgb
    color = cv2.resize(resized_color_image, (depth_colormap_dim[1] // 2, depth_colormap_dim[0] // 2))
    color_depth = cv2.resize(depth_rgb, (depth_colormap_dim[1] // 2, depth_colormap_dim[0] // 2))
    images = np.vstack((color, color_depth))
    if n:
        cv2.putText(images, '{}{} is saved!'.format(n, image_formats[opt.image_format]), (20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.imshow('IntelRealsense', images)


def save_data(rgb, depth, depth_rgb, aligned_frames, intr):
    global color_dir, depth_dir, depth_color_dir, depth_npy_dir, point_cloud_dir, dirname, opt
    cv2.imwrite(os.path.join(color_dir, str(n) + image_formats[opt.image_format]), rgb)
    cv2.imwrite(os.path.join(depth_dir, str(n) + image_formats[opt.image_format]), depth)
    cv2.imwrite(os.path.join(depth_color_dir, str(n) + image_formats[opt.image_format]), depth_rgb)
    np.save(os.path.join(depth_npy_dir, str(n)), depth)
    camera_parameters = {'fx': intr.fx, 'fy': intr.fy,
                         'ppx': intr.ppx, 'ppy': intr.ppy,
                         'height': intr.height, 'width': intr.width,
                         'depth_scale': profile.get_device().first_depth_sensor().get_depth_scale()}
    # 保存json文件
    with open(os.path.join(dirname, 'intrinsics.json'), 'w') as fp:
        json.dump(camera_parameters, fp)
    if opt.choose_pc:
        depth_frame = aligned_frames.get_depth_frame()
        pc = rs.pointcloud()
        points = pc.calculate(depth_frame)
        points.export_to_ply(os.path.join(point_cloud_dir, str(n)) + '.ply', depth_frame)


def showPoints(color_image, depth_image, cameraParam, vis):
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(o3d.geometry.Image(color_image),
                                                                    o3d.geometry.Image(depth_image))
    camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(cameraParam.width, cameraParam.height,
                                                         cameraParam.fx, cameraParam.fy,
                                                         cameraParam.ppx, cameraParam.ppy)
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, camera_intrinsic)
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    pcd.scale(10, center=pcd.get_center())
    vis.clear_geometries()
    vis.add_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()


if __name__ == "__main__":
    opt = parse_opt()
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, opt.image_width, opt.image_height, rs.format.z16, opt.fps)
    config.enable_stream(rs.stream.color, opt.image_width, opt.image_height, rs.format.bgr8, opt.fps)
    profile = pipeline.start(config)
    align = rs.align(rs.stream.color)
    color_dir, depth_dir, depth_color_dir, depth_npy_dir, point_cloud_dir, dirname, n = mkdir_images(opt)
    flag = 0
    image_formats = ['.jpg', '.png']
    if opt.show_pc:
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name='IntelRealsense')
        vis.get_view_control().scale(20)
    while True:
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        intr = color_frame.profile.as_video_stream_profile().intrinsics
        rgb = np.asanyarray(color_frame.get_data(), dtype=np.uint8)
        depth = np.asanyarray(depth_frame.get_data(), dtype=np.float32)
        depth_rgb = cv2.applyColorMap(cv2.convertScaleAbs(depth, alpha=0.03), cv2.COLORMAP_JET)
        show_result(depth_rgb, rgb, n)
        if opt.show_pc:
            showPoints(rgb, depth, intr, vis)
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            pipeline.stop()
            break
        elif opt.mode:
            if key == ord('s') or key == ord('S'):
                n = n + 1
                save_data(rgb, depth, depth_rgb, aligned_frames, intr)
        else:
            if key == ord('s') or key == ord('S'):
                flag = 1
            if key == ord('w') or key == ord('W'):
                flag = 0
            if flag:
                n = n + 1
                save_data(rgb, depth, depth_rgb, aligned_frames, intr)