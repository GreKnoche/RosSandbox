"""Launch Gazebo Harmonic and bridge it onto the EV3 Nav2 robot contract."""

from __future__ import annotations

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description() -> LaunchDescription:
    pkg_bringup = get_package_share_directory("ev3_gz_bringup")
    pkg_gazebo = get_package_share_directory("ev3_gz_gazebo")
    pkg_description = get_package_share_directory("ev3_gz_description")
    pkg_ros_gz_sim = get_package_share_directory("ros_gz_sim")

    urdf_file = os.path.join(pkg_description, "urdf", "ev3.urdf")
    with open(urdf_file, encoding="utf-8") as handle:
        robot_desc = handle.read()

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            "gz_args": [
                LaunchConfiguration("gz_args_prefix"),
                PathJoinSubstitution([pkg_gazebo, "worlds", "ev3_lab.sdf"]),
            ]
        }.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {"use_sim_time": True},
            {"robot_description": robot_desc},
        ],
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[
            {
                "config_file": os.path.join(pkg_bringup, "config", "bridge.yaml"),
                "qos_overrides./tf_static.publisher.durability": "transient_local",
            }
        ],
        output="screen",
    )

    scan_to_range = Node(
        package="ev3_gz_bringup",
        executable="scan_to_range.py",
        name="scan_to_range",
        output="screen",
        parameters=[{"use_sim_time": True}],
    )

    sensor_drift = Node(
        package="ev3_gz_bringup",
        executable="sensor_drift.py",
        name="sensor_drift",
        output="screen",
        parameters=[
            {
                "use_sim_time": True,
                "odom_drift": ParameterValue(
                    LaunchConfiguration("odom_drift"), value_type=bool
                ),
                "gyro_drift": ParameterValue(
                    LaunchConfiguration("gyro_drift"), value_type=bool
                ),
            }
        ],
    )

    teleop = Node(
        package="teleop_twist_keyboard",
        executable="teleop_twist_keyboard",
        name="teleop_twist_keyboard",
        output="screen",
        emulate_tty=True,
        parameters=[{"use_sim_time": True, "stamped": False}],
        condition=IfCondition(LaunchConfiguration("teleop")),
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        condition=IfCondition(LaunchConfiguration("rviz")),
    )

    return LaunchDescription(
        [
            SetEnvironmentVariable("GZ_IP", os.environ.get("GZ_IP", "127.0.0.1")),
            SetEnvironmentVariable(
                "GZ_PARTITION", os.environ.get("GZ_PARTITION", "ev3")
            ),
            SetEnvironmentVariable(
                "FASTDDS_BUILTIN_TRANSPORTS",
                os.environ.get("FASTDDS_BUILTIN_TRANSPORTS", "UDPv4"),
            ),
            DeclareLaunchArgument(
                "gz_args_prefix",
                default_value="-r ",
                description="Prefix for gz sim args. Use '-s -r ' for headless.",
            ),
            DeclareLaunchArgument(
                "rviz",
                default_value="false",
                description="Open RViz2 (off by default).",
            ),
            DeclareLaunchArgument(
                "teleop",
                default_value="false",
                description="Open teleop_twist_keyboard (default off so Docker compose keeps the TTY).",
            ),
            DeclareLaunchArgument(
                "odom_drift",
                default_value="false",
                description="Scale-error wheel odometry on /odom and odom -> base_link.",
            ),
            DeclareLaunchArgument(
                "gyro_drift",
                default_value="false",
                description="Constant yaw-rate bias on /imu heading.",
            ),
            gz_sim,
            bridge,
            scan_to_range,
            sensor_drift,
            robot_state_publisher,
            teleop,
            rviz,
        ]
    )
