#!/usr/bin/env python3
"""Lösung zu Übung 04."""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.parameter import Parameter


class TimedMove(Node):
    def __init__(self):
        super().__init__('ex04_timed_move')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.ticks = 0
        self.drive_ticks = 30
        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        msg = Twist()
        if self.ticks < self.drive_ticks:
            msg.linear.x = 0.15
            msg.angular.z = 0.0
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            if self.ticks == self.drive_ticks:
                self.get_logger().info('Stopp')
        self.ticks += 1
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TimedMove()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
