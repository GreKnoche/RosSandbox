from typing import Generic, TypeVar

MsgT = TypeVar('MsgT')

class Publisher(Generic[MsgT]):
    """Schreibt Nachrichten auf ein Topic. Kommt von ``create_publisher``."""

    def publish(self, msg: MsgT) -> None:
        """Eine Nachricht senden.

        :param msg: Instanz vom Typ des Publishers, z. B. ``Twist()`` oder ``Bool()``.
        """
        ...
