#!/usr/bin/env python3
"""Übung 04: Zeitgesteuert fahren und stoppen

Ziel: Ein paar Sekunden vorwärts fahren, danach Twist (0, 0) senden.

Vorher:
  ros2 launch ev3_sdf sim.launch.py

Start:
  ros2 run ev3_exercises ex04_timed_move

Der Timer läuft mit 10 Hz. 30 Ticks = 3.0 s.
"""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.parameter import Parameter


class TimedMove(Node):
    def __init__(self):
        super().__init__('ex04_timed_move')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        # LÜCKE 1: Publisher auf '/cmd_vel'
        self.pub = None

        self.ticks = 0
        # LÜCKE 2: Wie viele Timer-Ticks fahren, bevor gestoppt wird?
        # 10 Hz → 30 Ticks = 3 Sekunden
        self.drive_ticks = 0

        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        msg = Twist()
        if self.ticks < self.drive_ticks:
            # LÜCKE 3: Vorwärtsgeschwindigkeit setzen
            pass
        else:
            # LÜCKE 4: Stopp — linear.x und angular.z auf 0.0
            if self.ticks == self.drive_ticks:
                self.get_logger().info('Stopp')
        self.ticks += 1

        if self.pub is None:
            self.get_logger().warn('LÜCKE 1: Publisher auf /cmd_vel fehlt')
            return
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TimedMove()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
