#!/usr/bin/env python3
"""Schaltet die EV3-LED über /led (std_msgs/Bool) in Gazebo um."""

import rclpy
from rclpy.node import Node
from ros_gz_interfaces.msg import Entity, Light, MaterialColor
from std_msgs.msg import Bool, ColorRGBA


def rgba(r: float, g: float, b: float, a: float = 1.0) -> ColorRGBA:
    c = ColorRGBA()
    c.r, c.g, c.b, c.a = r, g, b, a
    return c


class LedRelay(Node):
    def __init__(self):
        super().__init__('led_relay')
        self.mat_pub = self.create_publisher(
            MaterialColor, '/world/basics_track/material_color', 10)
        self.light_pub = self.create_publisher(
            Light, '/world/basics_track/light_config', 10)
        self.create_subscription(Bool, '/led', self.on_led, 10)

    def on_led(self, msg: Bool):
        on = msg.data
        mat = MaterialColor()
        mat.entity.name = 'led'
        mat.entity.type = Entity.VISUAL
        mat.entity_match = MaterialColor.ALL
        if on:
            color = rgba(1.0, 0.12, 0.08)
            emit = rgba(1.0, 0.22, 0.08)
        else:
            color = rgba(0.25, 0.04, 0.04)
            emit = rgba(0.0, 0.0, 0.0)
        mat.ambient = color
        mat.diffuse = color
        mat.specular = rgba(0.4, 0.08, 0.05)
        mat.emissive = emit
        self.mat_pub.publish(mat)

        light = Light()
        light.name = 'led_light'
        light.type = Light.POINT
        light.intensity = 2.0 if on else 0.0
        light.range = 0.35
        light.cast_shadows = False
        light.diffuse = rgba(1.0, 0.15, 0.1) if on else rgba(0.0, 0.0, 0.0)
        self.light_pub.publish(light)


def main(args=None):
    rclpy.init(args=args)
    node = LedRelay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
