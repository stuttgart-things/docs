"""Zusatzübung 3b – Weitere Funktionen: Parameter, Rückgaben, Defaults.

Ausführen:  python 03b_netzmaske.py
"""


def maske_to_cidr(maske: str) -> int:
    """'255.255.255.0' -> 24. Zählt die 1-Bits der Netzmaske."""
    bits = 0
    for oktett in maske.split("."):
        bits += bin(int(oktett)).count("1")
    return bits


print("255.255.255.0 ->", maske_to_cidr("255.255.255.0"))
print("255.255.0.0   ->", maske_to_cidr("255.255.0.0"))

# ----------------------------------------------------------------------------
# AUFGABE:
#   1) Schreibe die Umkehrung cidr_to_maske(cidr: int) -> str,
#      z. B. 24 -> "255.255.255.0".
#   2) Rufe beide Funktionen mit ein paar Werten auf und vergleiche.
#
# ★ PROFI-BONUS:
#   Schreibe host_erreichbar(host: str, versuche: int = 3) -> bool mit einem
#   DEFAULT-Parameter (kein echter Ping nötig – simuliere z. B. "Host endet
#   auf gerade Ziffer" == erreichbar). Rufe sie einmal mit und einmal ohne
#   'versuche' auf und wende sie in einer Schleife auf mehrere Hosts an.
# ----------------------------------------------------------------------------
