"""Zusatzübung 5c – Robuste API-Abfrage mit Fehlerbehandlung.

Wir fragen eine zweite offene API ab und fangen Fehler sauber mit try/except.
Ausführen:  python 05c_api_robust.py
"""

import requests

URL = "https://httpbin.org/get"
HEADERS = {"User-Agent": "netzwerk-workshop/1.0"}


def main() -> None:
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as fehler:
        print(f"Abfrage fehlgeschlagen: {fehler}")
        return

    data = response.json()
    print(f"Server sah unsere Anfrage von: {data['origin']}")
    print(f"Gesendeter User-Agent       : {data['headers']['User-Agent']}")


if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------------
# AUFGABE:
#   1) Gib zusätzlich die Ziel-URL aus (data["url"]).
#   2) Ändere URL auf https://httpbin.org/status/404 und beobachte, wie
#      raise_for_status() den Fehler sauber in den except-Zweig schickt.
#
# ★ PROFI-BONUS:
#   Baue in eine KOPIE dieses Skripts selbst zwei Fehler ein (z. B. Tippfehler
#   im Key, fehlende Klammern) und lass den Sitznachbarn sie per Traceback
#   finden – danach Rollen tauschen.
# ----------------------------------------------------------------------------
