#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT/docker"

usage() {
  cat <<'EOF'
Aufruf: ./excercise.sh <n>

  ./excercise.sh 2
  ./excercise.sh -2
  ./excercise.sh --2

Die Simulation muss laufen (./start-simulation.sh).

Übungen:
  1  Hello-Node (Timer, rote LED)
  2  Vorwärtsfahren (/cmd_vel, linear.x)
  3  Drehen (angular.z)
  4  Zeitgesteuert fahren und stoppen
  5  Basics-Strecke
  6  Odometrie lesen
EOF
}

if [[ $# -lt 1 || "${1}" == "-h" || "${1}" == "--help" ]]; then
  usage
  exit 0
fi

raw="${1}"
num="${raw#--}"
num="${num#-}"

if [[ ! "${num}" =~ ^[0-9]+$ ]]; then
  echo "Unbekannte Übung: ${raw}" >&2
  usage
  exit 1
fi

num=$((10#${num}))

if [[ "${num}" -lt 1 || "${num}" -gt 6 ]]; then
  echo "Übung ${num} gibt es nicht (1–6)." >&2
  usage
  exit 1
fi

exe="uebung${num}"

if [[ -z "$(docker compose ps -q gazebo 2>/dev/null)" ]]; then
  echo "Simulation läuft nicht. Zuerst ./start-simulation.sh" >&2
  exit 1
fi

exec docker compose exec -it gazebo bash -lc \
  "source /opt/ros/jazzy/setup.bash && source /tmp/install/setup.bash && ros2 run ev3_exercises ${exe}"
