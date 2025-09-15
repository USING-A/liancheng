#!/root/archiconda3/envs/apple/bin/python
# -*- coding: utf-8 -*-

"""
AUTHOR: Luo Hefei
Copyright (C) 2023, Luo Hefei. All right reserved.
"""


import rospy
import time
from liancheng_socket.msg import MotorOrder, SwitchOrder
import utils.ROSPublisher as RP
import rosparam


if __name__ == "__main__":
    rospy.init_node('talker1', anonymous=True)
    pub_rs485 = rospy.Publisher('/Controller_motor_order', MotorOrder, queue_size=6)
    pub_can = rospy.Publisher('/CANController_motor_order', MotorOrder, queue_size=6)
    pub_plc = rospy.Publisher('/PLCController_motor_order', MotorOrder, queue_size=6)
    pub_switch = rospy.Publisher('/Controller_switch_order', SwitchOrder, queue_size=6)
    rate = rospy.Rate(1.0)
    rate.sleep()
    while True:
        a = input("Please enter: ")
        if a == "1":
            rospy.set_param('/arm_motor_position',-200)
            RP.arm_motor_move(pub_rs485)
            rate.sleep()
        elif a == "10":
            RP.arm_motor_zero(pub_rs485)
            rate.sleep()
        elif a == "2":
            rospy.set_param('/pitch_motor_position', -3)
            RP.pitch_motor_move(pub_can)
            rate.sleep()
        elif a == "20":
            RP.pitch_motor_zero(pub_can)
            rate.sleep()
        elif a == "3":
            rospy.set_param('/x_motor_position', -50)
            RP.x_motor_move(pub_plc)
            rate.sleep()
        elif a == "30":
            RP.x_motor_zero(pub_plc)
            rate.sleep()
        elif a == "4":
            rospy.set_param('/y_motor_position', -10)
            RP.y_motor_move(pub_plc)
            rate.sleep()
        elif a == "40":
            RP.y_motor_zero(pub_plc)
            rate.sleep()
        elif a == "5":
            RP.wind_motor_on(pub_plc)
            rate.sleep()
        elif a == "50":
            RP.wind_motor_off(pub_plc)
            rate.sleep()
        elif a == "6":
            RP.wrist_motor_on(pub_plc)
            rate.sleep()
        elif a == "60":
            RP.wrist_motor_off(pub_plc)
            rate.sleep()
        elif a == "7":
            rospy.set_param('/pitch_motor_position', -7)
            RP.pitch_motor_485_move(pub_rs485)
            rate.sleep()
        elif a == "70":
            RP.pitch_motor_485_zero(pub_rs485)
            rate.sleep()
        elif a== "8":
            RP.arm_motor_move(pub_rs485,1,0)
            rate.sleep()
        elif a== "80":
            RP.arm_motor_move(pub_rs485,0,1)
            rate.sleep()
        elif a=="88":    
            RP.arm_motor_set_zero(pub_rs485)
            rate.sleep()
        elif a=="9":
            RP.pitch_motor_485_move(pub_rs485,1,0)
            rate.sleep()
        elif a=="90":
            RP.pitch_motor_485_move(pub_rs485,0,1)
            rate.sleep()
        elif a=="99":
            RP.pitch_motor_set_zero(pub_rs485)    
            rate.sleep()
        elif a == "q":
            break