"""Übung 5 – Bibliothek nutzen & eine REST-API abfragen.

Wir fragen ab, mit welcher öffentlichen IP wir nach außen gehen – eine
klassische Netzwerk-Frage, und die API ist ohne Login nutzbar.
Ausführen:  python 05_api_debug.py
"""

import requests

URL = "https://api.ipify.org"
HEADERS = {"User-Agent": "netzwerk-workshop/1.0"}   # gute API-Etikette


def main() -> None:
    response = requests.get(URL, params={"format": "json"},
                            headers=HEADERS, timeout=10)
    response.raise_for_status()      # wirft Fehler bei HTTP 4xx/5xx
    data = response.json()           # JSON -> dict (Python-Wörterbuch)

    print(f"Unsere öffentliche IP ist: {data['ip']}")

    # AUFGABE:
    #   1) Gib zusätzlich den HTTP-Statuscode aus (response.status_code).
    #   2) Prüfe mit einer Bedingung, ob die IP mit "10." beginnt, und gib
    #      "privat" bzw. "öffentlich" aus.
    #
    # ★ PROFI-BONUS:
    #   Frage https://api.github.com/meta ab (der Header User-Agent ist dort
    #   PFLICHT!) und gib aus, wie viele CIDR-Bereiche unter "hooks" stehen.
    #   Hinweis: ohne Login limitiert GitHub die Abfragen pro Stunde.


if __name__ == "__main__":
    main()
