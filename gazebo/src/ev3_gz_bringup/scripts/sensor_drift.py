#!/usr/bin/env python3
"""Republish Gazebo odom/IMU onto the Nav2 contract, with optional drift.

Ground truth stays on /odom/perfect and /imu/perfect. This node publishes
/odom, /imu, and TF odom -> base_link. With both switches off it is a
passthrough, so the sim matches today's contract.
"""

from __future__ import annotations

import copy
import math

import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import Odometry
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from sensor_msgs.msg import Imu
from tf2_ros import TransformBroadcaster


def _as_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def _stamp_sec(stamp) -> float:
    return float(stamp.sec) + float(stamp.nanosec) * 1e-9


def wrap_angle(angle: float) -> float:
    """Wrap radians to (-pi, pi]."""
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


def yaw_from_quaternion(x: float, y: float, z: float, w: float) -> float:
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.atan2(siny_cosp, cosy_cosp)


def yaw_to_quaternion(yaw: float) -> tuple[float, float, float, float]:
    half = yaw * 0.5
    return (0.0, 0.0, math.sin(half), math.cos(half))


class SensorDrift(Node):
    def __init__(self) -> None:
        super().__init__("sensor_drift")
        self.declare_parameter("odom_drift", False)
        self.declare_parameter("gyro_drift", False)
        self.declare_parameter("linear_scale", 1.04)
        self.declare_parameter("angular_scale", 1.06)
        self.declare_parameter("gyro_bias_deg_s", 0.5)

        self._odom_drift = _as_bool(self.get_parameter("odom_drift").value)
        self._gyro_drift = _as_bool(self.get_parameter("gyro_drift").value)
        self._linear_scale = float(self.get_parameter("linear_scale").value)
        self._angular_scale = float(self.get_parameter("angular_scale").value)
        self._gyro_bias_deg_s = float(self.get_parameter("gyro_bias_deg_s").value)

        self._x = 0.0
        self._y = 0.0
        self._theta = 0.0
        self._last_odom_t: float | None = None
        self._extra_yaw = 0.0
        self._last_imu_t: float | None = None

        self._tf = TransformBroadcaster(self)
        self._odom_pub = self.create_publisher(Odometry, "odom", 10)
        self._imu_pub = self.create_publisher(Imu, "imu", 10)
        self.create_subscription(Odometry, "odom/perfect", self._on_odom, 10)
        self.create_subscription(Imu, "imu/perfect", self._on_imu, 10)
        self.add_on_set_parameters_callback(self._on_set_params)
        self.get_logger().info(
            f"odom_drift={self._odom_drift} gyro_drift={self._gyro_drift} "
            f"linear_scale={self._linear_scale} angular_scale={self._angular_scale} "
            f"gyro_bias_deg_s={self._gyro_bias_deg_s}"
        )

    def _on_set_params(self, params) -> SetParametersResult:
        for param in params:
            if param.name == "odom_drift":
                new = _as_bool(param.value)
                if new and not self._odom_drift:
                    self._last_odom_t = None
                self._odom_drift = new
            elif param.name == "gyro_drift":
                new = _as_bool(param.value)
                if new and not self._gyro_drift:
                    self._extra_yaw = 0.0
                    self._last_imu_t = None
                self._gyro_drift = new
            elif param.name == "linear_scale":
                self._linear_scale = float(param.value)
            elif param.name == "angular_scale":
                self._angular_scale = float(param.value)
            elif param.name == "gyro_bias_deg_s":
                self._gyro_bias_deg_s = float(param.value)
        return SetParametersResult(successful=True)

    def _seed_odom(self, msg: Odometry) -> None:
        pose = msg.pose.pose
        self._x = pose.position.x
        self._y = pose.position.y
        q = pose.orientation
        self._theta = yaw_from_quaternion(q.x, q.y, q.z, q.w)

    def _on_odom(self, msg: Odometry) -> None:
        out = copy.deepcopy(msg)
        now = _stamp_sec(msg.header.stamp)
        if self._odom_drift:
            if self._last_odom_t is None:
                self._seed_odom(msg)
            else:
                dt = now - self._last_odom_t
                if dt > 0.25:
                    self._seed_odom(msg)
                elif dt > 0.0:
                    ds = self._linear_scale * msg.twist.twist.linear.x * dt
                    dtheta = self._angular_scale * msg.twist.twist.angular.z * dt
                    mid = self._theta + 0.5 * dtheta
                    self._x += ds * math.cos(mid)
                    self._y += ds * math.sin(mid)
                    self._theta = wrap_angle(self._theta + dtheta)
            self._last_odom_t = now
            qx, qy, qz, qw = yaw_to_quaternion(self._theta)
            out.pose.pose.position.x = self._x
            out.pose.pose.position.y = self._y
            out.pose.pose.orientation.x = qx
            out.pose.pose.orientation.y = qy
            out.pose.pose.orientation.z = qz
            out.pose.pose.orientation.w = qw
            out.twist.twist.linear.x = self._linear_scale * msg.twist.twist.linear.x
            out.twist.twist.angular.z = self._angular_scale * msg.twist.twist.angular.z
        else:
            self._last_odom_t = None
            self._seed_odom(msg)

        self._odom_pub.publish(out)
        self._broadcast_tf(out)

    def _broadcast_tf(self, odom: Odometry) -> None:
        tf_msg = TransformStamped()
        tf_msg.header = odom.header
        tf_msg.child_frame_id = odom.child_frame_id or "base_link"
        tf_msg.transform.translation.x = odom.pose.pose.position.x
        tf_msg.transform.translation.y = odom.pose.pose.position.y
        tf_msg.transform.translation.z = odom.pose.pose.position.z
        tf_msg.transform.rotation = odom.pose.pose.orientation
        self._tf.sendTransform(tf_msg)

    def _on_imu(self, msg: Imu) -> None:
        out = copy.deepcopy(msg)
        now = _stamp_sec(msg.header.stamp)
        if self._gyro_drift:
            if self._last_imu_t is not None:
                dt = now - self._last_imu_t
                if 0.0 < dt <= 0.25:
                    self._extra_yaw += math.radians(self._gyro_bias_deg_s) * dt
            self._last_imu_t = now
            q = msg.orientation
            yaw = yaw_from_quaternion(q.x, q.y, q.z, q.w) + self._extra_yaw
            gx, gy, gz, gw = yaw_to_quaternion(wrap_angle(yaw))
            out.orientation.x = gx
            out.orientation.y = gy
            out.orientation.z = gz
            out.orientation.w = gw
            out.angular_velocity.z = msg.angular_velocity.z + math.radians(
                self._gyro_bias_deg_s
            )
        else:
            self._extra_yaw = 0.0
            self._last_imu_t = None
        self._imu_pub.publish(out)


def main() -> None:
    rclpy.init()
    node = SensorDrift()
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
