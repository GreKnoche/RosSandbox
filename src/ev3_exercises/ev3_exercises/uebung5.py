#!/usr/bin/env python3
"""Übung 05: Basics-Strecke abfahren

Ziel: Open-Loop-Sequenz auf /cmd_vel:
  1. Geradeaus durch die gelben Tore
  2. 90° nach links drehen
  3. Geradeaus auf die rote Zielplatte
  4. Stopp

Vorher:
  ./start-simulation.sh

Start:
  ./excercise.sh 5

Strecke (ungefähre Maße):
  Start (grün) bei (0, 0), Blick +x
  Gerade ~1.7 m  →  bei 0.15 m/s etwa 11–12 s
  90° links      →  bei 0.6 rad/s etwa 2.1 s (für die Simulation kalibriert)
  Gerade ~1.5 m  →  bei 0.15 m/s etwa 10 s

Timer: 10 Hz, 1 s = 10 Ticks.
"""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.parameter import Parameter

# Zeit zwischen zwei Timer-Aufrufen in Sekunden.
DT = 0.1


class TrackDriver(Node):
    def __init__(self):
        super().__init__('uebung5')
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        # Der Publisher sendet die Fahrbefehle für jede Phase.
        # LÜCKE 1: Publisher auf '/cmd_vel'
        self.pub = None

        # elapsed speichert, wie viele Sekunden seit dem Start vergangen sind.
        self.elapsed = 0.0

        # Die Strecke wird in drei zeitlich gesteuerte Phasen aufgeteilt.
        # LÜCKE 2: Phasen-Zeiten in Sekunden (Gerade, Drehen, Gerade)
        self.t_straight_1 = 0.0
        self.t_turn = 0.0
        self.t_straight_2 = 0.0

        self.timer = self.create_timer(DT, self.on_timer)
        self.get_logger().info('Strecke: fülle die Lücken und fahre Grün → Tore → Kurve → Rot')

    def on_timer(self):
        """Wählt anhand der vergangenen Zeit den nächsten Fahrbefehl."""
        msg = Twist()
        # t1, t2 und t3 sind die Endzeiten der drei Phasen.
        t1 = self.t_straight_1
        t2 = t1 + self.t_turn
        t3 = t2 + self.t_straight_2

        if self.elapsed < t1:
            # LÜCKE 3: Vorwärts (linear.x ca. 0.15)
            pass
        elif self.elapsed < t2:
            # LÜCKE 4: Linksdrehung (angular.z ca. 0.6, linear.x = 0.0)
            pass
        elif self.elapsed < t3:
            # LÜCKE 5: Wieder vorwärts
            pass
        else:
            # LÜCKE 6: Stopp (0, 0)
            pass

        self.elapsed += DT

        if self.pub is None:
            self.get_logger().warn('LÜCKE 1: Publisher auf /cmd_vel fehlt')
            return
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TrackDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
