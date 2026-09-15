#!/usr/bin/env python3
"""Übung 04: Zeitgesteuert fahren und stoppen

Ziel: Ein paar Sekunden vorwärts fahren, danach Twist (0, 0) senden.

Vorher:
  ./start-simulation.sh

Start:
  ./excercise.sh 4

Der Timer läuft mit 10 Hz. 30 Ticks = 3.0 s.
"""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.parameter import Parameter


class TimedMove(Node):
    def __init__(self):
        super().__init__('uebung4')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        # Der Publisher sendet die Geschwindigkeit auf /cmd_vel.
        # LÜCKE 1: Publisher auf '/cmd_vel'
        self.pub = None

        # ticks zählt, wie oft der Timer bereits aufgerufen wurde.
        self.ticks = 0
        # LÜCKE 2: Wie viele Timer-Ticks fahren, bevor gestoppt wird?
        # 10 Hz → 30 Ticks = 3 Sekunden
        self.drive_ticks = 0

        # 0.1 Sekunden pro Aufruf entsprechen 10 Aufrufen pro Sekunde.
        self.timer = self.create_timer(0.1, self.on_timer)

    def on_timer(self):
        """Sendet zuerst einen Fahrbefehl und danach einen Stoppbefehl."""
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
