"""Zusatzübung 4b – Ein zweites Modul, das netutils wiederverwendet.

'report.py' importiert aus 'netutils.py' und erzeugt eine Zusammenfassung.
Zeigt: ein Modul kann von mehreren Stellen genutzt werden.
Ausführen (im Ordner 04_module):  python report.py
"""

from netutils import is_private, subnet_prefix


def summary(ips: list) -> dict:
    """Zählt private vs. öffentliche Adressen."""
    ergebnis = {"privat": 0, "oeffentlich": 0}
    for ip in ips:
        if is_private(ip):
            ergebnis["privat"] += 1
        else:
            ergebnis["oeffentlich"] += 1
    return ergebnis


if __name__ == "__main__":
    ips = ["10.0.1.5", "8.8.8.8", "192.168.0.10", "1.1.1.1"]
    print(summary(ips))

# ----------------------------------------------------------------------------
# AUFGABE:
#   1) Ergänze eine Funktion, die pro Subnetz (subnet_prefix) zählt, wie viele
#      Adressen darunter fallen, und gib das Ergebnis aus.
#   2) Importiere und rufe summary() aus main.py heraus auf.
#
# ★ PROFI-BONUS:
#   Schreibe die Zusammenfassung zusätzlich in eine Datei report.txt
#   (open("report.txt", "w", encoding="utf-8")). Prüfe danach im Terminal:
#   'type report.txt' (Windows) bzw. 'cat report.txt' (Linux/macOS).
# ----------------------------------------------------------------------------
