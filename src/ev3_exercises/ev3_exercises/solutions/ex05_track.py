#!/usr/bin/env python3
"""Lösung zu Übung 05: Grün → Tore → 90° links → rote Zielplatte."""

import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.parameter import Parameter

DT = 0.1
LINEAR = 0.15
ANGULAR = 0.6


class TrackDriver(Node):
    def __init__(self):
        super().__init__('ex05_track')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.elapsed = 0.0
        self.t_straight_1 = 11.5
        self.t_turn = (math.pi / 2.0) / ANGULAR
        self.t_straight_2 = 10.5
        self.timer = self.create_timer(DT, self.on_timer)
        self.get_logger().info(
            f'Strecke: {self.t_straight_1:.1f}s gerade, '
            f'{self.t_turn:.2f}s drehen, {self.t_straight_2:.1f}s gerade'
        )

    def on_timer(self):
        msg = Twist()
        t1 = self.t_straight_1
        t2 = t1 + self.t_turn
        t3 = t2 + self.t_straight_2

        if self.elapsed < t1:
            msg.linear.x = LINEAR
            msg.angular.z = 0.0
        elif self.elapsed < t2:
            msg.linear.x = 0.0
            msg.angular.z = ANGULAR
        elif self.elapsed < t3:
            msg.linear.x = LINEAR
            msg.angular.z = 0.0
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0

        self.elapsed += DT
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TrackDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
