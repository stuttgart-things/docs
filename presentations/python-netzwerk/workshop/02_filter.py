"""Übung 2 – Schleifen & Bedingungen: IP-Adressen filtern.

Ausführen:  python 02_filter.py
"""

ip_addresses = [
    "10.0.1.11", "10.0.1.12", "192.168.5.4", "10.0.2.7",
    "172.16.0.9", "192.168.5.99", "10.0.1.250", "8.8.8.8",
]

# --- Basis: alle Adressen aus dem 10.0.1.x-Netz ausgeben --------------------
print("Adressen im Netz 10.0.1.x:")
for ip in ip_addresses:
    if ip.startswith("10.0.1."):
        print(f"  {ip}")

# ----------------------------------------------------------------------------
# AUFGABE:
#   1) Gib stattdessen alle Adressen aus, die mit "192.168." beginnen.
#   2) Zähle mit, WIE VIELE das sind, und gib die Zahl am Ende aus.
#
# ★ PROFI-BONUS:
#   Erzeuge ein Dictionary, das pro Präfix (z. B. "10.", "172.", "192.168.",
#   "8.")  zählt, wie viele Adressen darunter fallen. Ausgabe z. B.:
#       10.       -> 4
#       192.168.  -> 2
#   (Tipp: zaehler = {}, dann zaehler[prefix] = zaehler.get(prefix, 0) + 1)
# ----------------------------------------------------------------------------
