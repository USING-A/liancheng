#!/root/archiconda3/envs/apple/bin/python3.8
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



def get_mid_pos(aligned_depth_frame, mid_pixel):
    [x, y] = map(int, mid_pixel)
    # Approch the depth intrinsics of the camera
    depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
    # Get the depth of the pixel, unit: m
    dis = aligned_depth_frame.get_distance(x, y)
    # Get the coordinate of the pixel in the camera coordinate
    camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, [x, y], dis)
    camera_coordinate = [int(i * 1000) for i in camera_coordinate]
    if dis != 0:
        return camera_coordinate, dis
    else:
        return None, None
   
def draw_detections(img, objects, class_name, color = (255, 0, 0)):
    for info in objects:
        box = info[:4]
        score = info[4]
        # Extract the coordinates of the bounding box
        x1, y1, w, h = box
        # Draw the bounding box on the image
        cv2.rectangle(img, (int(x1), int(y1)), (int(x1 + w), int(y1 + h)), color, 2)
        # Create the label text with class name and score
        label = f'{class_name}: {score:.2f}'
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
        width = 640
        height = 480
        if x1 < margin or y1 < margin or width - x2 < margin or height - y2 < margin:
            pass
        else:
            if max([w / h, h / w]) <= ratio:
                center = [x1 + w / 2, y1 + h / 2]
                point, _ = get_mid_pos(depth_frame, center)
                result.append([x1, y1, w, h, score, point])
    return result


if __name__ == "__main__":
    # Preparing
    warnings.filterwarnings("ignore")
    # Create an instance of the model
    # /home/liancheng/Desktop/best40.engine
    # /home/liancheng/Desktop/robot/src/SimpleNetwork/scripts/models/yolov10n.engine
    detection = ultralytics.YOLO('/home/liancheng/Desktop/robot/src/SimpleNetwork/scripts/models/best40.engine', task='detect')
    # Getdown parameter from ROS
    image_width = 640
    image_height = 480
    fps = 30
    conf = 0.7
    iou = 0.7
    box_thr = [0, 1.5]
    classes = [ 'apple' ]
    # Init a pipeline of RealSense
    while(1):
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, image_width, image_height, rs.format.z16, fps)
        config.enable_stream(rs.stream.color, image_width, image_height, rs.format.bgr8, fps)
        profile = pipeline.start(config)
        device = profile.get_device()
        sensor = device.query_sensors()[1]
        sensor.set_option(rs.option.white_balance, 4600)
        align = rs.align(rs.stream.color)
        frame_pass = 0
        # Start the detecting process
        # Loading images 
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data(), dtype=np.uint8)
        # b,g,r = color_image[:,:,0],color_image[:,:,1],color_image[:,:,2]
        # color_image = np.stack((r,g,b), axis=-1)
        
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

