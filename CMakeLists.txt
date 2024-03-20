cmake_minimum_required(VERSION 3.5)
project(ros_engine_sound_sim)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package(${PROJECT_NAME} SCRIPTS_DESTINATION lib/${PROJECT_NAME})

## install
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  nodes/ros_engine_sound_sim
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()