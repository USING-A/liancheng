#!/root/archiconda3/envs/apple/bin/python
# -*- coding: utf-8 -*-
"""
AUTHOR: Luo Hefei
Copyright (C) 2023, Luo Hefei. All right reserved.
"""


import rosparam
import numpy as np
from spatialmath import SE3
from scipy.optimize import fsolve
from roboticstoolbox import DHRobot, RevoluteMDH, PrismaticMDH



# 同一单位为mm
class LianChengRobot:
    def __init__(self):
        self.param = {'base_x': 110, 'base_y': 105}
        L = [RevoluteMDH(a=0.0, d=0.0, alpha=0.0, qlim=np.array([-np.pi / 9, np.pi / 60])),
             PrismaticMDH(a=self.param['base_x'], theta=0.0, alpha=np.pi / 2, qlim=np.array([0, 545])),
             RevoluteMDH(a=0.0, d=self.param['base_y'], alpha=0.0)]
        self.robot = DHRobot(L, name='robot')
        self.T_picker2base = self.robot.fkine([0, 0, 0])
        self.T_base2picker = self.T_picker2base.inv()
        # self.T_camera2base = SE3.Rx(90, 'deg') * SE3.Rz(-90, 'deg') * SE3(-1 * self.param['camera_x'], -1 * self.param['camera_y'], -1 * self.param['camera_z']) * SE3.Rx(-1 * self.param['camera_deg'], 'deg')
        self.id = rosparam.get_param('/nx_id')
        self.T_camera2base = SE3(rosparam.get_param('/camera2base_{}'.format(self.id)))
        self.arm_max = rosparam.get_param('/arm_max')
        self.x_max = rosparam.get_param('/x_max')
        self.y_max = rosparam.get_param('/y_max')
        self.pitch_min = rosparam.get_param('/pitch_min')
        self.pitch_max = rosparam.get_param('/pitch_max')

    def T2point(self, T):
        return list(map(float, [T[0][0], T[1][0], T[2][0]]))

    def robot_ikine(self, a1, a2):
        def equations(vars):
            x, y = vars
            eq1 = self.param['base_x'] * np.cos(x) + (y - self.param['base_y']) * np.sin(x) - a1
            eq2 = self.param['base_x'] * np.sin(x) - (y - self.param['base_y']) * np.cos(x) - a2
            return [eq1, eq2]

        initial_guess = [0, 0]
        solution = fsolve(equations, initial_guess)
        float_solution = (float(solution[0]), float(solution[1]))
        return float_solution

    def compute_joint(self, target, y_motor=None):
        if target is None:
            return None
        p_target2base = self.T_camera2base * target
        print(p_target2base)
        p_target2picker = self.T_base2picker * p_target2base
        x_motor = self.T2point(p_target2picker)[1]
        if y_motor is None:
            y_motor = self.T2point(p_target2picker)[0]
            pitch_motor = 0
            arm_motor = self.T2point(p_target2picker)[2]
        else:
            p_target2picker_move = SE3(-1 * y_motor, -1 * x_motor, 0) * p_target2picker
            T = self.T_picker2base * p_target2picker_move
            pitch_motor, arm_motor = self.robot_ikine(T[0][0], T[1][0])
        if int(arm_motor) > self.arm_max:
            return None
        elif int(pitch_motor * 180 / np.pi) > self.pitch_max or int(pitch_motor * 180 / np.pi) < self.pitch_min:
            return None
        else:
            return [int(x_motor), int(y_motor), int(pitch_motor * 180 / np.pi), int(arm_motor)] # + 170