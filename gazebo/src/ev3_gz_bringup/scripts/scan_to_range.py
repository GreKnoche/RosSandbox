#!/usr/bin/env python3
"""Convert the Gazebo ultrasonic gpu_lidar scan into sensor_msgs/Range."""

from __future__ import annotations

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Range


class ScanToRange(Node):
    def __init__(self) -> None:
        super().__init__("scan_to_range")
        self.declare_parameter("min_range", 0.03)
        self.declare_parameter("max_range", 2.55)
        self.declare_parameter("field_of_view", 0.5)
        self.min_range = float(self.get_parameter("min_range").value)
        self.max_range = float(self.get_parameter("max_range").value)
        self.fov = float(self.get_parameter("field_of_view").value)
        self.pub = self.create_publisher(Range, "ultrasonic", 10)
        self.create_subscription(LaserScan, "ultrasonic/scan", self._on_scan, 10)

    def _on_scan(self, scan: LaserScan) -> None:
        hits = [
            r
            for r in scan.ranges
            if math.isfinite(r) and r >= self.min_range
        ]
        rng = Range()
        rng.header = scan.header
        rng.header.frame_id = "ultrasonic_link"
        rng.radiation_type = Range.ULTRASOUND
        rng.field_of_view = self.fov
        rng.min_range = self.min_range
        rng.max_range = self.max_range
        rng.range = min(hits) if hits else self.max_range
        if rng.range > self.max_range:
            rng.range = self.max_range
        self.pub.publish(rng)


def main() -> None:
    rclpy.init()
    node = ScanToRange()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
