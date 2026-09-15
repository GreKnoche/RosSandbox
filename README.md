# RosSandbox
Voraussetzung Docker; für Type-Annotations und Funktionsbeschreibungen in der IDE VS Code nutzen oder sudo apt install ros-jazzy-desktop lokal installieren.

Anpassungen von Übungsdateien die Ros-Nodes erzeugen unter `src/ev3_excercises/ev3_excercises`
Lösungen in `src/ev3_excercises/ev3_excercises/solutions`

## ROS kurz

Ein **Knoten** ist ein kleines Programm. Knoten reden nicht direkt, sondern über **Topics** (Kanäle), z. B. `/cmd_vel` (fahren), `/led` (Lampe) und `/odom` (Position).

Ein **Publisher** schreibt auf ein Topic, ein **Subscriber** liest davon. Gleicher Name, gleicher Nachrichtentyp.

Ein **Timer** ruft regelmäßig eine Funktion auf, z. B. alle 1 s für die LED oder alle 0,1 s zum Fahren. `/cmd_vel` gilt nur kurz, ohne neue Nachricht bleibt der Roboter stehen. Die rote Lampe auf dem EV3 hört auf `/led` (`True` = an, `False` = aus).

## Container starten

Terminal 1 — Gazebo (bleibt laufen):

```bash
./start-simulation.sh
```

## Übungen starten

Terminal 2 — sobald die Sim läuft. Nummer anhängen; `2`, `-2` und `--2` sind gleich. Mit `-s` wird die Lösung gestartet:

```bash
./excercise.sh 1
./excercise.sh 2
./excercise.sh -2
./excercise.sh --3
./excercise.sh -1 -s
```

Ohne Argument listet das Skript die Übungen. Abbruch mit Strg+C; Gazebo weiterlaufen lassen und den Node einfach neu starten.

## Übungen

Übungsdateien mit `# LÜCKE N:` liegen unter `src/ev3_exercises/ev3_exercises/`. Lösungen nur zum Abgleich unter `src/ev3_exercises/ev3_exercises/solutions/`.

| Start | Datei | Inhalt |
| --- | --- | --- |
| `./excercise.sh 1` | `src/ev3_exercises/ev3_exercises/uebung1.py` | Timer: rote LED auf dem EV3 blinken (`/led`) |
| `./excercise.sh 2` | `src/ev3_exercises/ev3_exercises/uebung2.py` | Publisher auf `/cmd_vel`, vorwärts (`linear.x`) |
| `./excercise.sh 3` | `src/ev3_exercises/ev3_exercises/uebung3.py` | Auf der Stelle drehen (`angular.z`) |
| `./excercise.sh 4` | `src/ev3_exercises/ev3_exercises/uebung4.py` | Ein paar Sekunden fahren, dann Stopp `(0, 0)` |
| `./excercise.sh 5` | `src/ev3_exercises/ev3_exercises/uebung5.py` | Strecke: vor durch die Tore, 90° links, vor auf Rot, stop |
| `./excercise.sh 6` | `src/ev3_exercises/ev3_exercises/uebung6.py` | Subscriber auf `/odom`, Pose loggen |

Richtwerte für den EV3: etwa **0.15 m/s** und **0.6 rad/s**. Positives `angular.z` dreht nach links.
