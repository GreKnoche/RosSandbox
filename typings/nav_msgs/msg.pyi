from geometry_msgs.msg import Pose

class PoseWithCovariance:
    pose: Pose

class Odometry:
    """Schätzung, wo der Roboter ist. Topic ``/odom``.

    Position: ``msg.pose.pose.position.x`` / ``.y``.
    Orientierung: ``msg.pose.pose.orientation``.
    """

    pose: PoseWithCovariance
