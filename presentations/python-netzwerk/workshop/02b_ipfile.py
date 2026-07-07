"""Zusatzübung 2b – Eine Datei zeilenweise einlesen und auswerten.

Wir nutzen die echte Datei data/ips.txt (eine IP pro Zeile).
Läuft auf Linux, macOS UND Windows aus jedem Verzeichnis:
'pathlib' baut den Pfad plattformunabhängig relativ zu DIESER Datei.
Ausführen:  python 02b_ipfile.py
"""

from pathlib import Path

# Path(__file__).parent = der Ordner dieser Datei -> Pfad ist überall gültig,
# egal aus welchem Verzeichnis man das Skript startet (auch unter Windows).
ips_datei = Path(__file__).parent / "data" / "ips.txt"

with open(ips_datei, encoding="utf-8") as f:      # encoding fixiert = Windows-sicher
    zeilen = [z.strip() for z in f if z.strip()]

print(f"{len(zeilen)} Adressen eingelesen:")
for ip in zeilen:
    print(f"  {ip}")

# ----------------------------------------------------------------------------
# AUFGABE:
#   1) Gib nur die Adressen aus, die NICHT mit "10." beginnen.
#   2) Zähle, wie viele Adressen im privaten Bereich liegen
#      (10. / 192.168. / 172.16.) und wie viele öffentlich sind.
#      Gib beide Zahlen aus.
#
# ★ PROFI-BONUS:
#   Finde mit einer while-Schleife die ERSTE öffentliche Adresse und brich
#   dann mit 'break' ab. Gib aus, an welcher Position (Index) sie stand.
# ----------------------------------------------------------------------------
