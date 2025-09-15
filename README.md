# liancheng
山东联诚苹果采摘项目相关代码

！！上传修改统一按“年月日-姓名缩写-今日第几次提交”格式发起，eg. 20250915-lc-1

代码网络结构图如下：
<!-- readme-tree start -->
```
.
├── .github
│   └── workflows
│       └── tree.yml
├── README.md
├── _
├── build
│   ├── .built_by
│   ├── .catkin_tools.yaml
│   ├── catkin_tools_prebuild
│   │   ├── CATKIN_IGNORE
│   │   ├── CMakeCache.txt
│   │   ├── CMakeFiles
│   │   │   ├── 3.16.3
│   │   │   │   ├── CMakeCCompiler.cmake
│   │   │   │   ├── CMakeCXXCompiler.cmake
│   │   │   │   ├── CMakeDetermineCompilerABI_C.bin
│   │   │   │   ├── CMakeDetermineCompilerABI_CXX.bin
│   │   │   │   ├── CMakeSystem.cmake
│   │   │   │   ├── CompilerIdC
│   │   │   │   │   ├── CMakeCCompilerId.c
│   │   │   │   │   └── a.out
│   │   │   │   └── CompilerIdCXX
│   │   │   │       ├── CMakeCXXCompilerId.cpp
│   │   │   │       └── a.out
│   │   │   ├── CMakeDirectoryInformation.cmake
│   │   │   ├── CMakeError.log
│   │   │   ├── CMakeOutput.log
│   │   │   ├── CMakeRuleHashes.txt
│   │   │   ├── Makefile.cmake
│   │   │   ├── Makefile2
│   │   │   ├── TargetDirectories.txt
│   │   │   ├── _catkin_empty_exported_target.dir
│   │   │   │   ├── DependInfo.cmake
│   │   │   │   ├── build.make
│   │   │   │   ├── cmake_clean.cmake
│   │   │   │   └── progress.make
│   │   │   ├── clean_test_results.dir
│   │   │   │   ├── DependInfo.cmake
│   │   │   │   ├── build.make
│   │   │   │   ├── cmake_clean.cmake
│   │   │   │   └── progress.make
│   │   │   ├── cmake.check_cache
│   │   │   ├── download_extra_data.dir
│   │   │   │   ├── DependInfo.cmake
│   │   │   │   ├── build.make
│   │   │   │   ├── cmake_clean.cmake
│   │   │   │   └── progress.make
│   │   │   ├── doxygen.dir
│   │   │   │   ├── DependInfo.cmake
│   │   │   │   ├── build.make
│   │   │   │   ├── cmake_clean.cmake
│   │   │   │   └── progress.make
│   │   │   ├── progress.marks
│   │   │   ├── run_tests.dir
│   │   │   │   ├── DependInfo.cmake
│   │   │   │   ├── build.make
│   │   │   │   ├── cmake_clean.cmake
│   │   │   │   └── progress.make
│   │   │   └── tests.dir
│   │   │       ├── DependInfo.cmake
│   │   │       ├── build.make
│   │   │       ├── cmake_clean.cmake
│   │   │       └── progress.make
│   │   ├── CMakeLists.txt
│   │   ├── CTestConfiguration.ini
│   │   ├── CTestCustom.cmake
│   │   ├── CTestTestfile.cmake
│   │   ├── Makefile
│   │   ├── atomic_configure
│   │   │   ├── .rosinstall
│   │   │   ├── _setup_util.py
│   │   │   ├── env.sh
│   │   │   ├── local_setup.bash
│   │   │   ├── local_setup.sh
│   │   │   ├── local_setup.zsh
│   │   │   ├── setup.bash
│   │   │   ├── setup.sh
│   │   │   └── setup.zsh
│   │   ├── catkin
│   │   │   └── catkin_generated
│   │   │       └── version
│   │   │           └── package.cmake
│   │   ├── catkin_generated
│   │   │   ├── env_cached.sh
│   │   │   ├── generate_cached_setup.py
│   │   │   ├── installspace
│   │   │   │   ├── .rosinstall
│   │   │   │   ├── _setup_util.py
│   │   │   │   ├── catkin_tools_prebuild.pc
│   │   │   │   ├── catkin_tools_prebuildConfig-version.cmake
│   │   │   │   ├── catkin_tools_prebuildConfig.cmake
│   │   │   │   ├── env.sh
│   │   │   │   ├── local_setup.bash
│   │   │   │   ├── local_setup.sh
│   │   │   │   ├── local_setup.zsh
│   │   │   │   ├── setup.bash
│   │   │   │   ├── setup.sh
│   │   │   │   └── setup.zsh
│   │   │   ├── package.cmake
│   │   │   ├── pkg.develspace.context.pc.py
│   │   │   ├── pkg.installspace.context.pc.py
│   │   │   ├── setup_cached.sh
│   │   │   └── stamps
│   │   │       └── catkin_tools_prebuild
│   │   │           ├── _setup_util.py.stamp
│   │   │           ├── interrogate_setup_dot_py.py.stamp
│   │   │           ├── package.xml.stamp
│   │   │           └── pkg.pc.em.stamp
│   │   ├── cmake_install.cmake
│   │   ├── gtest
│   │   │   ├── CMakeFiles
│   │   │   │   ├── CMakeDirectoryInformation.cmake
│   │   │   │   └── progress.marks
│   │   │   ├── CTestTestfile.cmake
│   │   │   ├── Makefile
│   │   │   ├── cmake_install.cmake
│   │   │   ├── googlemock
│   │   │   │   ├── CMakeFiles
│   │   │   │   │   ├── CMakeDirectoryInformation.cmake
│   │   │   │   │   ├── gmock.dir
│   │   │   │   │   │   ├── DependInfo.cmake
│   │   │   │   │   │   ├── build.make
│   │   │   │   │   │   ├── cmake_clean.cmake
│   │   │   │   │   │   ├── depend.make
│   │   │   │   │   │   ├── flags.make
│   │   │   │   │   │   ├── link.txt
│   │   │   │   │   │   └── progress.make
│   │   │   │   │   ├── gmock_main.dir
│   │   │   │   │   │   ├── DependInfo.cmake
│   │   │   │   │   │   ├── build.make
│   │   │   │   │   │   ├── cmake_clean.cmake
│   │   │   │   │   │   ├── depend.make
│   │   │   │   │   │   ├── flags.make
│   │   │   │   │   │   ├── link.txt
│   │   │   │   │   │   └── progress.make
│   │   │   │   │   └── progress.marks
│   │   │   │   ├── CTestTestfile.cmake
│   │   │   │   ├── Makefile
│   │   │   │   └── cmake_install.cmake
│   │   │   └── googletest
│   │   │       ├── CMakeFiles
│   │   │       │   ├── CMakeDirectoryInformation.cmake
│   │   │       │   ├── gtest.dir
│   │   │       │   │   ├── DependInfo.cmake
│   │   │       │   │   ├── build.make
│   │   │       │   │   ├── cmake_clean.cmake
│   │   │       │   │   ├── depend.make
│   │   │       │   │   ├── flags.make
│   │   │       │   │   ├── link.txt
│   │   │       │   │   └── progress.make
│   │   │       │   ├── gtest_main.dir
│   │   │       │   │   ├── DependInfo.cmake
│   │   │       │   │   ├── build.make
│   │   │       │   │   ├── cmake_clean.cmake
│   │   │       │   │   ├── depend.make
│   │   │       │   │   ├── flags.make
│   │   │       │   │   ├── link.txt
│   │   │       │   │   └── progress.make
│   │   │       │   └── progress.marks
│   │   │       ├── CTestTestfile.cmake
│   │   │       ├── Makefile
│   │   │       └── cmake_install.cmake
│   │   └── package.xml
│   └── liancheng_socket
│       ├── CATKIN_IGNORE
│       ├── CMakeCache.txt
│       ├── CMakeFiles
│       │   ├── 3.16.3
│       │   │   ├── CMakeCCompiler.cmake
│       │   │   ├── CMakeCXXCompiler.cmake
│       │   │   ├── CMakeDetermineCompilerABI_C.bin
│       │   │   ├── CMakeDetermineCompilerABI_CXX.bin
│       │   │   ├── CMakeSystem.cmake
│       │   │   ├── CompilerIdC
│       │   │   │   ├── CMakeCCompilerId.c
│       │   │   │   └── a.out
│       │   │   └── CompilerIdCXX
│       │   │       ├── CMakeCXXCompilerId.cpp
│       │   │       └── a.out
│       │   ├── CMakeDirectoryInformation.cmake
│       │   ├── CMakeError.log
│       │   ├── CMakeOutput.log
│       │   ├── CMakeRuleHashes.txt
│       │   ├── Makefile.cmake
│       │   ├── Makefile2
│       │   ├── TargetDirectories.txt
│       │   ├── _liancheng_socket_generate_messages_check_deps_MotorOrder.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── _liancheng_socket_generate_messages_check_deps_ReadOutput.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── _liancheng_socket_generate_messages_check_deps_SwitchOrder.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── actionlib_generate_messages_cpp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── actionlib_generate_messages_eus.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── actionlib_generate_messages_lisp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── actionlib_generate_messages_nodejs.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── actionlib_generate_messages_py.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── actionlib_msgs_generate_messages_cpp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── actionlib_msgs_generate_messages_eus.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── actionlib_msgs_generate_messages_lisp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── actionlib_msgs_generate_messages_nodejs.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── actionlib_msgs_generate_messages_py.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── clean_test_results.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   └── progress.make
│       │   ├── cmake.check_cache
│       │   ├── download_extra_data.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   └── progress.make
│       │   ├── doxygen.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   └── progress.make
│       │   ├── geometry_msgs_generate_messages_cpp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── geometry_msgs_generate_messages_eus.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── geometry_msgs_generate_messages_lisp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── geometry_msgs_generate_messages_nodejs.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── geometry_msgs_generate_messages_py.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── liancheng_can.dir
│       │   │   ├── CXX.includecache
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   ├── flags.make
│       │   │   ├── link.txt
│       │   │   ├── progress.make
│       │   │   └── src
│       │   │       └── canusb.cpp.o
│       │   ├── liancheng_client.dir
│       │   │   ├── CXX.includecache
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   ├── flags.make
│       │   │   ├── link.txt
│       │   │   ├── progress.make
│       │   │   └── src
│       │   │       ├── TCPClient.cpp.o
│       │   │       └── client.cpp.o
│       │   ├── liancheng_plc.dir
│       │   │   ├── CXX.includecache
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   ├── flags.make
│       │   │   ├── link.txt
│       │   │   ├── progress.make
│       │   │   └── src
│       │   │       └── plc.cpp.o
│       │   ├── liancheng_serial.dir
│       │   │   ├── CXX.includecache
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   ├── flags.make
│       │   │   ├── link.txt
│       │   │   ├── progress.make
│       │   │   └── src
│       │   │       ├── RS485Serial.cpp.o
│       │   │       └── serial.cpp.o
│       │   ├── liancheng_server.dir
│       │   │   ├── CXX.includecache
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   ├── flags.make
│       │   │   ├── link.txt
│       │   │   ├── progress.make
│       │   │   └── src
│       │   │       ├── TCPServer.cpp.o
│       │   │       └── server.cpp.o
│       │   ├── liancheng_socket_gencpp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   └── progress.make
│       │   ├── liancheng_socket_generate_messages.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── liancheng_socket_generate_messages_cpp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── liancheng_socket_generate_messages_eus.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── liancheng_socket_generate_messages_lisp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── liancheng_socket_generate_messages_nodejs.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── liancheng_socket_generate_messages_py.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── liancheng_socket_geneus.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   └── progress.make
│       │   ├── liancheng_socket_genlisp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   └── progress.make
│       │   ├── liancheng_socket_gennodejs.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   └── progress.make
│       │   ├── liancheng_socket_genpy.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   └── progress.make
│       │   ├── progress.marks
│       │   ├── roscpp_generate_messages_cpp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── roscpp_generate_messages_eus.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── roscpp_generate_messages_lisp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── roscpp_generate_messages_nodejs.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── roscpp_generate_messages_py.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── rosgraph_msgs_generate_messages_cpp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── rosgraph_msgs_generate_messages_eus.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── rosgraph_msgs_generate_messages_lisp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── rosgraph_msgs_generate_messages_nodejs.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── rosgraph_msgs_generate_messages_py.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── run_tests.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   └── progress.make
│       │   ├── std_msgs_generate_messages_cpp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── std_msgs_generate_messages_eus.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── std_msgs_generate_messages_lisp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── std_msgs_generate_messages_nodejs.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── std_msgs_generate_messages_py.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── talk_test.dir
│       │   │   ├── CXX.includecache
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   ├── flags.make
│       │   │   ├── link.txt
│       │   │   ├── progress.make
│       │   │   └── src
│       │   │       └── test_talk.cpp.o
│       │   ├── tests.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   └── progress.make
│       │   ├── tf2_msgs_generate_messages_cpp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── tf2_msgs_generate_messages_eus.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── tf2_msgs_generate_messages_lisp.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   ├── tf2_msgs_generate_messages_nodejs.dir
│       │   │   ├── DependInfo.cmake
│       │   │   ├── build.make
│       │   │   ├── cmake_clean.cmake
│       │   │   ├── depend.internal
│       │   │   ├── depend.make
│       │   │   └── progress.make
│       │   └── tf2_msgs_generate_messages_py.dir
│       │       ├── DependInfo.cmake
│       │       ├── build.make
│       │       ├── cmake_clean.cmake
│       │       ├── depend.internal
│       │       ├── depend.make
│       │       └── progress.make
│       ├── CTestConfiguration.ini
│       ├── CTestCustom.cmake
│       ├── CTestTestfile.cmake
│       ├── Makefile
│       ├── atomic_configure
│       │   ├── .rosinstall
│       │   ├── _setup_util.py
│       │   ├── env.sh
│       │   ├── local_setup.bash
│       │   ├── local_setup.sh
│       │   ├── local_setup.zsh
│       │   ├── setup.bash
│       │   ├── setup.sh
│       │   └── setup.zsh
│       ├── catkin
│       │   └── catkin_generated
│       │       └── version
│       │           └── package.cmake
│       ├── catkin_generated
│       │   ├── env_cached.sh
│       │   ├── generate_cached_setup.py
│       │   ├── installspace
│       │   │   ├── .rosinstall
│       │   │   ├── _setup_util.py
│       │   │   ├── env.sh
│       │   │   ├── liancheng_socket-msg-extras.cmake
│       │   │   ├── liancheng_socket-msg-paths.cmake
│       │   │   ├── liancheng_socket.pc
│       │   │   ├── liancheng_socketConfig-version.cmake
│       │   │   ├── liancheng_socketConfig.cmake
│       │   │   ├── local_setup.bash
│       │   │   ├── local_setup.sh
│       │   │   ├── local_setup.zsh
│       │   │   ├── setup.bash
│       │   │   ├── setup.sh
│       │   │   └── setup.zsh
│       │   ├── liancheng_socket-msg-extras.cmake.develspace.in
│       │   ├── liancheng_socket-msg-extras.cmake.installspace.in
│       │   ├── ordered_paths.cmake
│       │   ├── package.cmake
│       │   ├── pkg.develspace.context.pc.py
│       │   ├── pkg.installspace.context.pc.py
│       │   ├── setup_cached.sh
│       │   └── stamps
│       │       └── liancheng_socket
│       │           ├── _setup_util.py.stamp
│       │           ├── interrogate_setup_dot_py.py.stamp
│       │           ├── package.xml.stamp
│       │           ├── pkg-genmsg.cmake.em.stamp
│       │           └── pkg.pc.em.stamp
│       ├── cmake
│       │   ├── liancheng_socket-genmsg-context.py
│       │   └── liancheng_socket-genmsg.cmake
│       ├── cmake_install.cmake
│       └── gtest
│           ├── CMakeFiles
│           │   ├── CMakeDirectoryInformation.cmake
│           │   └── progress.marks
│           ├── CTestTestfile.cmake
│           ├── Makefile
│           ├── cmake_install.cmake
│           ├── googlemock
│           │   ├── CMakeFiles
│           │   │   ├── CMakeDirectoryInformation.cmake
│           │   │   ├── gmock.dir
│           │   │   │   ├── DependInfo.cmake
│           │   │   │   ├── build.make
│           │   │   │   ├── cmake_clean.cmake
│           │   │   │   ├── depend.make
│           │   │   │   ├── flags.make
│           │   │   │   ├── link.txt
│           │   │   │   └── progress.make
│           │   │   ├── gmock_main.dir
│           │   │   │   ├── DependInfo.cmake
│           │   │   │   ├── build.make
│           │   │   │   ├── cmake_clean.cmake
│           │   │   │   ├── depend.make
│           │   │   │   ├── flags.make
│           │   │   │   ├── link.txt
│           │   │   │   └── progress.make
│           │   │   └── progress.marks
│           │   ├── CTestTestfile.cmake
│           │   ├── Makefile
│           │   └── cmake_install.cmake
│           └── googletest
│               ├── CMakeFiles
│               │   ├── CMakeDirectoryInformation.cmake
│               │   ├── gtest.dir
│               │   │   ├── DependInfo.cmake
│               │   │   ├── build.make
│               │   │   ├── cmake_clean.cmake
│               │   │   ├── depend.make
│               │   │   ├── flags.make
│               │   │   ├── link.txt
│               │   │   └── progress.make
│               │   ├── gtest_main.dir
│               │   │   ├── DependInfo.cmake
│               │   │   ├── build.make
│               │   │   ├── cmake_clean.cmake
│               │   │   ├── depend.make
│               │   │   ├── flags.make
│               │   │   ├── link.txt
│               │   │   └── progress.make
│               │   └── progress.marks
│               ├── CTestTestfile.cmake
│               ├── Makefile
│               └── cmake_install.cmake
├── devel
│   ├── .built_by
│   ├── .catkin
│   ├── .private
│   │   ├── catkin_tools_prebuild
│   │   │   ├── .catkin
│   │   │   ├── .rosinstall
│   │   │   ├── _setup_util.py
│   │   │   ├── cmake.lock
│   │   │   ├── env.sh
│   │   │   ├── lib
│   │   │   │   └── pkgconfig
│   │   │   │       └── catkin_tools_prebuild.pc
│   │   │   ├── local_setup.bash
│   │   │   ├── local_setup.sh
│   │   │   ├── local_setup.zsh
│   │   │   ├── setup.bash
│   │   │   ├── setup.sh
│   │   │   ├── setup.zsh
│   │   │   └── share
│   │   │       └── catkin_tools_prebuild
│   │   │           └── cmake
│   │   │               ├── catkin_tools_prebuildConfig-version.cmake
│   │   │               └── catkin_tools_prebuildConfig.cmake
│   │   └── liancheng_socket
│   │       ├── .catkin
│   │       ├── .rosinstall
│   │       ├── _setup_util.py
│   │       ├── cmake.lock
│   │       ├── env.sh
│   │       ├── include
│   │       │   └── liancheng_socket
│   │       │       ├── MotorOrder.h
│   │       │       ├── ReadOutput.h
│   │       │       └── SwitchOrder.h
│   │       ├── lib
│   │       │   ├── liancheng_socket
│   │       │   │   ├── liancheng_can
│   │       │   │   ├── liancheng_client
│   │       │   │   ├── liancheng_plc
│   │       │   │   ├── liancheng_serial
│   │       │   │   ├── liancheng_server
│   │       │   │   └── talk_test
│   │       │   ├── pkgconfig
│   │       │   │   └── liancheng_socket.pc
│   │       │   └── python3
│   │       │       └── dist-packages
│   │       │           └── liancheng_socket
│   │       │               ├── __init__.py
│   │       │               └── msg
│   │       │                   ├── _MotorOrder.py
│   │       │                   ├── _ReadOutput.py
│   │       │                   ├── _SwitchOrder.py
│   │       │                   └── __init__.py
│   │       ├── local_setup.bash
│   │       ├── local_setup.sh
│   │       ├── local_setup.zsh
│   │       ├── setup.bash
│   │       ├── setup.sh
│   │       ├── setup.zsh
│   │       └── share
│   │           ├── common-lisp
│   │           │   └── ros
│   │           │       └── liancheng_socket
│   │           │           └── msg
│   │           │               ├── MotorOrder.lisp
│   │           │               ├── ReadOutput.lisp
│   │           │               ├── SwitchOrder.lisp
│   │           │               ├── _package.lisp
│   │           │               ├── _package_MotorOrder.lisp
│   │           │               ├── _package_ReadOutput.lisp
│   │           │               ├── _package_SwitchOrder.lisp
│   │           │               └── liancheng_socket-msg.asd
│   │           ├── gennodejs
│   │           │   └── ros
│   │           │       └── liancheng_socket
│   │           │           ├── _index.js
│   │           │           └── msg
│   │           │               ├── MotorOrder.js
│   │           │               ├── ReadOutput.js
│   │           │               ├── SwitchOrder.js
│   │           │               └── _index.js
│   │           ├── liancheng_socket
│   │           │   └── cmake
│   │           │       ├── liancheng_socket-msg-extras.cmake
│   │           │       ├── liancheng_socket-msg-paths.cmake
│   │           │       ├── liancheng_socketConfig-version.cmake
│   │           │       └── liancheng_socketConfig.cmake
│   │           └── roseus
│   │               └── ros
│   │                   └── liancheng_socket
│   │                       ├── manifest.l
│   │                       └── msg
│   │                           ├── MotorOrder.l
│   │                           ├── ReadOutput.l
│   │                           └── SwitchOrder.l
│   ├── _setup_util.py
│   ├── cmake.lock
│   ├── env.sh
│   ├── include
│   │   └── liancheng_socket
│   │       ├── MotorOrder.h
│   │       ├── ReadOutput.h
│   │       └── SwitchOrder.h
│   ├── lib
│   │   ├── liancheng_socket
│   │   │   ├── liancheng_can
│   │   │   ├── liancheng_client
│   │   │   ├── liancheng_plc
│   │   │   ├── liancheng_serial
│   │   │   ├── liancheng_server
│   │   │   └── talk_test
│   │   ├── pkgconfig
│   │   │   ├── catkin_tools_prebuild.pc
│   │   │   └── liancheng_socket.pc
│   │   └── python3
│   │       └── dist-packages
│   │           └── liancheng_socket
│   │               ├── __init__.py
│   │               ├── __pycache__
│   │               │   └── __init__.cpython-38.pyc
│   │               └── msg
│   │                   ├── _MotorOrder.py
│   │                   ├── _ReadOutput.py
│   │                   ├── _SwitchOrder.py
│   │                   ├── __init__.py
│   │                   └── __pycache__
│   │                       ├── _MotorOrder.cpython-38.pyc
│   │                       ├── _ReadOutput.cpython-38.pyc
│   │                       ├── _SwitchOrder.cpython-38.pyc
│   │                       └── __init__.cpython-38.pyc
│   ├── local_setup.bash
│   ├── local_setup.sh
│   ├── local_setup.zsh
│   ├── setup.bash
│   ├── setup.sh
│   ├── setup.zsh
│   └── share
│       ├── catkin_tools_prebuild
│       │   └── cmake
│       │       ├── catkin_tools_prebuildConfig-version.cmake
│       │       └── catkin_tools_prebuildConfig.cmake
│       ├── common-lisp
│       │   └── ros
│       │       └── liancheng_socket
│       │           └── msg
│       │               ├── MotorOrder.lisp
│       │               ├── ReadOutput.lisp
│       │               ├── SwitchOrder.lisp
│       │               ├── _package.lisp
│       │               ├── _package_MotorOrder.lisp
│       │               ├── _package_ReadOutput.lisp
│       │               ├── _package_SwitchOrder.lisp
│       │               └── liancheng_socket-msg.asd
│       ├── gennodejs
│       │   └── ros
│       │       └── liancheng_socket
│       │           ├── _index.js
│       │           └── msg
│       │               ├── MotorOrder.js
│       │               ├── ReadOutput.js
│       │               ├── SwitchOrder.js
│       │               └── _index.js
│       ├── liancheng_socket
│       │   └── cmake
│       │       ├── liancheng_socket-msg-extras.cmake
│       │       ├── liancheng_socket-msg-paths.cmake
│       │       ├── liancheng_socketConfig-version.cmake
│       │       └── liancheng_socketConfig.cmake
│       └── roseus
│           └── ros
│               └── liancheng_socket
│                   ├── manifest.l
│                   └── msg
│                       ├── MotorOrder.l
│                       ├── ReadOutput.l
│                       └── SwitchOrder.l
├── logs
│   ├── catkin_tools_prebuild
│   │   ├── build.cache-manifest.000.log
│   │   ├── build.cache-manifest.log
│   │   ├── build.cmake.000.log
│   │   ├── build.cmake.log
│   │   ├── build.loadenv.000.log
│   │   ├── build.loadenv.log
│   │   ├── build.make.000.log
│   │   ├── build.make.log
│   │   ├── build.mkdir.000.log
│   │   ├── build.mkdir.001.log
│   │   ├── build.mkdir.log
│   │   ├── build.symlink.000.log
│   │   └── build.symlink.log
│   └── liancheng_socket
│       ├── build.cache-manifest.000.log
│       ├── build.cache-manifest.log
│       ├── build.cmake.000.log
│       ├── build.cmake.000.log.stderr
│       ├── build.cmake.log
│       ├── build.loadenv.000.log
│       ├── build.loadenv.log
│       ├── build.make.000.log
│       ├── build.make.log
│       ├── build.mkdir.000.log
│       ├── build.mkdir.001.log
│       ├── build.mkdir.log
│       ├── build.symlink.000.log
│       └── build.symlink.log
├── robot.sh
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
└── tree.bak

197 directories, 803 files
```
<!-- readme-tree end -->
