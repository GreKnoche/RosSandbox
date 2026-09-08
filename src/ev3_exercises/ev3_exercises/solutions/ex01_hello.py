#!/usr/bin/env python3
"""Lösung zu Übung 01."""

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter


class HelloNode(Node):
    def __init__(self):
        super().__init__('ex01_hello')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        self.get_logger().info('Hallo EV3-Sandbox')


def main(args=None):
    rclpy.init(args=args)
    node = HelloNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
