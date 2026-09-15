#!/usr/bin/env python3
"""Lösung zu Übung 01."""

import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_msgs.msg import Bool


class HelloNode(Node):
    def __init__(self):
        super().__init__('uebung1')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        self.pub = self.create_publisher(Bool, '/led', 10)
        self.on = False
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        self.on = not self.on
        msg = Bool()
        msg.data = self.on
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = HelloNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
