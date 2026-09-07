cmake_minimum_required(VERSION 3.8)
project(ev3_gz_gazebo)

find_package(ament_cmake REQUIRED)
find_package(ev3_gz_description REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

set(GEN_DIR "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(GEN_WORLD "${GEN_DIR}/worlds/ev3_lab.sdf")
set(GEN_TEX "${GEN_DIR}/textures/baseplate.png")

add_custom_command(
  OUTPUT "${GEN_WORLD}" "${GEN_TEX}"
  COMMAND
    "${Python3_EXECUTABLE}"
    "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate_ev3_lab.py"
    --out "${GEN_DIR}"
  DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/scripts/generate_ev3_lab.py"
  COMMENT "Generating EV3 LEGO lab world and baseplate texture"
  VERBATIM
)

add_custom_target(ev3_lab_assets ALL DEPENDS "${GEN_WORLD}" "${GEN_TEX}")

install(FILES "${GEN_WORLD}" DESTINATION share/${PROJECT_NAME}/worlds)
install(FILES "${GEN_TEX}" DESTINATION share/${PROJECT_NAME}/textures)

ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.dsv.in")
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.sh.in")

ament_package()
