cmake_minimum_required(VERSION 3.8)
project(ev3_sdf)

find_package(ament_cmake REQUIRED)

install(DIRECTORY models worlds launch
  DESTINATION share/${PROJECT_NAME})

ament_package()
