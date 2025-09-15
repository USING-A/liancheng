# liancheng
山东联诚苹果采摘项目相关代码

代码网络结构图如下：
<!-- readme-tree start -->
```
.
├── build
│   ├── catkin_tools_prebuild
│   │   ├── CMakeFiles
│   │   │   ├── 3.16.3
│   │   │   │   ├── CompilerIdC
│   │   │   │   └── CompilerIdCXX
│   │   │   ├── _catkin_empty_exported_target.dir
│   │   │   ├── clean_test_results.dir
│   │   │   ├── download_extra_data.dir
│   │   │   ├── doxygen.dir
│   │   │   ├── run_tests.dir
│   │   │   └── tests.dir
│   │   ├── atomic_configure
│   │   ├── catkin
│   │   │   └── catkin_generated
│   │   │       └── version
│   │   ├── catkin_generated
│   │   │   ├── installspace
│   │   │   └── stamps
│   │   │       └── catkin_tools_prebuild
│   │   └── gtest
│   │       ├── CMakeFiles
│   │       ├── googlemock
│   │       │   └── CMakeFiles
│   │       │       ├── gmock.dir
│   │       │       └── gmock_main.dir
│   │       └── googletest
│   │           └── CMakeFiles
│   │               ├── gtest.dir
│   │               └── gtest_main.dir
│   └── liancheng_socket
│       ├── CMakeFiles
│       │   ├── 3.16.3
│       │   │   ├── CompilerIdC
│       │   │   └── CompilerIdCXX
│       │   ├── _liancheng_socket_generate_messages_check_deps_MotorOrder.dir
│       │   ├── _liancheng_socket_generate_messages_check_deps_ReadOutput.dir
│       │   ├── _liancheng_socket_generate_messages_check_deps_SwitchOrder.dir
│       │   ├── actionlib_generate_messages_cpp.dir
│       │   ├── actionlib_generate_messages_eus.dir
│       │   ├── actionlib_generate_messages_lisp.dir
│       │   ├── actionlib_generate_messages_nodejs.dir
│       │   ├── actionlib_generate_messages_py.dir
│       │   ├── actionlib_msgs_generate_messages_cpp.dir
│       │   ├── actionlib_msgs_generate_messages_eus.dir
│       │   ├── actionlib_msgs_generate_messages_lisp.dir
│       │   ├── actionlib_msgs_generate_messages_nodejs.dir
│       │   ├── actionlib_msgs_generate_messages_py.dir
│       │   ├── clean_test_results.dir
│       │   ├── download_extra_data.dir
│       │   ├── doxygen.dir
│       │   ├── geometry_msgs_generate_messages_cpp.dir
│       │   ├── geometry_msgs_generate_messages_eus.dir
│       │   ├── geometry_msgs_generate_messages_lisp.dir
│       │   ├── geometry_msgs_generate_messages_nodejs.dir
│       │   ├── geometry_msgs_generate_messages_py.dir
│       │   ├── liancheng_can.dir
│       │   │   └── src
│       │   ├── liancheng_client.dir
│       │   │   └── src
│       │   ├── liancheng_plc.dir
│       │   │   └── src
│       │   ├── liancheng_serial.dir
│       │   │   └── src
│       │   ├── liancheng_server.dir
│       │   │   └── src
│       │   ├── liancheng_socket_gencpp.dir
│       │   ├── liancheng_socket_generate_messages.dir
│       │   ├── liancheng_socket_generate_messages_cpp.dir
│       │   ├── liancheng_socket_generate_messages_eus.dir
│       │   ├── liancheng_socket_generate_messages_lisp.dir
│       │   ├── liancheng_socket_generate_messages_nodejs.dir
│       │   ├── liancheng_socket_generate_messages_py.dir
│       │   ├── liancheng_socket_geneus.dir
│       │   ├── liancheng_socket_genlisp.dir
│       │   ├── liancheng_socket_gennodejs.dir
│       │   ├── liancheng_socket_genpy.dir
│       │   ├── roscpp_generate_messages_cpp.dir
│       │   ├── roscpp_generate_messages_eus.dir
│       │   ├── roscpp_generate_messages_lisp.dir
│       │   ├── roscpp_generate_messages_nodejs.dir
│       │   ├── roscpp_generate_messages_py.dir
│       │   ├── rosgraph_msgs_generate_messages_cpp.dir
│       │   ├── rosgraph_msgs_generate_messages_eus.dir
│       │   ├── rosgraph_msgs_generate_messages_lisp.dir
│       │   ├── rosgraph_msgs_generate_messages_nodejs.dir
│       │   ├── rosgraph_msgs_generate_messages_py.dir
│       │   ├── run_tests.dir
│       │   ├── std_msgs_generate_messages_cpp.dir
│       │   ├── std_msgs_generate_messages_eus.dir
│       │   ├── std_msgs_generate_messages_lisp.dir
│       │   ├── std_msgs_generate_messages_nodejs.dir
│       │   ├── std_msgs_generate_messages_py.dir
│       │   ├── talk_test.dir
│       │   │   └── src
│       │   ├── tests.dir
│       │   ├── tf2_msgs_generate_messages_cpp.dir
│       │   ├── tf2_msgs_generate_messages_eus.dir
│       │   ├── tf2_msgs_generate_messages_lisp.dir
│       │   ├── tf2_msgs_generate_messages_nodejs.dir
│       │   └── tf2_msgs_generate_messages_py.dir
│       ├── atomic_configure
│       ├── catkin
│       │   └── catkin_generated
│       │       └── version
│       ├── catkin_generated
│       │   ├── installspace
│       │   └── stamps
│       │       └── liancheng_socket
│       ├── cmake
│       └── gtest
│           ├── CMakeFiles
│           ├── googlemock
│           │   └── CMakeFiles
│           │       ├── gmock.dir
│           │       └── gmock_main.dir
│           └── googletest
│               └── CMakeFiles
│                   ├── gtest.dir
│                   └── gtest_main.dir
├── devel
│   ├── include
│   │   └── liancheng_socket
│   ├── lib
│   │   ├── liancheng_socket
│   │   ├── pkgconfig
│   │   └── python3
│   │       └── dist-packages
│   │           └── liancheng_socket
│   │               ├── __pycache__
│   │               └── msg
│   │                   └── __pycache__
│   └── share
│       ├── catkin_tools_prebuild
│       │   └── cmake
│       ├── common-lisp
│       │   └── ros
│       │       └── liancheng_socket
│       │           └── msg
│       ├── gennodejs
│       │   └── ros
│       │       └── liancheng_socket
│       │           └── msg
│       ├── liancheng_socket
│       │   └── cmake
│       └── roseus
│           └── ros
│               └── liancheng_socket
│                   └── msg
├── logs
│   ├── catkin_tools_prebuild
│   └── liancheng_socket
└── src
    └── SimpleNetwork
        ├── config
        ├── msg
        ├── scripts
        │   ├── assests
        │   ├── models
        │   └── utils
        │       └── __pycache__
        └── src

163 directories
```
<!-- readme-tree end -->
