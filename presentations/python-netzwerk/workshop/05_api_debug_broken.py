"""Übung 5b – DEBUGGING: In diesem Skript stecken DREI Fehler.

Aufgabe: Führe es aus, lies den Traceback (von UNTEN nach OBEN!) und behebe
die Fehler EINZELN. Das Ziel-Verhalten entspricht 05_api_debug.py.

Ausführen:  python 05_api_debug_broken.py
"""

import request

URL = "https://api.ipify.org"


def main():
    response = requests.get(URL, params={"format": "json"}, timeout=10)
    data = response.json

    print(f"Unsere IP: {data['address']}")


if __name__ == "__main__":
    main()
