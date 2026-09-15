#!/usr/bin/env python3
"""Übung 01: Hello-Node — rote LED blinken

Ziel: Einen ROS-2-Node starten, der per Timer die LED auf dem EV3 umschaltet.

Vorher:
  ./start-simulation.sh

Start:
  ./excercise.sh 1

Die LED hört auf /led (std_msgs/Bool): True = an, False = aus.
"""

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
        """
        Timer sind dazu da regelmäßig Daten einzuholen, oder Befehle auszuführen.
        """
        # LÜCKE 1: Timer mit 1.0 s Periode, Callback self.on_timer
        # self.timer = self.create_timer(...)

    def on_timer(self):
        """
        
        """
        # LÜCKE 2: LED umschalten und auf /led publishen
        # self.on = ...
        # msg = Bool()
        # msg.data = ...
        # self.pub.publish(msg)
        pass


def main(args=None):
    rclpy.init(args=args)
    node = HelloNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
