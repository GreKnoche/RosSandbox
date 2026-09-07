# Gazebo overlay

ROS 2 Jazzy + Gazebo Harmonic workspace shaped like [`ros_gz_project_template`](https://gazebosim.org/docs/harmonic/ros_gz_project_template_guide/). The robot is the LEGO Education **Robot Educator driving base** with both official sensor attachments fitted at once. The world is a Python-generated LEGO tabletop (grey studded baseplate, 8 mm bricks).

- 56 mm motorcycle tires, 118 mm axle track (LEGO Education DriveBase figures)
- White Education EV3 brick on two Large Motors
- Rear steel-ball caster
- Gyro on the rear L-beam tower (`gyro_link`, yaw about +Z)
- Ultrasonic on the front 7-hole beam (`ultrasonic_link`, eyes just below axle height)

That matches the Gyro Sensor Driving Base and Ultrasonic Sensor Driving Base instruction PDFs. `/ultrasonic` is `sensor_msgs/Range` (a narrow gpu_lidar cone is converted by `scan_to_range.py`). Hardware uses the same type.

Gazebo kinematics use 0.028 m / 0.118 m. `shared/chassis.yaml` stays the BrickPi3 measurement (0.0277 / 0.1103) until you re-measure that build.

## Drive it

The physics plugin already listens on `/model/ev3/cmd_vel`. `ros_gz_bridge` maps ROS `/cmd_vel` there. Nothing in Docker compose publishes a twist by itself — pick one:

**WASD in the Gazebo window** (click the 3D view first): `W`/`S` forward/back, `A`/`D` turn, `X` stop.

**ROS teleop** in a second terminal, after the sim is up. Publish ROS `/cmd_vel`, not the Gazebo name `/model/ev3/cmd_vel`. Source `localhost.env` so FastDDS and `gz topic` use the same loopback transport as Docker:

```bash
source /opt/ros/jazzy/setup.bash
set -a && source localhost.env && set +a
ros2 daemon stop
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=false
# or
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.08}}" -r 10
```

Native launch with the keyboard node in the same process (needs a TTY; leave it off under `docker compose`):

```bash
ros2 launch ev3_gz_bringup sim.launch.py teleop:=true
```

Gyro and wheel-odom drift are off by default. `sensor_drift` still republishes `/odom`, `/imu`, and TF `odom → base_link` so the Nav2 contract stays intact; Gazebo ground truth remains on `/odom/perfect` and `/imu/perfect`. Turn a source on at launch or later:

```bash
ros2 launch ev3_gz_bringup sim.launch.py odom_drift:=true gyro_drift:=true
ros2 param set /sensor_drift gyro_drift true
ros2 param set /sensor_drift odom_drift true
```

## Docker (recommended)

On the companion PC, with X11:

```bash
xhost +local:docker
cd gazebo
docker compose up --build
```

Then WASD in the sim window, or ROS teleop from another host terminal after sourcing `localhost.env` as above (`network_mode: host`).

## Native

```bash
source /opt/ros/jazzy/setup.bash
cd gazebo
colcon build --symlink-install
source install/setup.bash
ros2 launch ev3_gz_bringup sim.launch.py
```

The lab SDF and `textures/baseplate.png` are generated at build by `scripts/generate_ev3_lab.py`.

## Packages

| Package | Role |
| --- | --- |
| `ev3_gz_description` | Educator SDF + URDF, `GZ_SIM_RESOURCE_PATH` hook |
| `ev3_gz_gazebo` | Generated `worlds/ev3_lab.sdf` + baseplate texture |
| `ev3_gz_bringup` | `sim.launch.py` + `ros_gz_bridge` + Range converter + sensor drift + optional teleop |

The kinematic twin (`backend:=sim` in the laptop overlay) is separate. Use it for lessons 00–01 without Gazebo.
