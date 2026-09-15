# RosSandbox

ROS-2-Jazzy-Sandbox: EV3 als SDF in Gazebo Harmonic, `cmd_vel` und Odometrie als Basics.

## Voraussetzungen

- Docker und Docker Compose (empfohlen)
- oder nativ: ROS 2 Jazzy, Gazebo Harmonic (`sudo apt install ros-jazzy-ros-gz`), `colcon`, Python 3

## Docker (empfohlen)

Auf dem Rechner mit X11:

```bash
xhost +local:docker
cd RosSandbox
docker compose up --build
```

`src/` ist ins Image gemountet; Übungsdateien ändern, Container neu starten reicht meist. Übungen ohne ROS auf dem Host:

```bash
./excercise.sh 1
./excercise.sh -2
./excercise.sh --3
```

Teleop vom Host (wenn Jazzy dort installiert ist). Die Loopback-Variablen für FastDDS/Gazebo sind im Docker-Setup bereits gesetzt; für den Host kannst du sie auch lokal exportieren:

```bash
source /opt/ros/jazzy/setup.bash
export GZ_IP=127.0.0.1
export GZ_PARTITION=ev3
export FASTDDS_BUILTIN_TRANSPORTS=UDPv4
ros2 daemon stop
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.15}}"
```

## Bauen (nativ)

```bash
cd RosSandbox
colcon build --symlink-install
source install/setup.bash
```

## Simulation (nativ)

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

Die Nodes in `src/ev3_exercises` haben markierte `# LÜCKE N:`-Stellen. Sim starten, danach die Nummer anhängen (`2`, `-2` oder `--2` sind gleich):

```bash
./start-simulation.sh
./excercise.sh 1
```

1. `./excercise.sh 1` — Node, Timer, Logger
2. `./excercise.sh 2` — Publisher + `linear.x`
3. `./excercise.sh 3` — `angular.z`
4. `./excercise.sh 4` — fahren, dann Stopp `(0, 0)`
5. `./excercise.sh 5` — Strecke: vor, 90° links, vor, stop
6. `./excercise.sh 6` — Subscriber `/odom`

Lösungen (nur zum Abgleich): `ros2 run ev3_exercises uebung5_solution` usw.
