"""Übung 4 – Code auf mehrere Dateien aufteilen.

Diese Datei importiert aus dem Nachbarmodul 'netutils.py'.
Ausführen (im Ordner 04_module):  python main.py
"""

from netutils import is_private, subnet_prefix

ips = ["10.0.1.5", "8.8.8.8", "192.168.0.10", "10.0.1.250"]

for ip in ips:
    art = "privat" if is_private(ip) else "öffentlich"
    print(f"{ip:<15} {art:<12} Subnetz={subnet_prefix(ip)}")

# ----------------------------------------------------------------------------
# AUFGABE:
#   1) Ergänze in netutils.py eine Funktion is_in_subnet(ip, prefix) und nutze
#      sie hier (importieren nicht vergessen!).
#   2) Lege eine venv an und installiere daraus 'rich':
#        python -m venv .venv
#        source .venv/bin/activate
#        pip install -r requirements.txt
#
# ★ PROFI-BONUS:
#   Nutze 'rich' (siehe requirements.txt), um die Ausgabe als hübsche Tabelle
#   darzustellen:  from rich.table import Table
# ----------------------------------------------------------------------------
