#!/usr/bin/env python3
"""Lösung zu Übung 03."""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.parameter import Parameter


class TurnNode(Node):
    def __init__(self):
        super().__init__('ex03_turn')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.6
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TurnNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
