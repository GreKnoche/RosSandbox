#!/usr/bin/env python3
"""Startet Gazebo Harmonic mit EV3, Basics-Strecke und ROS-GZ-Bridge."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node, SetParameter


def generate_launch_description():
    pkg_share = get_package_share_directory('ev3_sdf')
    world_path = os.path.join(pkg_share, 'worlds', 'basics_track.sdf')
    models_path = os.path.join(pkg_share, 'models')

    gz_resource = models_path
    existing = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    if existing:
        gz_resource = models_path + os.pathsep + existing

    use_sim_time = LaunchConfiguration('use_sim_time')

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py',
            )
        ),
        launch_arguments={'gz_args': ['-r ', world_path]}.items(),
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
        ],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Uhr von Gazebo (/clock) verwenden',
        ),
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH', gz_resource),
        SetParameter(name='use_sim_time', value=use_sim_time),
        gz_sim,
        bridge,
    ])
