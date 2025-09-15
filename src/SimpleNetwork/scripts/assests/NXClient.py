#!/root/archiconda3/envs/apple/bin/python
# -*- coding: utf-8 -*-

import socket
import base64
import cv2
import numpy as np
import rospy
import rosparam
import time


def start_client(SERVER_HOST='localhost', SERVER_PORT=7070):
    try:
        # 1. 创建TCP套接字
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 2. 连接服务器
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        rospy.loginfo('已连接到服务器IP: %s\t 端口: %s', SERVER_HOST, SERVER_PORT)
        while True:
            a = input("请输入要发送的命令编号:")
            if a == '1':
                message = 'Order:1\r\n'
                client_socket.sendall(message.encode('utf-8').ljust(20))
            elif a == '2':
                message = 'Order:2\r\n'
                client_socket.sendall(message.encode('utf-8').ljust(20))
            elif a == '3':
                message = 'Order:3\r\n'
                client_socket.sendall(message.encode('utf-8').ljust(20))
            elif a == '4':
                message = 'Datas:1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24\r\n'
                client_socket.sendall(message.encode('utf-8').ljust(20))
                data = client_socket.recv(1024).decode('utf-8')
                data = data.split('\r\n')[0]
                rospy.loginfo('接收到服务器消息: %s', data)
            elif a == '5':
                message = 'Order:11\r\n'
                client_socket.sendall(message.encode('utf-8').ljust(20))
                info = client_socket.recv(20).decode('utf-8').split('\r\n')[0]
                lenData = int(info.split(':')[1])
                bytesData = b''
                while lenData:
                    newbuf = client_socket.recv(lenData)
                    if not newbuf:
                        break
                    bytesData += newbuf
                    lenData -= len(newbuf)
                decimg = cv2.imdecode(np.frombuffer(base64.b64decode(
                    bytesData), np.uint8), flags=cv2.IMREAD_COLOR)
                decimg = decimg.reshape(480, 640, 3)
            elif a == '6':
                message = 'SSE01:0\r\n'
                client_socket.sendall(message.encode('utf-8').ljust(20))
            elif a == '7':
                message = 'SSE01:1\r\n'
                client_socket.sendall(message.encode('utf-8').ljust(20))
            elif a == '8':
                message = 'FYE01:0\r\n'
                client_socket.sendall(message.encode('utf-8').ljust(20))
            elif a == '9':
                message = 'FYE01:1\r\n'
                client_socket.sendall(message.encode('utf-8').ljust(20))
            elif a == '10':
                message = 'SSM01:2000\r\n'
                client_socket.sendall(message.encode('utf-8').ljust(20))
            elif a == '11':
                message = 'FYM01:-3000\r\n'
                client_socket.sendall(message.encode('utf-8').ljust(20))
            elif a == '12':
                client_socket.close()
                break
    except Exception as e:
        rospy.loginfo('客户端出错: %s', e)


if __name__ == "__main__":
    # 服务器地址和端口
    start_client(SERVER_HOST=rosparam.get_param('/server_host'),
                 SERVER_PORT=rosparam.get_param('/server_port'))
