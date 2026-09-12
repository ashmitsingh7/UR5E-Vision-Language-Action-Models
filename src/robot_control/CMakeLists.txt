cmake_minimum_required(VERSION 3.5)
project(ur5e_robot_control)

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)
find_package(tf2_ros REQUIRED)

# Python dependencies
ament_python_install_package(${PROJECT_NAME})

# Install launch files
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/launch
)

# Install config files
install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}/config
)

# Install scripts
install(PROGRAMS
  scripts/target_pose_publisher.py
  scripts/trajectory_executor.py
  scripts/verify_tf_tree.sh
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
