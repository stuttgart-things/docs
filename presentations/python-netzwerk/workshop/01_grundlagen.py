"""Übung 1 – Variablen, Datentypen, Ausgabe.

Ziel: ein Gefühl für die Grundbausteine bekommen.
Ausführen:  python 01_grundlagen.py
"""

# --- Variablen verschiedener Typen ------------------------------------------
hostname = "router-stuttgart-01"     # str
port_count = 48                      # int
cpu_load = 0.41                      # float
is_online = True                     # bool

print("=== Geräte-Info ===")
print(f"Hostname : {hostname}")
print(f"Ports    : {port_count}")
print(f"CPU-Last : {cpu_load * 100:.0f} %")
print(f"Online   : {is_online}")

# --- Eine Liste von Hosts ---------------------------------------------------
hosts = ["sw-01", "sw-02", "fw-01", "rtr-01"]
print(f"\nWir verwalten {len(hosts)} Geräte:")
for host in hosts:
    print(f" - {host}")

# --- Ein Dictionary: Hostname -> IP -----------------------------------------
ip_of = {
    "sw-01": "10.0.1.11",
    "sw-02": "10.0.1.12",
    "fw-01": "10.0.0.1",
}
print(f"\nIP von sw-02: {ip_of['sw-02']}")

# ----------------------------------------------------------------------------
# AUFGABE:
#   1) Lege eine Variable 'standort' an und gib sie mit aus.
#   2) Füge dem Dictionary 'ip_of' einen Eintrag für "rtr-01" hinzu.
#
# ★ PROFI-BONUS:
#   Gib für JEDES Gerät aus der Liste 'hosts' die IP aus – und "unbekannt",
#   falls kein Eintrag im Dictionary existiert. (Tipp: ip_of.get(host, ...))
# ----------------------------------------------------------------------------
