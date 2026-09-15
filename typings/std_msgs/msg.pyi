class Bool:
    """Einfache Ja/Nein-Nachricht. Topic ``/led``: ``True`` = Lampe an."""

    data: bool

class ColorRGBA:
    """Farbe mit Rot, Grün, Blau, Alpha (0.0–1.0)."""

    r: float
    g: float
    b: float
    a: float
