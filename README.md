# liancheng
山东联诚苹果采摘项目相关代码

代码网络结构图如下：
├── build
├── devel
├── logs
├── src
│   ├── CMakeLists.txt
│   └── SimpleNetwork
│       ├── CMakeLists.txt
│       ├── LICENSE
│       ├── README.md
│       ├── config
│       │   └── ROS_Param.yaml
│       ├── msg
│       │   ├── MotorOrder.msg
│       │   ├── ReadOutput.msg
│       │   └── SwitchOrder.msg
│       ├── package.xml
│       ├── scripts
│       │   ├── AppleROS.py
│       │   ├── NXServer.py
│       │   ├── assests
│       │   │   ├── BrightnessScore.py
│       │   │   ├── HighlightRemove.py
│       │   │   ├── ImagePublisher.py
│       │   │   ├── ImagesLoader.py
│       │   │   ├── ImagesMerge.py
│       │   │   ├── NXClient.py
│       │   │   └── PicturesCapture.py
│       │   ├── models
│       │   │   ├── best40.engine
│       │   │   ├── yolov10n.engine
│       │   │   ├── yolov10n.onnx
│       │   │   ├── yolov10n_fp16_4.engine
│       │   │   ├── yolov11m.engine
│       │   │   └── yolov8s.engine
│       │   ├── testDetection.py
│       │   ├── testPublisher.py
│       │   ├── testSubscriber.py
│       │   └── utils
│       │       ├── PickSequence.py
│       │       ├── ROSPublisher.py
│       │       ├── RobotMovement.py
│       │       ├── __init__.py
│       │       └── __pycache__
│       │           ├── EngineModels.cpython-38.pyc
│       │           ├── ONNXModels.cpython-38.pyc
│       │           ├── PickSequence.cpython-38.pyc
│       │           ├── ROSPublisher.cpython-38.pyc
│       │           ├── RobotMovement.cpython-38.pyc
│       │           └── __init__.cpython-38.pyc
│       └── src
│           ├── Makefile
│           ├── RS485Serial.cpp
│           ├── RS485Serial.h
│           ├── TCPClient.cpp
│           ├── TCPClient.h
│           ├── TCPServer.cpp
│           ├── TCPServer.h
│           ├── canusb.cpp
│           ├── client.cpp
│           ├── plc.cpp
│           ├── serial.cpp
│           ├── server.cpp
│           ├── test_talk.cpp
│           └── testcan.py
├── test.sh
├── robot.sh
└── tree.bak


