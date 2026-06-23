"""Hilfsfunktionen rund um IP-Adressen – wiederverwendbar als eigenes Modul.

Alles, was thematisch zusammengehört und woanders gebraucht wird, kommt in
ein eigenes Modul (eigene Datei). 'main.py' importiert daraus.
"""

PRIVATE_PREFIXES = ("10.", "192.168.", "172.16.")


def is_private(ip: str) -> bool:
    """True, wenn die Adresse in einem privaten Bereich liegt."""
    return ip.startswith(PRIVATE_PREFIXES)


def subnet_prefix(ip: str) -> str:
    """Liefert die ersten drei Oktette, z. B. '10.0.1.5' -> '10.0.1'."""
    return ".".join(ip.split(".")[:3])
