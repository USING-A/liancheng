#!/bin/bash

sudo gnome-terminal --title="roscore" -- bash -c "source /opt/ros/noetic/setup.bash; roscore; exec bash"

sleep 5s

sudo chmod 777 /dev/ttyUSB0 /dev/ttyUSB1

sleep 2s

sudo gnome-terminal --title="RS485" -- bash -c "cd Desktop/robot/; source devel/setup.bash; rosparam load src/SimpleNetwork/config/ROS_Param.yaml; rosrun liancheng_socket liancheng_serial; exec bash"

echo "RS485 successfully connected"

sleep 3s

# gnome-terminal --title="CAN" -- bash -c "cd Desktop/robot/; source devel/setup.bash; rosrun liancheng_socket liancheng_can; exec bash"

# echo "CAN successfully connected"

# sleep 2s

sudo gnome-terminal --title="PLC" -- bash -c "cd Desktop/robot/; source devel/setup.bash; rosrun liancheng_socket liancheng_plc; exec bash"

echo "PLC successfully connected"

sleep 3s


# sudo gnome-terminal --title="testPublish" -- bash -c "cd Desktop/robot/; source devel/setup.bash; rosrun liancheng_socket testPublisher.py; exec bash"

# echo "Publisher test successfully started"

# sleep 2s

sudo gnome-terminal --title="RobotPicking" -- bash -c "conda activate apple; cd Desktop/robot/; source devel/setup.bash; rosrun liancheng_socket AppleROS.py; exec bash"

echo "Picking programme successfully started"

sleep 2s

sudo gnome-terminal --title="NXServer" -- bash -c "conda activate apple; cd Desktop/robot/; source devel/setup.bash; rosrun liancheng_socket NXServer.py; exec bash"

echo "NXServer successfully started"



