cmake_minimum_required(VERSION 3.8)
project(ev3_gz_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY models/
  DESTINATION share/${PROJECT_NAME}/models
)
install(
  DIRECTORY urdf/
  DESTINATION share/${PROJECT_NAME}/urdf
)

ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.dsv.in")
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.sh.in")

ament_package()
