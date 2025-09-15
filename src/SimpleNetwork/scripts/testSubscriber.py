#!/root/archiconda3/envs/apple/bin/python
# -*- coding: utf-8 -*-

import rospy
from liancheng_socket.msg import MotorOrder, SwitchOrder

def RS485InfoCallback(msg):
    rospy.loginfo("Subcribe RS485 Info: %s,%s,%s,%s,%s,%s,%s,%s",msg.station_num, msg.form, msg.vel, msg.vel_ac, msg.vel_de, msg.pos_mode, msg.pos, msg.pos_thr)

def CANInfoCallback(msg):
    rospy.loginfo("Subcribe CAN Info: %s,%s,%s,%s,%s,%s,%s,%s",msg.station_num, msg.form, msg.vel, msg.vel_ac, msg.vel_de, msg.pos_mode, msg.pos, msg.pos_thr)

def SWITCHInfoCallback(msg):
    rospy.loginfo("Subcribe SWITCH Info: %s,%s,%s", msg.station_num, msg.switch_num, msg.case_num)
    

def person_subscriber():
	# ROS节点初始化
    rospy.init_node('person_subscriber', anonymous=True)
	# 创建一个Subscriber，订阅名为/person_info的topic，注册回调函数personInfoCallback
    rospy.Subscriber("/Controller_motor_order", MotorOrder, RS485InfoCallback)
    rospy.Subscriber("/CANController_motor_order", MotorOrder, CANInfoCallback)
    rospy.Subscriber("/Controller_switch_order", SwitchOrder, SWITCHInfoCallback)
	# 循环等待回调函数
    rospy.spin()

if __name__ == '__main__':
    person_subscriber()

