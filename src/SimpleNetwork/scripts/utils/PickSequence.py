#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AUTHOR: Luo Hefei
Copyright (C) 2024, Luo Hefei. All right reserved.
"""


def sort_sequence(robot, objects):
    pick_warning = []
    pick_prepared = []
    stop = 0
    apples_sorted = sorted(objects, key=lambda x: (x[0] + x[2] / 2, -(x[1] + x[3] / 2)), reverse=False)
    for i in range(len(apples_sorted)):
        motors = robot.compute_joint(apples_sorted[i][5], 0)
        if motors is None:
            pick_warning.append(apples_sorted[i])
        else:
            pick_prepared = [apples_sorted[i], motors]
            stop = i + 1
            # break
    if stop >= len(apples_sorted):
        pick_waiting = []
    else:
        pick_waiting = apples_sorted[stop:]
    return pick_warning, pick_prepared, pick_waiting