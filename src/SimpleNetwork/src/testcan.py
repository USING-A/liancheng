#!/root/Softwares/archiconda3/envs/apple/bin/python
# -*- coding: utf-8 -*-
import time
import os
import can
import threading

can0=can.interface(channel='can0',bustyp='socketcab_ctypes')
msg=can.Message(arbitration_id=0x142,data=[0xa4,0x00,0xf4,0x01,0xa0,0x8c,0x00,0x00],extended_id=False)

while 1:
    os.system('sudo ip link set can0 type can bitrate 1000000')
    os.system('sudo ifconfig can0 up')
    
