"""Übung 3 – Wiederholungen in Funktionen auslagern.

Der Code unten funktioniert, ist aber voller Copy-Paste.
Ausführen:  python 03_refactor.py
"""

# --- "Vorher": dreimal fast derselbe Block -----------------------------------
ip1 = "10.0.1.5"
if ip1.startswith("10.") or ip1.startswith("192.168.") or ip1.startswith("172.16."):
    print(f"{ip1} ist eine private Adresse")
else:
    print(f"{ip1} ist öffentlich")

ip2 = "8.8.8.8"
if ip2.startswith("10.") or ip2.startswith("192.168.") or ip2.startswith("172.16."):
    print(f"{ip2} ist eine private Adresse")
else:
    print(f"{ip2} ist öffentlich")

ip3 = "192.168.0.10"
if ip3.startswith("10.") or ip3.startswith("192.168.") or ip3.startswith("172.16."):
    print(f"{ip3} ist eine private Adresse")
else:
    print(f"{ip3} ist öffentlich")

# ----------------------------------------------------------------------------
# AUFGABE:
#   Schreibe EINE Funktion, die die Wiederholung beseitigt, z. B.:
#
#       def klassifiziere(ip: str) -> str:
#           ...
#
#   und rufe sie für ip1, ip2, ip3 auf. Faustregel: Wenn du Code kopierst und
#   nur einen Wert änderst -> das gehört in eine Funktion (ein Parameter).
#
# ★ PROFI-BONUS:
#   - Gib einen Docstring und einen sinnvollen Rückgabewert (bool oder str).
#   - Verarbeite eine ganze Liste von IPs in einer Schleife.
# ----------------------------------------------------------------------------
