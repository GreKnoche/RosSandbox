#!/usr/bin/env python3
"""Übung 02: Vorwärtsfahren mit /cmd_vel

Ziel: geometry_msgs/Twist auf /cmd_vel veröffentlichen, linear.x setzen.

Vorher:
  ros2 launch ev3_sdf sim.launch.py

Start:
  ros2 run ev3_exercises ex02_drive_forward

Hinweis: EV3 langsam fahren, ca. 0.15 m/s. Zum Stoppen Strg+C und ggf.
  ros2 topic pub --once /cmd_vel geometry_msgs/Twist "{}"
"""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.parameter import Parameter


class DriveForward(Node):
    def __init__(self):
        super().__init__('ex02_drive_forward')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        # LÜCKE 1: Publisher anlegen (Typ Twist, Topic '/cmd_vel', Queue 10)
        self.pub = None

        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        msg = Twist()
        # LÜCKE 2: Geradeausgeschwindigkeit in m/s (ca. 0.15), angular.z = 0.0
        # msg.linear.x = ...
        # msg.angular.z = ...

        if self.pub is None:
            self.get_logger().warn('LÜCKE 1: Publisher auf /cmd_vel fehlt')
            return
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = DriveForward()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
