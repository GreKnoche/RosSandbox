#!/usr/bin/env python3
"""Generate the EV3 lab world: studded baseplate PNG, LEGO-like bricks, WASD driving."""

from __future__ import annotations

import argparse
import math
import struct
import zlib
from pathlib import Path

MODULE = 0.008  # Technic / stud pitch (m)
BRICK_H = 0.0096
PLATE_STUDS = 160  # 5 × 32-stud baseplates → 1.28 m
PLATE_M = PLATE_STUDS * MODULE
PNG_SIZE = 2048

COLORS = {
    "red": (0.79, 0.10, 0.09),
    "yellow": (0.95, 0.76, 0.20),
    "blue": (0.00, 0.34, 0.75),
    "green": (0.00, 0.52, 0.24),
    "grey": (0.62, 0.63, 0.64),
}

# Gazebo GUI key codes (Qt): W A S D X
KEY_W, KEY_A, KEY_S, KEY_D, KEY_X = 87, 65, 83, 68, 88


def write_png_rgb(path: Path, width: int, height: int, pixels: bytearray) -> None:
    """Write an RGB888 PNG with only the stdlib (no Pillow)."""

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        raw.extend(pixels[y * stride : (y + 1) * stride])
    compressed = zlib.compress(bytes(raw), 9)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", compressed)
        + chunk(b"IEND", b"")
    )


def render_baseplate(size: int, studs: int) -> bytearray:
    """Grey 32-stud-style plate with circular studs."""
    base = (158, 161, 165)
    groove = (132, 135, 138)
    stud = (186, 189, 192)
    rim = (118, 121, 124)
    highlight = (214, 216, 218)
    pixels = bytearray(size * size * 3)
    pitch = size / studs
    radius = pitch * 0.28
    rim_r = radius + pitch * 0.04

    def put(x: int, y: int, rgb: tuple[int, int, int]) -> None:
        if 0 <= x < size and 0 <= y < size:
            i = (y * size + x) * 3
            pixels[i : i + 3] = bytes(rgb)

    for i in range(0, len(pixels), 3):
        pixels[i : i + 3] = bytes(base)

    # Faint grid in the grooves between studs.
    for s in range(studs + 1):
        line = int(round(s * pitch))
        for x in range(size):
            put(x, min(line, size - 1), groove)
        for y in range(size):
            put(min(line, size - 1), y, groove)

    for sy in range(studs):
        cy = (sy + 0.5) * pitch
        for sx in range(studs):
            cx = (sx + 0.5) * pitch
            x0 = max(0, int(cx - rim_r - 1))
            x1 = min(size - 1, int(cx + rim_r + 1))
            y0 = max(0, int(cy - rim_r - 1))
            y1 = min(size - 1, int(cy + rim_r + 1))
            for y in range(y0, y1 + 1):
                dy = y + 0.5 - cy
                for x in range(x0, x1 + 1):
                    dx = x + 0.5 - cx
                    d = math.hypot(dx, dy)
                    if d <= radius:
                        shade = highlight if (dx + dy) < -radius * 0.25 else stud
                        put(x, y, shade)
                    elif d <= rim_r:
                        put(x, y, rim)
    return pixels


def sdf_color(rgb: tuple[float, float, float]) -> str:
    r, g, b = rgb
    return f"{r:.3f} {g:.3f} {b:.3f} 1"


def brick_model(
    name: str,
    x: float,
    y: float,
    yaw: float,
    studs_x: int,
    studs_y: int,
    color: str,
    layer: int = 0,
) -> str:
    sx = studs_x * MODULE
    sy = studs_y * MODULE
    z = BRICK_H * (layer + 0.5)
    r, g, b = COLORS[color]
    dark = (max(0.0, r * 0.65), max(0.0, g * 0.65), max(0.0, b * 0.65))
    return f"""
    <model name="{name}">
      <static>true</static>
      <pose>{x:.5f} {y:.5f} {z:.5f} 0 0 {yaw:.5f}</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box><size>{sx:.5f} {sy:.5f} {BRICK_H:.5f}</size></box>
          </geometry>
        </collision>
        <visual name="body">
          <geometry>
            <box><size>{sx:.5f} {sy:.5f} {BRICK_H:.5f}</size></box>
          </geometry>
          <material>
            <ambient>{sdf_color(dark)}</ambient>
            <diffuse>{sdf_color(COLORS[color])}</diffuse>
            <specular>0.15 0.15 0.15 1</specular>
          </material>
        </visual>
        <visual name="tubes">
          <pose>0 0 {BRICK_H * 0.42:.5f} 0 0 0</pose>
          <geometry>
            <box><size>{sx * 0.92:.5f} {sy * 0.92:.5f} {BRICK_H * 0.12:.5f}</size></box>
          </geometry>
          <material>
            <ambient>{sdf_color(COLORS[color])}</ambient>
            <diffuse>{sdf_color(tuple(min(1.0, c * 1.12) for c in COLORS[color]))}</diffuse>
          </material>
        </visual>
      </link>
    </model>"""


def border_bricks() -> str:
    """One-brick-tall 2x8 (and 2x4) ring around the plate."""
    half = PLATE_M / 2
    chunks: list[str] = []
    length_8 = 8 * MODULE
    width_2 = 2 * MODULE
    # Along ±Y edges, long axis = X (2×8 with sy=2, sx=8).
    n_long = PLATE_STUDS // 8
    for edge, y_sign in (("n", 1.0), ("s", -1.0)):
        y = y_sign * (half - width_2 / 2)
        for i in range(n_long):
            x = -half + length_8 / 2 + i * length_8
            color = "red" if (i + (0 if y_sign > 0 else 1)) % 2 == 0 else "grey"
            chunks.append(
                brick_model(f"border_{edge}_{i}", x, y, 0.0, 8, 2, color)
            )
    # Along ±X edges, skip the 2-stud corners already filled by the Y walls.
    inner_studs = PLATE_STUDS - 4
    n_side = inner_studs // 8
    remainder = inner_studs - n_side * 8
    for edge, x_sign in (("e", 1.0), ("w", -1.0)):
        x = x_sign * (half - width_2 / 2)
        cursor = -half + 2 * MODULE
        for i in range(n_side):
            y = cursor + length_8 / 2
            color = "blue" if (i + (0 if x_sign > 0 else 1)) % 2 == 0 else "yellow"
            chunks.append(
                brick_model(f"border_{edge}_{i}", x, y, 1.5708, 8, 2, color)
            )
            cursor += length_8
        if remainder >= 4:
            y = cursor + 4 * MODULE / 2
            chunks.append(
                brick_model(f"border_{edge}_end", x, y, 1.5708, 4, 2, "green")
            )
    return "\n".join(chunks)


def obstacle_bricks() -> str:
    """A few stacks in front of the ultrasonic (+X) and to the sides."""
    parts = [
        # Short red wall ahead of the robot.
        brick_model("stack_red_0", 0.40, 0.00, 1.5708, 8, 2, "red", 0),
        brick_model("stack_red_1", 0.40, 0.00, 1.5708, 8, 2, "red", 1),
        brick_model("stack_red_2", 0.40, 0.00, 1.5708, 8, 2, "red", 2),
        brick_model("stack_red_3", 0.40, 0.00, 1.5708, 8, 2, "red", 3),
        # Yellow 2×8 lying as a low barrier.
        brick_model("bar_yellow", 0.32, 0.22, 0.4, 8, 2, "yellow", 0),
        brick_model("bar_yellow_1", 0.32, 0.22, 0.4, 8, 2, "yellow", 1),
        # Blue cube-ish stack to the right.
        brick_model("stack_blue_0", 0.24, -0.28, 0.0, 4, 2, "blue", 0),
        brick_model("stack_blue_1", 0.24, -0.28, 0.0, 4, 2, "blue", 1),
        brick_model("stack_blue_2", 0.24, -0.28, 0.0, 4, 2, "blue", 2),
        # Green 2×4 behind-left so turning has something to see.
        brick_model("stack_green_0", -0.36, 0.28, 0.0, 4, 2, "green", 0),
        brick_model("stack_green_1", -0.36, 0.28, 0.0, 4, 2, "green", 1),
    ]
    return "\n".join(parts)


def triggered_publisher(key: int, twist_body: str) -> str:
    return f"""
    <plugin filename="gz-sim-triggered-publisher-system"
            name="gz::sim::systems::TriggeredPublisher">
      <input type="gz.msgs.Int32" topic="/keyboard/keypress">
        <match field="data">{key}</match>
      </input>
      <output type="gz.msgs.Twist" topic="/model/ev3/cmd_vel">
        {twist_body}
      </output>
    </plugin>"""


def gui_xml() -> str:
    return """
    <gui fullscreen="0">
      <plugin filename="MinimalScene" name="3D View">
        <gz-gui>
          <title>3D View</title>
          <property type="bool" key="showTitleBar">false</property>
          <property type="string" key="state">docked</property>
        </gz-gui>
        <engine>ogre2</engine>
        <scene>scene</scene>
        <ambient_light>0.45 0.45 0.48</ambient_light>
        <background_color>0.72 0.76 0.80</background_color>
        <camera_pose>-0.85 -0.95 0.70 0 0.55 0.85</camera_pose>
      </plugin>
      <plugin filename="EntityContextMenuPlugin" name="Entity context menu">
        <gz-gui>
          <property key="state" type="string">floating</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>
      <plugin filename="GzSceneManager" name="Scene Manager">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>
      <plugin filename="InteractiveViewControl" name="Interactive view control">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>
      <plugin filename="CameraTracking" name="Camera Tracking">
        <gz-gui>
          <property key="resizable" type="bool">false</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>
      <plugin filename="WorldControl" name="World control">
        <gz-gui>
          <title>World control</title>
          <property type="bool" key="showTitleBar">false</property>
          <property type="bool" key="resizable">false</property>
          <property type="double" key="height">72</property>
          <property type="double" key="width">200</property>
          <property type="double" key="z">1</property>
          <property type="string" key="state">floating</property>
          <anchors target="3D View">
            <line own="left" target="left"/>
            <line own="bottom" target="bottom"/>
          </anchors>
        </gz-gui>
        <play_pause>true</play_pause>
        <step>true</step>
        <start_paused>false</start_paused>
      </plugin>
      <plugin filename="WorldStats" name="World stats">
        <gz-gui>
          <title>World stats</title>
          <property type="bool" key="showTitleBar">false</property>
          <property type="bool" key="resizable">false</property>
          <property type="double" key="height">110</property>
          <property type="double" key="width">290</property>
          <property type="double" key="z">1</property>
          <property type="string" key="state">floating</property>
          <anchors target="3D View">
            <line own="right" target="right"/>
            <line own="bottom" target="bottom"/>
          </anchors>
        </gz-gui>
        <sim_time>true</sim_time>
        <real_time>true</real_time>
        <real_time_factor>true</real_time_factor>
        <iterations>true</iterations>
      </plugin>
      <plugin filename="KeyPublisher" name="Key publisher">
        <gz-gui>
          <anchors target="3D View">
            <line own="right" target="right"/>
            <line own="top" target="top"/>
          </anchors>
          <property key="resizable" type="bool">false</property>
          <property key="width" type="double">5</property>
          <property key="height" type="double">5</property>
          <property key="state" type="string">floating</property>
          <property key="showTitleBar" type="bool">false</property>
        </gz-gui>
      </plugin>
    </gui>"""


def world_sdf() -> str:
    keys = (
        triggered_publisher(KEY_W, "linear: {x: 0.10}")
        + triggered_publisher(KEY_S, "linear: {x: -0.10}")
        + triggered_publisher(KEY_A, "angular: {z: 0.80}")
        + triggered_publisher(KEY_D, "angular: {z: -0.80}")
        + triggered_publisher(KEY_X, "linear: {x: 0.0}, angular: {z: 0.0}")
    )
    return f"""<?xml version="1.0" ?>
<!-- Generated by ev3_gz_gazebo/scripts/generate_ev3_lab.py — do not edit by hand. -->
<sdf version="1.11">
  <world name="ev3_lab">
    <physics name="1ms" type="ignored">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>
    <plugin filename="gz-sim-physics-system" name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-scene-broadcaster-system" name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-user-commands-system" name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-contact-system" name="gz::sim::systems::Contact"/>
    <plugin filename="gz-sim-imu-system" name="gz::sim::systems::Imu"/>
    <plugin filename="gz-sim-sensors-system" name="gz::sim::systems::Sensors">
      <render_engine>ogre2</render_engine>
    </plugin>
{keys}
{gui_xml()}

    <scene>
      <ambient>0.45 0.45 0.48 1</ambient>
      <background>0.72 0.76 0.80 1</background>
      <grid>false</grid>
    </scene>

    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.85 0.85 0.82 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <model name="baseplate">
      <static>true</static>
      <pose>0 0 0 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>{PLATE_M:.3f} {PLATE_M:.3f}</size>
            </plane>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>{PLATE_M:.3f} {PLATE_M:.3f}</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.55 0.56 0.58 1</ambient>
            <diffuse>1 1 1 1</diffuse>
            <specular>0.08 0.08 0.08 1</specular>
            <pbr>
              <metal>
                <albedo_map>package://ev3_gz_gazebo/textures/baseplate.png</albedo_map>
              </metal>
            </pbr>
          </material>
        </visual>
      </link>
    </model>
{border_bricks()}
{obstacle_bricks()}

    <include>
      <pose>0 0 0.028 0 0 0</pose>
      <uri>package://ev3_gz_description/models/ev3</uri>
    </include>
  </world>
</sdf>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output directory (writes worlds/ev3_lab.sdf and textures/baseplate.png)",
    )
    args = parser.parse_args()
    out: Path = args.out
    worlds = out / "worlds"
    textures = out / "textures"
    worlds.mkdir(parents=True, exist_ok=True)
    textures.mkdir(parents=True, exist_ok=True)
    write_png_rgb(
        textures / "baseplate.png",
        PNG_SIZE,
        PNG_SIZE,
        render_baseplate(PNG_SIZE, PLATE_STUDS),
    )
    (worlds / "ev3_lab.sdf").write_text(world_sdf(), encoding="utf-8")
    print(f"wrote {worlds / 'ev3_lab.sdf'}")
    print(f"wrote {textures / 'baseplate.png'}")


if __name__ == "__main__":
    main()
