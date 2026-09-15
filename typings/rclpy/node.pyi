from collections.abc import Callable
from typing import Any, TypeVar

from rclpy.parameter import Parameter
from rclpy.publisher import Publisher
from rclpy.subscription import Subscription
from rclpy.timer import Timer

MsgT = TypeVar('MsgT')

class Node:
    """Ein Knoten ist ein kleines ROS-Programm mit Timer, Publisher und Subscriber."""

    def __init__(self, node_name: str, **kwargs: Any) -> None:
        """Knoten erzeugen.

        :param node_name: Name in ROS, z. B. ``'uebung1'``.
        """
        ...

    def create_timer(
        self,
        timer_period_sec: float,
        callback: Callable[[], None],
        callback_group: Any = None,
        clock: Any = None,
        autostart: bool = True,
    ) -> Timer:
        """Timer: ruft ``callback`` regelmäßig auf.

        :param timer_period_sec: Periode in Sekunden. ``1.0`` = einmal pro Sekunde,
            ``0.1`` = 10 Hz.
        :param callback: Funktion ohne Argumente, z. B. ``self.on_timer``.
        """
        ...

    def create_publisher(
        self,
        msg_type: type[MsgT],
        topic: str,
        qos_profile: int | Any,
        **kwargs: Any,
    ) -> Publisher[MsgT]:
        """Publisher: schreibt Nachrichten auf ein Topic.

        :param msg_type: Nachrichtentyp, z. B. ``Bool`` oder ``Twist``.
        :param topic: Kanalname, z. B. ``'/led'`` oder ``'/cmd_vel'``.
        :param qos_profile: Warteschlangenlänge, in den Übungen ``10``.
        """
        ...

    def create_subscription(
        self,
        msg_type: type[MsgT],
        topic: str,
        callback: Callable[[MsgT], None],
        qos_profile: int | Any,
        **kwargs: Any,
    ) -> Subscription[MsgT]:
        """Subscriber: liest Nachrichten von einem Topic.

        :param msg_type: Nachrichtentyp, z. B. ``Odometry``.
        :param topic: Kanalname, z. B. ``'/odom'``.
        :param callback: Funktion mit der Nachricht als Argument, z. B. ``self.on_odom``.
        :param qos_profile: Warteschlangenlänge, in den Übungen ``10``.
        """
        ...

    def get_logger(self) -> Any:
        """Logger für Text in der Konsole. ``.info(...)``, ``.warn(...)``."""
        ...

    def set_parameters(self, parameter_list: list[Parameter]) -> list[Any]:
        """Parameter setzen. In den Übungen: ``use_sim_time = True``."""
        ...

    def destroy_node(self) -> None:
        """Knoten aufräumen. Am Ende von ``main()`` aufrufen."""
        ...
