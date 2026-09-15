# RosSandbox

ROS-2-Jazzy-Sandbox: EV3 in Gazebo Harmonic, Übungen zu `cmd_vel` und Odometrie.

Voraussetzung: Docker mit Compose, grafische Sitzung (X11).

## Container starten

Terminal 1 — Gazebo (bleibt laufen):

```bash
./start-simulation.sh
```

Das gibt X11 für Docker frei und startet den `gazebo`-Container (`docker/compose.yaml`). Der EV3 steht auf der **grünen** Startplatte (Blick +x). Gelbe Tore testen Geradeausfahrt, die 90°-Kurve das Drehen, die **rote** Platte ist das Ziel.

## Übungen starten

Terminal 2 — sobald die Sim läuft. Nummer anhängen; `2`, `-2` und `--2` sind gleich:

```bash
./excercise.sh 1
./excercise.sh 2
./excercise.sh -2
./excercise.sh --3
```

Ohne Argument listet das Skript die Übungen. Abbruch mit Strg+C; Gazebo weiterlaufen lassen und den Node einfach neu starten.

## Übungen

Schülerdateien mit `# LÜCKE N:` liegen unter `src/ev3_exercises/ev3_exercises/`. Lösungen nur zum Abgleich unter `src/ev3_exercises/ev3_exercises/solutions/`.

| Start | Datei | Inhalt |
| --- | --- | --- |
| `./excercise.sh 1` | `src/ev3_exercises/ev3_exercises/uebung1.py` | Hello-Node: Timer und Logger, ohne Gazebo |
| `./excercise.sh 2` | `src/ev3_exercises/ev3_exercises/uebung2.py` | Publisher auf `/cmd_vel`, vorwärts (`linear.x`) |
| `./excercise.sh 3` | `src/ev3_exercises/ev3_exercises/uebung3.py` | Auf der Stelle drehen (`angular.z`) |
| `./excercise.sh 4` | `src/ev3_exercises/ev3_exercises/uebung4.py` | Ein paar Sekunden fahren, dann Stopp `(0, 0)` |
| `./excercise.sh 5` | `src/ev3_exercises/ev3_exercises/uebung5.py` | Strecke: vor durch die Tore, 90° links, vor auf Rot, stop |
| `./excercise.sh 6` | `src/ev3_exercises/ev3_exercises/uebung6.py` | Subscriber auf `/odom`, Pose loggen |

Richtwerte für den EV3: etwa **0.15 m/s** und **0.6 rad/s**. Positives `angular.z` dreht nach links.
