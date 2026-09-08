#!/usr/bin/env python3
"""Lösung zu Übung 06."""

import math

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.parameter import Parameter


def yaw_from_quat(q) -> float:
    siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
    cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
    return math.atan2(siny_cosp, cosy_cosp)


class OdomListener(Node):
    def __init__(self):
        super().__init__('ex06_odom')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        self.sub = self.create_subscription(Odometry, '/odom', self.on_odom, 10)

    def on_odom(self, msg: Odometry):
        pose = msg.pose.pose
        yaw = yaw_from_quat(pose.orientation)
        self.get_logger().info(
            f'x={pose.position.x:.3f} m  y={pose.position.y:.3f} m  yaw={math.degrees(yaw):.1f} deg'
        )


def main(args=None):
    rclpy.init(args=args)
    node = OdomListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
