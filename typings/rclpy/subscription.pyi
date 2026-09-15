from typing import Generic, TypeVar

MsgT = TypeVar('MsgT')

class Subscription(Generic[MsgT]):
    """Liest Nachrichten von einem Topic. Kommt von ``create_subscription``.

    Die Callback-Funktion wird aufgerufen, sobald eine Nachricht da ist.
    """
    ...
