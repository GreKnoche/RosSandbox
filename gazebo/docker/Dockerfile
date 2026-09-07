FROM osrf/ros:jazzy-desktop

ENV DEBIAN_FRONTEND=noninteractive
ENV GZ_VERSION=harmonic

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-ros-gz \
    ros-jazzy-ros-gz-sim \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-sdformat-urdf \
    ros-jazzy-teleop-twist-keyboard \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ws
COPY src /ws/src

SHELL ["/bin/bash", "-c"]
RUN source /opt/ros/jazzy/setup.bash && colcon build --symlink-install

CMD ["bash", "-lc", "source /opt/ros/jazzy/setup.bash && source /ws/install/setup.bash && ros2 launch ev3_gz_bringup sim.launch.py"]
