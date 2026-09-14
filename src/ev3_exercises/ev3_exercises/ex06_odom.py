#!/usr/bin/env python3
"""Übung 06: Odometrie lesen

Ziel: nav_msgs/Odometry auf /odom abonnieren und die Pose loggen.

Vorher:
  ros2 launch ev3_sdf sim.launch.py
  optional parallel: ros2 run ev3_exercises ex02_drive_forward
    (bzw. die Lösung, damit sich die Pose ändert)

Start:
  ros2 run ev3_exercises ex06_odom
"""

import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from rclpy.parameter import Parameter


class OdomListener(Node):
    def __init__(self):
        super().__init__('ex06_odom')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        # LÜCKE 1: Subscriber auf '/odom', Typ Odometry, Callback self.on_odom
        # self.sub = self.create_subscription(...)

    def on_odom(self, msg: Odometry):
        pose = msg.pose.pose
        # LÜCKE 2: x, y und Orientierung loggen
        # pose.position.x, pose.position.y, pose.orientation.z / pose.orientation.w
        _ = pose


def main(args=None):
    rclpy.init(args=args)
    node = OdomListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
