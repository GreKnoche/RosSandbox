class Vector3:
    """Drei Zahlen. Bei Twist: Meter bzw. Radiant pro Sekunde."""

    x: float
    y: float
    z: float

class Point:
    """Position in Metern."""

    x: float
    y: float
    z: float

class Quaternion:
    """Orientierung. Zum Gieren reicht oft ``z`` und ``w``."""

    x: float
    y: float
    z: float
    w: float

class Pose:
    """Lage: Position plus Orientierung."""

    position: Point
    orientation: Quaternion

class Twist:
    """Fahrbefehl für ``/cmd_vel``.

    ``linear.x``: vorwärts (m/s), beim EV3 ca. 0.15.
    ``angular.z``: drehen (rad/s), positiv = links, ca. 0.6.
    """

    linear: Vector3
    angular: Vector3
