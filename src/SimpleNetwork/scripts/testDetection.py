#!/home/archiconda3/envs/apple/bin/python3.8
# -*- coding: utf-8 -*-
"""
AUTHOR: Luo Hefei
Copyright (C) 2023, Luo Hefei. All right reserved.
"""

import cv2
import rospy
import time
import rosparam
import warnings
import ultralytics
import numpy as np
import pyrealsense2 as rs
from sensor_msgs.msg import CompressedImage
from utils.PickSequence import sort_sequence

from scipy.spatial import KDTree
from scipy.ndimage import gaussian_filter

def voxel_downsample(pointcloud, voxel_size=5):
    """
    :param pointcloud: 输入点云(numpy数组，shape=(N,3))
    :param voxel_size: 体素大小(毫米)
    :return: 下采样后的点云
    """
    if len(pointcloud) == 0:
        return np.array([])
    
    # 计算每个点所属的体素索引
    voxel_indices = np.floor(pointcloud / voxel_size).astype(int)
    
    # 按体素分组，计算每个体素的平均点
    unique_voxels, voxel_counts = np.unique(voxel_indices, axis=0, return_counts=True)
    downsampled = []
    for voxel in unique_voxels:
        mask = np.all(voxel_indices == voxel, axis=1)
        voxel_points = pointcloud[mask]
        downsampled.append(np.mean(voxel_points, axis=0))  # 体素内取平均
    
    return np.array(downsampled)


def statistical_outlier_removal(pointcloud, k=8, std_ratio=1.0):
    """
    :param pointcloud: 输入点云(numpy数组，shape=(N,3))
    :param k: 邻域点数量
    :param std_ratio: 标准差倍数阈值
    :return: 去除离群点后的点云
    """
    if len(pointcloud) <= k:
        return pointcloud  # 点数量不足时直接返回
    
    # 构建KDTree计算最近邻
    tree = KDTree(pointcloud)
    distances, _ = tree.query(pointcloud, k=k+1)  # 第0个是自身，取k+1个后排除自身
    mean_distances = np.mean(distances[:, 1:], axis=1)  # 计算每个点到k个邻域的平均距离
    
    # 计算距离的均值和标准差，确定阈值
    mean = np.mean(mean_distances)
    std = np.std(mean_distances)
    threshold = mean + std_ratio * std
    
    # 保留平均距离小于阈值的点
    inliers = pointcloud[mean_distances < threshold]
    return inliers


def get_mid_pos(aligned_depth_frame, x1, y1, x2, y2):
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
    depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
    
    # 计算锚框中心点
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    
    # 定义50×50区域（中心±25像素）并限制在图像内
    width = aligned_depth_frame.get_width()
    height = aligned_depth_frame.get_height()
    x_start = max(0, cx - 25)
    x_end = min(width - 1, cx + 24)
    y_start = max(0, cy - 25)
    y_end = min(height - 1, cy + 24)
    
    # 收集50×50区域内的有效深度点（单位：毫米）
    points = []
    for y in range(y_start, y_end + 1):
        for x in range(x_start, x_end + 1):
            dis = aligned_depth_frame.get_distance(x, y)  # 米
            if dis != 0:
                coord = rs.rs2_deproject_pixel_to_point(depth_intrin, [x, y], dis)
                points.append([int(c * 1000) for c in coord])  # 转换为毫米
    
    if not points:
        print("50×50区域内无有效深度数据")
        return None
    
    pointcloud = np.array(points)
    
    # 1. 体素下采样：减少点数量，保留结构
    downsampled = voxel_downsample(pointcloud, voxel_size=5)
    if len(downsampled) == 0:
        print("体素下采样后无有效点")
        return None
    
    # 2. 统计离群点去除：剔除噪声点
    filtered = statistical_outlier_removal(downsampled, k=8, std_ratio=1.0)
    if len(filtered) == 0:
        print("离群点去除后无有效点")
        return None
    
    # 3. 平滑处理：高斯滤波减少局部波动
    smoothed_x = gaussian_filter(filtered[:, 0], sigma=1)
    smoothed_y = gaussian_filter(filtered[:, 1], sigma=1)
    smoothed_z = gaussian_filter(filtered[:, 2], sigma=1)
    smoothed = np.column_stack((smoothed_x, smoothed_y, smoothed_z))
    
    # 计算预处理后的平均点
    average_point = np.mean(smoothed, axis=0)
    
    return average_point if average_point[2] != 0 else None

    
def draw_detections(img, objects, class_name, color = (255, 0, 0)):
    for info in objects:
        box = info[:4]
        score = info[4]
        depth = info[5][2]
        # Extract the coordinates of the bounding box
        x1, y1, w, h = box
        # Draw the bounding box on the image
        cv2.rectangle(img, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)
        # Create the label text with class name and score
        label = f'{class_name}: {score:.2f},{depth:.4f}'
        # Calculate the dimensions of the label text
        (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        # Calculate the position of the label text
        label_x = int(x1)
        label_y = int(y1 - 10) if y1 - 10 > label_height else int(y1 + 10)
        # Draw a filled rectangle as the background for the label text
        cv2.rectangle(img, (label_x, label_y - label_height), (label_x + label_width, label_y + label_height), color, cv2.FILLED)
        # Draw the label text on the image
        cv2.putText(img, label, (label_x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    return img


def boxes_filter(coords, confidences, depth_frame, threshold):
    result = []
    margin, ratio = threshold
    objects = np.concatenate((coords, np.expand_dims(confidences, axis=1)), axis=1)
    for info in objects:
        x1, y1, x2, y2, score = info
        w = x2 - x1
        h = y2 - y1
        width = rosparam.get_param('/image_width')
        height = rosparam.get_param('/image_height')
        if x1 < margin or y1 < margin or width - x2 < margin or height - y2 < margin:
            pass
        else:
            if max([w / h, h / w]) <= ratio:
                # center = [x1 + w / 2, y1 + h / 2]
                point = get_mid_pos(depth_frame, x1, y1, x2, y2)
                result.append([x1, y1, w, h, score, point])
    return result



if __name__ == "__main__":
    # Preparing
    warnings.filterwarnings("ignore")
    # Create an instance of the model
    # /home/liancheng/Desktop/best40.engine
    # /home/liancheng/Desktop/robot/src/SimpleNetwork/scripts/models/yolov10n.engine
    detection = ultralytics.YOLO('/home/liancheng/Desktop/robot/src/SimpleNetwork/scripts/models/yolov10n_1101.engine', task='detect')
    # Getdown parameter from ROS
    image_width = 640
    image_height = 480
    fps = 30
    conf = 0.4
    iou = 0.4
    box_thr = [0, 1.5]
    classes = [ 'apple' ]
    # Init a pipeline of RealSense
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, image_width, image_height, rs.format.z16, fps)
    config.enable_stream(rs.stream.color, image_width, image_height, rs.format.bgr8, fps)
    
    decimation = rs.decimation_filter()
    spatial = rs.spatial_filter()
    temporal = rs.temporal_filter()
    hole_filling = rs.hole_filling_filter()
    depth_to_disparity = rs.disparity_transform(True)
    disparity_to_depth = rs.disparity_transform(False)

    profile = pipeline.start(config)
        # device = profile.get_device()
        # sensor = device.query_sensors()[1]
        # sensor.set_option(rs.option.white_balance, 4600)
    align = rs.align(rs.stream.color)
    frame_pass = 0
    while(1):
        rospy.sleep(0.01)
        
        # Align all sensors frame to color frame
        frames = []
        for x in range(5):
            frameset = pipeline.wait_for_frames()
            frameset = align.process(frameset)
            color_frame = frameset.get_color_frame()
            depth_frame = frameset.get_depth_frame()
            frames.append(depth_frame)
        for x in range(5):
            frame = frames[x]
            # 降采样滤波器，卷积核[2x2] to [8x8] pixels，采用核内深度中值作为当前值，会降低分辨率
            # frame = decimation.process(frame)
            frame = depth_to_disparity.process(frame)
            # 空间滤波器，保证边缘信息对深度值进行平滑
            frame = spatial.process(frame)
            # 时间滤波器，利用不同时间帧图像融合
            frame = temporal.process(frame)
            frame = disparity_to_depth.process(frame)
            # frame = hole_filling.process(frame)

        # Validate that both frames are valid
        if not frame or not color_frame:
            continue
        
        # Start the detecting process
        # Loading images 
        # frames = pipeline.wait_for_frames()
        # aligned_frames = align.process(frames)
        # depth_frame = aligned_frames.get_depth_frame()
        # color_frame = aligned_frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data(), dtype=np.uint8)
        
        # Perform object detection, apples harvesting and obtain the output image
        results = detection.predict(color_image, imgsz=640, device='cuda:0', conf=conf, iou=iou, augment=True, agnostic_nms=True)    
        apples = boxes_filter(np.array(results[0].boxes.xyxy.cpu()), np.array(results[0].boxes.conf.cpu()), depth_frame, box_thr)
        if len(apples) > 0:
            color_image = draw_detections(color_image, apples, classes[0], color=[0, 0, 255])
        # Publish detection results
        cv2.imshow('Output', color_image)
        rospy.loginfo("Publsh compressed image!")
        # Wait for a key press to exit
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            pipeline.stop()
            break

