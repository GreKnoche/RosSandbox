from typing import Any

class Parameter:
    """Knoten-Parameter, z. B. ob die Simulationsuhr genutzt wird."""

    class Type:
        BOOL: Any
        INTEGER: Any
        DOUBLE: Any
        STRING: Any

    def __init__(self, name: str, type_: Any = None, value: Any = None) -> None:
        """Parameter anlegen.

        In den Übungen immer::

            Parameter('use_sim_time', Parameter.Type.BOOL, True)
        """
        ...
