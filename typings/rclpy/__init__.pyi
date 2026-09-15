from rclpy.node import Node

def init(args: list[str] | None = None) -> None:
    """ROS starten. Einmal am Anfang von ``main()`` aufrufen."""
    ...

def spin(node: Node) -> None:
    """Knoten laufen lassen, bis Strg+C.

    Hier werden Timer- und Topic-Callbacks wirklich ausgeführt.
    """
    ...

def shutdown() -> None:
    """ROS beenden. Am Ende von ``main()`` aufrufen."""
    ...
