#!/usr/bin/env python3
"""Übung 01: Hello-Node

Ziel: Einen ROS-2-Node starten, der regelmäßig eine Logzeile ausgibt.

Vorher: nichts (Gazebo nicht nötig).

Start:
  ros2 run ev3_exercises ex01_hello
"""

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter


class HelloNode(Node):
    def __init__(self):
        super().__init__('ex01_hello')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        # LÜCKE 1: Timer mit 1.0 s Periode, Callback self.on_timer
        # self.timer = self.create_timer(...)

    def on_timer(self):
        # LÜCKE 2: Info-Log, z. B. "Hallo EV3-Sandbox"
        pass


def main(args=None):
    rclpy.init(args=args)
    node = HelloNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
