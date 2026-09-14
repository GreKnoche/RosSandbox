# RosSandbox

ROS-2-Jazzy-Sandbox: EV3 als SDF in Gazebo Harmonic, `cmd_vel` und Odometrie als Basics.

## Voraussetzungen

- ROS 2 Jazzy
- Gazebo Harmonic (`sudo apt install ros-jazzy-ros-gz`)
- `colcon`, Python 3

## Bauen

```bash
cd RosSandbox
colcon build --symlink-install
source install/setup.bash
```

## Simulation

```bash
ros2 launch ev3_sdf sim.launch.py
```

Der EV3 steht auf der **grünen** Startplatte (Blick +x). Gelbe Tore testen Geradeausfahrt, die 90°-Kurve das Drehen, die **rote** Platte ist das Ziel.

Topics:

| Topic | Typ | Richtung |
| --- | --- | --- |
| `/cmd_vel` | `geometry_msgs/Twist` | fahren |
| `/odom` | `nav_msgs/Odometry` | Pose |
| `/clock` | `rosgraph_msgs/Clock` | Sim-Zeit |

Twist: `linear.x` vorwärts (m/s), `angular.z` drehen (rad/s). Für den EV3 langsam bleiben, ca. **0.15 m/s** und **0.6 rad/s**. Positives `angular.z` = links.

Kurztest ohne eigenen Node:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.15}}"
```

## Übungen

Die Nodes in `src/ev3_exercises` haben markierte `# LÜCKE N:`-Stellen. Reihenfolge:

1. `ros2 run ev3_exercises ex01_hello` — Node, Timer, Logger
2. `ros2 run ev3_exercises ex02_drive_forward` — Publisher + `linear.x`
3. `ros2 run ev3_exercises ex03_turn` — `angular.z`
4. `ros2 run ev3_exercises ex04_timed_move` — fahren, dann Stopp `(0, 0)`
5. `ros2 run ev3_exercises ex05_track` — Strecke: vor, 90° links, vor, stop
6. `ros2 run ev3_exercises ex06_odom` — Subscriber `/odom`

Lösungen (nur zum Abgleich): `ros2 run ev3_exercises ex05_track_solution` usw.
