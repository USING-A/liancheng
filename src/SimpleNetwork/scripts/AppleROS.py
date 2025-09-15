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
import utils.ROSPublisher as RP
import utils.RobotMovement as RM
from utils.RobotMovement import LianChengRobot
from liancheng_socket.msg import MotorOrder, SwitchOrder
from utils.PickSequence import sort_sequence


def get_mid_pos(aligned_depth_frame, mid_pixel):
    [x, y] = map(int, mid_pixel)
    # Approch the depth intrinsics of the camera
    depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
    # Get the depth of the pixel, unit: m
    # Get the coordinate of the pixel in the camera coordinate
    points = []
    for i in range(5):
        for j in range(5):
            if aligned_depth_frame.get_distance(x + i - 2, y + j - 2) != 0:
                dis = aligned_depth_frame.get_distance(x + i - 2, y + j - 2)
                camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, [x + i - 2, y + j - 2], dis)
                camera_coordinate = [int(i * 1000) for i in camera_coordinate]
                
                points.append(camera_coordinate)
    if not points:
        print("未检测到有效点云数据")
        return None
            
    pointcloud = np.array(points)
    average_point = np.mean(pointcloud, axis=0)
    
    if average_point[2] != 0:
        return average_point
    else:
        return None
    
    
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
        width = rosparam.get_param('/image_width')
        height = rosparam.get_param('/image_height')
        if x1 < margin or y1 < margin or width - x2 < margin or height - y2 < margin:
            pass
        else:
            if max([w / h, h / w]) <= ratio:
                center = [x1 + w / 2, y1 + h / 2]
                point = get_mid_pos(depth_frame, center)
                result.append([x1, y1, w, h, score, point])
    return result


def x_move_limit(id, x_motor):
    x_position = rosparam.get_param('/nx{}_x_motor_position'.format(id)) + x_motor # target position of x motor 
    # Get the nearby x motor position
    if id % 2 == 0:
        nearby_x_position = rosparam.get_param('/nx{}_x_motor_position'.format(id-1))
    else:
        nearby_x_position = rosparam.get_param('/nx{}_x_motor_position'.format(id+1))
    # Check if the x motor position is within the safe range
    # Safe range checking
    if (id % 2 ==1 and (x_position < 0 or x_position > 646)) or (id % 2 == 0 and (x_position < -740 or x_position > 0))  or (id % 2 == 0 and nearby_x_position - x_position > 1100):
        return 1
    elif id % 2 == 1 and x_position - nearby_x_position > 1100:
        return 2
    else:
        return 0


def if_harvest_done(id, x_motor):
    x_position = rosparam.get_param('/nx{}_x_motor_position'.format(id)) + x_motor # target position of x motor
    if (id % 2 == 1 and x_position > 646) or (id % 2 == 0 and x_position > 0):
        return 1
    else:
        return 0

def y_pos_judge(id):
    y_position = rosparam.get_param('/nx{}_y_motor_position'.format(id))

    # 向下为正，y1，y2，y3下层分别为150，-138，-10，给30mm的余量
    # y1:(120, 180), y2:(-168, -108), y3:(-40, 20)
    if (id ==1 or id ==2) and (y_position < 180 or y_position > 120):
        return 1
    elif (id == 3 or id == 4) and (y_position < -108 or y_position > -168):
        return 1
    elif (id == 5 or id == 6) and (y_position < 20 or y_position > -40):
        return 1
    else:
        return 0

if __name__ == "__main__":
    rospy.init_node('NX_Detection')
    pub_rs485 = rospy.Publisher('/Controller_motor_order', MotorOrder, queue_size=6)
    pub_can = rospy.Publisher('/CANController_motor_order', MotorOrder, queue_size=6)
    pub_plc = rospy.Publisher('/PLCController_motor_order', MotorOrder, queue_size=6)
    pub_switch = rospy.Publisher('/Controller_switch_order', SwitchOrder, queue_size=6)
    pub_image = rospy.Publisher("/image_compressed", CompressedImage, queue_size=1)
    rate = rospy.Rate(1.0)
    rate.sleep()

    # Preparing
    warnings.filterwarnings("ignore")

    # Create an instance of the model
    detection = ultralytics.YOLO(rosparam.get_param('/model_path'), task='detect')
    robot = LianChengRobot()

    # Getdown parameter from ROS
    id = rosparam.get_param('/nx_id')
    image_width = rosparam.get_param('/image_width')
    image_height = rosparam.get_param('/image_height')
    fps = rosparam.get_param('/realsense_fps')
    conf = rosparam.get_param('/conf-threshold')
    iou = rosparam.get_param('/iou-threshold')
    box_thr = rosparam.get_param('/box-threshold')
    classes = rosparam.get_param('/class-names')

    # Init a pipeline of RealSense
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, image_width, image_height, rs.format.z16, fps)
    config.enable_stream(rs.stream.color, image_width, image_height, rs.format.bgr8, fps)
    try:
        profile = pipeline.start(config)
    except Exception as e:
        rospy.logerr(f"Failed to start RealSense pipeline: {e}")
        exit(1)
    align = rs.align(rs.stream.color)
    frame_pass = 0
    apple_num = 0

    # Start the detecting process
    while not rospy.is_shutdown():
        rospy.sleep(0.01)
        # Loading images
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        color_image = np.array(color_frame.get_data(), dtype=np.uint8)

        # Perform object detection, apples harvesting and obtain the output image
        nx_mode = rospy.get_param('/nx_mode')
        motors = None
        results = detection.predict(color_image, imgsz=640, device='cuda:0', conf=conf, iou=iou, augment=True, agnostic_nms=True)    
        apples = boxes_filter(np.array(results[0].boxes.xyxy.cpu()), np.array(results[0].boxes.conf.cpu()), depth_frame, box_thr)
        if len(apples) > 0:
            pick_warning, pick_prepared, pick_waiting = sort_sequence(robot, apples)
            if len(pick_warning) > 0:
                color_image = draw_detections(color_image, pick_warning, 'Warning', color=[0, 0, 255])
            if len(pick_prepared) > 0:
                color_image = draw_detections(color_image, [pick_prepared[0]], 'Picking', color=[0, 255, 0])
            if len(pick_waiting) > 0:
                color_image = draw_detections(color_image, pick_waiting, classes[0], color=[255, 0, 0])
        
        # Publish detection results
        compressed_msg = CompressedImage()
        compressed_msg.header.stamp = rospy.Time.now()
        compressed_msg.format = "jpg"
        compressed_msg.data = np.array(cv2.imencode('.jpg', color_image)[1]).tobytes()
        cv2.imshow('Output', color_image)
        pub_image.publish(compressed_msg)
        rospy.loginfo("Publsh compressed image!")
        

        # Wait for a key press to exit
        key = cv2.waitKey(1)
        if key == ord('q') or key == ord('Q'):
            pipeline.stop()
            break
        if nx_mode == 1 :
            
            if_move = 0
            
            if len(apples) > 0 and len(pick_prepared) > 0:

                for j in range(len(pick_prepared)):
                    if j % 2 == 0:
                        x_motor, y_motor, pitch_motor, arm_motor = pick_prepared[j + 1]
                        
                        if x_move_limit(id, x_motor) == 1: # Check if the x motor position is within the safe range
                            rospy.logwarn("Target x motor position is out of range! Skipping this apple!")
                            continue
                        elif x_move_limit(id, x_motor) == 2: # Wait for the nearby x motor to move
                            rospy.logwarn("Target x motor position is too close to the nearby x motor! Waiting for the nearby x motor to move!")
                            while(x_move_limit(id, x_motor) == 2):
                                time.sleep(1)
                        
                        if_move = 1
                        rospy.set_param('/x_motor_position', x_motor)
                        RP.x_motor_move(pub_plc)
                        rospy.set_param('/y_motor_position', y_motor)
                        RP.y_motor_move(pub_plc)
                        time.sleep(2)
                        rospy.set_param('/pitch_motor_position', pitch_motor)
                        RP.pitch_motor_485_move(pub_rs485)
                        time.sleep(1)  
                        rospy.set_param('/arm_motor_position', arm_motor-50)
                        RP.arm_motor_move(pub_rs485)
                        time.sleep(2)
                        RP.wind_motor_on(pub_plc)
                        RP.arm_motor_slow(pub_rs485)
                        time.sleep(2)
                        RP.wrist_motor_on(pub_plc)
                        time.sleep(4)
                        RP.pitch_motor_485_zero(pub_rs485)
                        RP.arm_motor_zero(pub_rs485)
                        time.sleep(2)
                        RP.wrist_motor_off(pub_plc)
                        RP.wind_motor_off(pub_plc)
                        time.sleep(3)

                        apple_num += 1
                        rospy.set_param('/fruit_number',apple_num)
            else:
                if if_move == 0:
                    frame_pass += 1
            
            if frame_pass == 1:
                frame_pass = 0
                if if_harvest_done(id, 100)==1:
                    if y_pos_judge(id) == 1:
                        rospy.set_param('/nx_mode', 4) # 结束工作时机械臂处于下层，置4
                    else:
                        rospy.set_param('/nx_mode',3) # 结束工作时机械臂处于上层，置3
                    rospy.loginfo('Work done!')
                    continue
                while(x_move_limit(id, 100) == 2):
                    time.sleep(1)
                rospy.set_param('/x_motor_position', 100)
                RP.x_motor_move(pub_plc)
                time.sleep(2)
        