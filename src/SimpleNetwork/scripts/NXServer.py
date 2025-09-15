#!/home/archiconda3/envs/apple/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from socket import *
import base64
import cv2
import rospy
import rosparam
import time
import threading
import utils.ROSPublisher as RP
from sensor_msgs.msg import CompressedImage
from liancheng_socket.msg import MotorOrder, SwitchOrder

class NXServer:
    def __init__(self, ip="localhost", port_number=7070):
        self.socket_connection = socket(AF_INET, SOCK_STREAM)
        self.socket_connection.settimeout(10)
        self.socket_connection.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket_connection.setblocking(True)
        # print(ip)
        # print(port_number)
        self.socket_connection.bind((ip, port_number))
        self.socket_connection.listen()

    def accept_connections(self):
        try:
            connection, client_address = self.socket_connection.accept()
            rospy.loginfo("IP: %s\t端口: %s 已连接！", client_address[0], client_address[1])
            return connection, client_address
        except timeout:
            rospy.loginfo("等待客户端连接超时！")
            return None, None
        except Exception as e:
            rospy.loginfo(f"未知客户端尝试连接失败，错误信息: {e}！")
            return None, None
        # finally:
        #     self.close_server()

    def close_server(self):
        self.socket_connection.close()


class ConnectionHandler:
    def __init__(self, connection, client_address, pub):
        self.connection = connection
        self.client_address = client_address
        self.end = "\r\n"
        self.connection_status = 0
        self.stop_event = threading.Event()
        self.start_time = 0
        self.time_length = 0
        self.image = None
        self.pub_rs485 = pub
        
    def close(self):
        self.connection.close()
        rospy.loginfo("IP: %s\t端口: %s 已断开连接！", self.client_address[0], self.client_address[1])

    def send_data(self, data):
        data += self.end
        try:
            self.connection.sendall(data.encode("utf-8").ljust(20))
        except BrokenPipeError:
            rospy.logerr("客户端在发送数据时断开连接！")
            self.connection_status = 1
            self.close()
        except Exception as e:
            rospy.logerr(f"发送数据时出现错误: {e}！")

    def send_image(self):
        global image_stream
        self.image = image_stream
        while True:
            if self.image is not None:
                try:
                    _, message = cv2.imencode(".jpg", self.image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                    bytesData = base64.b64encode(np.array(message))
                    info = "Image:" + str(len(bytesData)) + self.end
                    self.connection.send(info.encode("utf-8").ljust(20))
                    self.connection.sendall(bytesData)
                    rospy.loginfo("\tNX的图像信息已发送,指令为: %s！", "Image:" + str(len(bytesData)))
                    break
                except BrokenPipeError:
                    rospy.logerr("客户端在发送图像时断开连接！")
                    self.connection_status = 1
                    self.close()
                    break
                except Exception as e:
                    rospy.logerr(f"发送图像时出现错误: {e}")
                    break
            else:
                pass

    def check_block_time(self):
        try:
            data = self.connection.recv(1024).decode("utf-8").replace(" ", "")
            self.buffer += data
            message = self.buffer.split("\r\n")
            if len(message) > 1:
                for msg in message[:-1]:
                    self.parse(msg)
                self.buffer = message[-1]
            self.time_length = time.time() - self.start_time
            if data:
                self.time_length = 0
        except UnicodeDecodeError:
            rospy.logerr("数据解码时出现错误！")
        except Exception as e:
            rospy.logerr(f"接收数据时出现错误: {e}！")

    def receive_order(self):
        self.buffer = ""
        while True:
            self.start_time = time.time()
            thread = threading.Thread(target=self.check_block_time)
            thread.start()
            if self.time_length > 5:
                self.stop_event.set()
                rospy.loginfo("\t接收数据超时！")
                self.connection_status = 1
                break
            else:
                self.stop_event.clear()
                thread.join()
                break

    def parse(self, data):
        try:
            if data == "Order:1":
                # 启动NX程序
                rospy.set_param("/nx_mode", 1)
                rospy.loginfo("\t接受到客户端指令: %s\t启动NX程序！", data)

            elif data == "Order:2":
                # 暂停NX程序
                rospy.set_param("/nx_mode", 3)
                rospy.loginfo("\t接受到客户端指令: %s\t暂停NX程序！", data)

            elif data == "Order:3":
                # 暂时不用250701
                rospy.set_param("/nx_mode", 0)
                rospy.loginfo("\t接受到客户端指令: %s\t关闭NX程序！", data)

            elif data.startswith("Datas"):
                pitch_position = float(rospy.get_param("/read_pitch_motor_position"))  # 俯仰位置
                flex_position = float(rospy.get_param("/read_arm_motor_position"))  # 伸缩位置
                pitch_speed = float(rospy.get_param("/read_pitch_motor_speed"))  # 俯仰速度
                flex_speed = float(rospy.get_param("/read_arm_motor_speed"))  # 伸缩速度
                pitch_motor = int(rospy.get_param("/read_pitch_motor_enable_status"))  # 俯仰电机使能  1=ON 0=OFF
                flex_motor = int(rospy.get_param("/read_arm_motor_enable_status"))  # 伸缩电机使能  1=ON 0=OFF
                apple_num = int(rospy.get_param("/fruit_number"))  # 果实数量
                nx_mode = int(rospy.get_param("/nx_mode"))  # nx工作状态   3=当前车位置点采摘结束  2=采摘暂停   1=正在采摘   0=静默状态
                y_motor_position_mode = int(rospy.get_param("/y_motor_position_mode"))  # 当前Y轴位置下采摘状态  1=采摘完成    0=采摘未完成
                y_motor_position_next = float(rospy.get_param("/y_motor_position_next"))  # 当前Y轴位置采摘结束后，接下来采摘时的Y轴位置

                # 待添加
                pitch_motor_RS485_status = int(rospy.get_param("/pitch_motor_RS485_status"))  # NX与俯仰电机通讯状态  1=在线 0=离线
                arm_motor_RS485_status = int(rospy.get_param("/arm_motor_RS485_status"))  # NX与伸缩电机通讯状态  1=在线 0=离线
                PLC_status = int(rospy.get_param("/PLC_status"))  # NX与PLC通讯状态  1=在线 0=离线

                self.send_data(f"{pitch_position},{flex_position},{pitch_speed},{flex_speed},{pitch_motor},{flex_motor},{apple_num},{nx_mode},{y_motor_position_mode},{y_motor_position_next}")
                rospy.loginfo("\t接受到客户端指令: %s\t发送参数列表: %s！", data, f"{pitch_position},{flex_position},{pitch_speed},{flex_speed},{pitch_motor},{flex_motor},{apple_num},{nx_mode},{y_motor_position_mode},{y_motor_position_next}")
                data_list = data.split(":")[1].split(",")
                rospy.set_param("/nx1_x_motor_position", float(data_list[0]))
                rospy.set_param("/nx1_y_motor_position", float(data_list[1]))
                rospy.set_param("/nx1_y_motor_position_mode", int(data_list[2]))
                rospy.set_param("/nx1_y_motor_position_next", float(data_list[3]))
                rospy.set_param("/nx2_x_motor_position", float(data_list[4]))
                rospy.set_param("/nx2_y_motor_position", float(data_list[5]))
                rospy.set_param("/nx2_y_motor_position_mode", int(data_list[6]))
                rospy.set_param("/nx2_y_motor_position_next", float(data_list[7]))
                rospy.set_param("/nx3_x_motor_position", float(data_list[8]))
                rospy.set_param("/nx3_y_motor_position", float(data_list[9]))
                rospy.set_param("/nx3_y_motor_position_mode", int(data_list[10]))
                rospy.set_param("/nx3_y_motor_position_next", float(data_list[11]))
                rospy.set_param("/nx4_x_motor_position", float(data_list[12]))
                rospy.set_param("/nx4_y_motor_position", float(data_list[13]))
                rospy.set_param("/nx4_y_motor_position_mode", int(data_list[14]))
                rospy.set_param("/nx4_y_motor_position_next", float(data_list[15]))
                rospy.set_param("/nx5_x_motor_position", float(data_list[16]))
                rospy.set_param("/nx5_y_motor_position", float(data_list[17]))
                rospy.set_param("/nx5_y_motor_position_mode", int(data_list[18]))
                rospy.set_param("/nx5_y_motor_position_next", float(data_list[19]))
                rospy.set_param("/nx6_x_motor_position", float(data_list[20]))
                rospy.set_param("/nx6_y_motor_position", float(data_list[21]))
                rospy.set_param("/nx6_y_motor_position_mode", int(data_list[22]))
                rospy.set_param("/nx6_y_motor_position_next", float(data_list[23]))

            elif data.startswith("Order:11"):
                self.send_image()

            elif data.split(":")[0].startswith("SSZ"):
                # 设置伸缩电机零点位置
                RP.arm_motor_set_zero(self.pub_rs485)
                rospy.loginfo("\t接受到客户端指令: %s\t设置伸缩电机零点位置成功！", data)

            elif data.split(":")[0].startswith("FYZ"):
                # 设置俯仰电机零点位置
                RP.pitch_motor_set_zero(pub_rs485) 
                rospy.loginfo("\t接受到客户端指令: %s\t设置俯仰电机零点位置成功！", data)

            elif data.split(":")[0].startswith("SSP") and data.split(":")[1] == "1":
                # 伸缩电机JOG+启动
                RP.arm_motor_move(pub_rs485,1,0)
                rospy.loginfo("\t接受到客户端指令: %s\t伸缩电机JOG+启动！", data)

            elif data.split(":")[0].startswith("SSM") and data.split(":")[1] == "1":
                # 伸缩电机JOG-启动
                RP.arm_motor_move(pub_rs485,0,1)
                rospy.loginfo("\t接受到客户端指令: %s\t伸缩电机JOG-启动！", data)

            elif data.split(":")[0].startswith("FYP") and data.split(":")[1] == "1":
                # 俯仰电机JOG+启动
                RP.pitch_motor_485_move(pub_rs485,1,0)
                rospy.loginfo("\t接受到客户端指令: %s\t俯仰电机JOG+启动！", data)

            elif data.split(":")[0].startswith("FYM") and data.split(":")[1] == "1":
                # 俯仰电机JOG-启动
                RP.pitch_motor_485_move(pub_rs485,0,1)
                rospy.loginfo("\t接受到客户端指令: %s\t俯仰电机JOG-启动！", data)

            elif data.split(":")[0].startswith("SSF") and data.split(":")[1] == "1":
                # 伸缩电机复位
                RP.arm_motor_zero(pub_rs485)
                rospy.loginfo("\t接受到客户端指令: %s\t伸缩电机复位！", data)

            elif data.split(":")[0].startswith("FYF") and data.split(":")[1] == "1":
                # 俯仰电机复位
                RP.pitch_motor_zero(pub_rs485)
                rospy.loginfo("\t接受到客户端指令: %s\t俯仰电机复位！", data)

            else:
                rospy.logerr(f"接收到未知指令: {data}！")

        except (ValueError, IndexError):
            rospy.logerr(f"解析指令 {data} 时出现错误！")
        except Exception as e:
            rospy.logerr(f"解析指令时出现错误: {e}！")


def connect_new_client(connection, client_address,pub):
    handler = ConnectionHandler(connection, client_address,pub)
    while True:
        if not handler.connection_status:
            handler.receive_order()
        else:
            handler.close()
            break


def cv2_callback(data):
    global image_stream
    try:
        byte_data = np.frombuffer(data.data, np.uint8)
        image_stream = cv2.imdecode(byte_data, cv2.IMREAD_COLOR)
        # rospy.loginfo("图像接收并解码成功！")
    except Exception as e:
        rospy.logerr(f"解码图像数据时出现错误: {e}！")


if __name__ == "__main__":
    global image_stream
    rospy.init_node("NX_Server", anonymous=True)
    server = NXServer(ip=rosparam.get_param('/server_host'), port_number=rosparam.get_param('/server_port'))
    rospy.Subscriber("/image_compressed", CompressedImage, cv2_callback, queue_size=5)
    pub_rs485 = rospy.Publisher('/Controller_motor_order', MotorOrder, queue_size=6)
    rate = rospy.Rate(1.0)

    while not rospy.is_shutdown():
        try:
            connection, client_address = server.accept_connections()
            if not (connection is None):
                client_thread = threading.Thread(target=connect_new_client, args=(connection, client_address,pub_rs485))
                client_thread.setDaemon(True)
                client_thread.start()
        except Exception as e:
            rospy.loginfo("客户端连接中断！！！")
        rate.sleep()
    
    server.close_server()
