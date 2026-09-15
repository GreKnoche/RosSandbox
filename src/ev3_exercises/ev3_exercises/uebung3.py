#!/usr/bin/env python3
"""Übung 03: Drehen mit /cmd_vel

Ziel: Auf der Stelle drehen über Twist.angular.z.

Vorher:
  ros2 launch ev3_sdf sim.launch.py

Start:
  ./excercise.sh 3

Hinweis: Positives angular.z dreht nach links (Gegenuhrzeigersinn).
Ca. 0.6 rad/s ist für den EV3 ein guter Startwert.
"""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.parameter import Parameter


class TurnNode(Node):
    def __init__(self):
        super().__init__('uebung3')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        # Der Publisher sendet Fahrbefehle an den Roboter.
        # LÜCKE 1: Publisher auf '/cmd_vel', Typ Twist
        self.pub = None

        # Alle 0.1 Sekunden wird ein neuer Fahrbefehl erzeugt.
        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        """Bei Twist steuert angular.z die Drehung um die senkrechte Achse."""
        msg = Twist()
        # LÜCKE 2: linear.x = 0.0 (auf der Stelle), angular.z setzen (ca. 0.6)
        # msg.linear.x = ...
        # msg.angular.z = ...

        if self.pub is None:
            self.get_logger().warn('LÜCKE 1: Publisher auf /cmd_vel fehlt')
            return
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TurnNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
