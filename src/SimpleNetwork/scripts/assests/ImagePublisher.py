#!/root/archiconda3/envs/apple/bin/python
# -*- coding: utf-8 -*-

from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np
import rospy
import time
import random


if __name__ == '__main__':
    # 创建 publisher
    rospy.init_node("Image_Publisher", anonymous=True)
    cimage_pub = rospy.Publisher(
        "/image_compressed", CompressedImage, queue_size=1)
    # 设置循环的频率
    rate = rospy.Rate(100)
    number = 1
    while not rospy.is_shutdown():
        compressed_msg = CompressedImage()
        compressed_msg.header.stamp = rospy.Time.now()
        compressed_msg.format = "jpg"
        image = cv2.imread(f'src/SimpleNetwork/scripts/assests/{number}.jpg')
        compressed_msg.data = np.array(cv2.imencode('.jpg', image)[1]).tobytes()
        cimage_pub.publish(compressed_msg)
        rospy.loginfo("Publsh compressed image: %s", f'src/SimpleNetwork/scripts/assests/{number}.jpg')
        number += 1
        if number == 5:
            number = 1
        if rospy.get_param('/nx_mode') == 1:
            time.sleep(10)
            rospy.set_param('/nx_mode', 3)
            
