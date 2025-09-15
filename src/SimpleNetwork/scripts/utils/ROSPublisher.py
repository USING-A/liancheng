#!/root/archiconda3/envs/apple/bin/python
# -*- coding: utf-8 -*-
"""
AUTHOR: Luo Hefei
Copyright (C) 2024, Luo Hefei. All right reserved.
"""

import rospy
from liancheng_socket.msg import MotorOrder, SwitchOrder, ReadOutput


def x_motor_move(pub1):
    if rospy.has_param('/x_motor_position'):
        x_position = rospy.get_param('/x_motor_position') * 1000
    if rospy.has_param('/nx_id'):
        id = rospy.get_param('/nx_id')
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (2).to_bytes(1, 'little') # station num 2 is static
    msg.station_num += (int(id)).to_bytes(1, 'little') # station num top:1->2 middle:3->4 down:5->6
    msg.form += (12).to_bytes(1, 'little')
    msg.vel.append(100)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(x_position)
    msg.pos_thr.append(10)
    pub1.publish(msg)


def x_motor_zero(pub1):
    if rospy.has_param('/x_motor_position'):
        rospy.set_param('/x_motor_position',0)
    if rospy.has_param('/nx_id'):
        id = rospy.get_param('/nx_id')
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (2).to_bytes(1, 'little')
    msg.station_num += (int(id)).to_bytes(1, 'little')
    msg.form += (11).to_bytes(1, 'little')
    msg.vel.append(100)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(10)
    pub1.publish(msg)


def y_motor_move(pub1):
    if rospy.has_param('/y_motor_position'):
        y_position = rospy.get_param('/y_motor_position')
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (2).to_bytes(1, 'little')
    msg.station_num += (19).to_bytes(1, 'little')
    msg.form += (12).to_bytes(1, 'little')
    msg.vel.append(100)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(y_position)
    msg.pos_thr.append(10)
    pub1.publish(msg)


def y_motor_zero(pub1):
    if rospy.has_param('/y_motor_position'):
        rospy.set_param('/y_motor_position',0)
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (2).to_bytes(1, 'little')
    msg.station_num += (19).to_bytes(1, 'little')
    msg.form += (11).to_bytes(1, 'little')
    msg.vel.append(100)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(10)
    pub1.publish(msg)


def wind_motor_on(pub1):
    if rospy.has_param('/nx_id'):
        id = rospy.get_param('/nx_id')
    msg_sw = MotorOrder()
    msg_sw.header.stamp = rospy.Time.now()
    msg_sw.station_num += (3).to_bytes(1, 'little')
    msg_sw.station_num += (int(id)).to_bytes(1, 'little')
    msg_sw.vel_ac.append(1)
    msg_sw.form += (1).to_bytes(1, 'little')
    pub1.publish(msg_sw)


def wind_motor_off(pub1):
    if rospy.has_param('/nx_id'):
        id = rospy.get_param('/nx_id')
    msg_sw = MotorOrder()
    msg_sw.header.stamp = rospy.Time.now()
    msg_sw.station_num += (3).to_bytes(1, 'little')
    msg_sw.station_num += (int(id)).to_bytes(1, 'little')
    msg_sw.vel_ac.append(1)
    msg_sw.form += (0).to_bytes(1, 'little')
    pub1.publish(msg_sw)


def wrist_motor_on(pub1):
    if rospy.has_param('/nx_id'):
        id = rospy.get_param('/nx_id')
    msg_sw = MotorOrder()
    msg_sw.header.stamp = rospy.Time.now()
    msg_sw.station_num += (3).to_bytes(1, 'little')
    msg_sw.station_num += (int(id)).to_bytes(1, 'little')
    msg_sw.vel_ac.append(2)
    msg_sw.form += (1).to_bytes(1, 'little')
    pub1.publish(msg_sw)


def wrist_motor_off(pub1):
    if rospy.has_param('/nx_id'):
        id = rospy.get_param('/nx_id')
    msg_sw = MotorOrder()
    msg_sw.header.stamp = rospy.Time.now()
    msg_sw.station_num += (3).to_bytes(1, 'little')
    msg_sw.station_num += (int(id)).to_bytes(1, 'little')
    msg_sw.vel_ac.append(2)
    msg_sw.form += (0).to_bytes(1, 'little')
    pub1.publish(msg_sw)


def arm_motor_enable_on(pub):
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num = (2).to_bytes(1, 'little')
    msg.form = (99).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(1000)
    pub.publish(msg)


def arm_motor_enable_off(pub):
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num = (2).to_bytes(1, 'little')
    msg.form = (100).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(1000)
    pub.publish(msg)


def arm_motor_move(pub,jog_positive=0,jog_negative=0):
    if rospy.has_param('/arm_motor_position'):
        arm_position = rospy.get_param('/arm_motor_position')
    if rospy.has_param('/read_arm_motor_position'):
        current_arm_position = rospy.get_param('/read_arm_motor_position')
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (2).to_bytes(1, 'little')
    msg.form += (100).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(False)
    msg.pos.append(0)
    msg.pos_thr.append(1000)
    
    if jog_positive:
        msg.station_num += (2).to_bytes(1, 'little')
        msg.form += (0).to_bytes(1, 'little')
        msg.vel.append(300)
        msg.vel_ac.append(50)
        msg.vel_de.append(50)
        msg.pos_mode.append(False)
        msg.pos.append(20)
        msg.pos_thr.append(5000)   
    elif jog_negative:
        msg.station_num += (2).to_bytes(1, 'little')
        msg.form += (0).to_bytes(1, 'little')
        msg.vel.append(300)
        msg.vel_ac.append(50)
        msg.vel_de.append(50)
        msg.pos_mode.append(False)
        msg.pos.append(-20)
        msg.pos_thr.append(5000)     
        
    else:
        msg.station_num += (2).to_bytes(1, 'little')
        msg.form += (0).to_bytes(1, 'little')
        msg.vel.append(300)
        msg.vel_ac.append(50)
        msg.vel_de.append(50)
        msg.pos_mode.append(False)
        msg.pos.append(int(arm_position - current_arm_position))
        msg.pos_thr.append(5000)
    
    msg.station_num += (2).to_bytes(1, 'little')
    msg.form += (99).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(False)
    msg.pos.append(0)
    msg.pos_thr.append(1000)
    pub.publish(msg)

def arm_motor_slow(pub):
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (2).to_bytes(1, 'little')
    msg.form += (100).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(False)
    msg.pos.append(0)
    msg.pos_thr.append(1000)
    msg.station_num += (2).to_bytes(1, 'little')
    msg.form += (0).to_bytes(1, 'little')
    msg.vel.append(100)
    msg.vel_ac.append(50)
    msg.vel_de.append(50)
    msg.pos_mode.append(False)
    msg.pos.append(50)
    msg.pos_thr.append(5000)
    msg.station_num += (2).to_bytes(1, 'little')
    msg.form += (99).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(False)
    msg.pos.append(0)
    msg.pos_thr.append(1000)
    pub.publish(msg)

def arm_motor_zero(pub):
    if rospy.has_param('/arm_motor_position'):
        rospy.set_param('/arm_motor_position',0)
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (2).to_bytes(1, 'little')
    msg.form += (100).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(1000)
    msg.station_num += (2).to_bytes(1, 'little')
    msg.form += (0).to_bytes(1, 'little')
    msg.vel.append(300)
    msg.vel_ac.append(50)
    msg.vel_de.append(50)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(5000)
    msg.station_num += (2).to_bytes(1, 'little')
    msg.form += (99).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(1000)
    pub.publish(msg)

def arm_motor_set_zero(pub):
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (2).to_bytes(1, 'little')
    msg.form += (100).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(1000)

    msg.station_num += (2).to_bytes(1, 'little')
    msg.form = (2).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(1000)

    msg.station_num += (2).to_bytes(1, 'little')
    msg.form += (99).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(1000)
    pub.publish(msg)

def pitch_motor_move(pub1):
    if rospy.has_param('/pitch_motor_position'):
        pitch_position = rospy.get_param('/pitch_motor_position')
    if rospy.has_param('/read_pitch_motor_position'):
        current_pitch_position = rospy.get_param('/read_pitch_motor_position')
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (1).to_bytes(1, 'little')
    msg.station_num += (66).to_bytes(1, 'little')
    msg.form = (200).to_bytes(1, 'little')
    msg.vel.append(20)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(int(pitch_position - current_pitch_position))
    msg.pos_thr.append(0)
    pub1.publish(msg)

def pitch_motor_zero(pub1):
    if rospy.has_param('/pitch_motor_position'):
        rospy.set_param('/pitch_motor_position',0)
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (1).to_bytes(1, 'little')
    msg.station_num += (66).to_bytes(1, 'little')
    msg.form = (199).to_bytes(1, 'little')
    msg.vel.append(20)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(0) 
    msg.pos_thr.append(0)
    pub1.publish(msg)


def pitch_motor_485_move(pub,jog_positive=0,jog_negative=0):
    if rospy.has_param('/pitch_motor_position'):
        pitch_position = rospy.get_param('/pitch_motor_position')
    if rospy.has_param('/read_pitch_motor_position'):
        current_pitch_position = rospy.get_param('/read_pitch_motor_position')
    """两度点动"""
    if jog_positive:
        msg = MotorOrder()
        msg.header.stamp = rospy.Time.now()
        msg.station_num += (1).to_bytes(1, 'little')
        msg.form += (200).to_bytes(1, 'little')
        msg.vel.append(20)
        msg.vel_ac.append(50)
        msg.vel_de.append(50)
        msg.pos_mode.append(False)
        msg.pos.append(2)
        msg.pos_thr.append(5000)
        pub.publish(msg)
    elif jog_negative:
        msg = MotorOrder()
        msg.header.stamp = rospy.Time.now()
        msg.station_num += (1).to_bytes(1, 'little')
        msg.form += (200).to_bytes(1, 'little')
        msg.vel.append(20)
        msg.vel_ac.append(50)
        msg.vel_de.append(50)
        msg.pos_mode.append(False)
        msg.pos.append(-2)
        msg.pos_thr.append(5000)
        pub.publish(msg)
    else:
        msg = MotorOrder()
        msg.header.stamp = rospy.Time.now()
        msg.station_num += (1).to_bytes(1, 'little')
        msg.form += (200).to_bytes(1, 'little')
        msg.vel.append(100)
        msg.vel_ac.append(50)
        msg.vel_de.append(50)
        msg.pos_mode.append(False)
        msg.pos.append(int(pitch_position - current_pitch_position))
        msg.pos_thr.append(5000)
        pub.publish(msg)


def pitch_motor_485_zero(pub):
    if rospy.has_param('/pitch_motor_position'):
        rospy.set_param('/pitch_motor_position',0)
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (1).to_bytes(1, 'little')
    msg.form += (200).to_bytes(1, 'little')
    msg.vel.append(6) # speed have to under 10
    msg.vel_ac.append(50)
    msg.vel_de.append(50)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(5000)
    pub.publish(msg)

def pitch_motor_set_zero(pub1):
    msg = MotorOrder()
    msg.header.stamp = rospy.Time.now()
    msg.station_num += (1).to_bytes(1, 'little')
    msg.station_num += (66).to_bytes(1, 'little')
    msg.form = (201).to_bytes(1, 'little')
    msg.vel.append(0)
    msg.vel_ac.append(0)
    msg.vel_de.append(0)
    msg.pos_mode.append(True)
    msg.pos.append(0)
    msg.pos_thr.append(0)
    pub1.publish(msg)


