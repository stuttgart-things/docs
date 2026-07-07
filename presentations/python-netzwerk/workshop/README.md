# Python-Schulung Netzwerkteam

Willkommen! Diese Umgebung ist VS Code im Browser mit fertig installiertem Python.

## Wie arbeite ich hier?

- Links im **Explorer** siehst du die Übungsordner `01_…` bis `05_…`.
- Ein Skript ausführen: Datei öffnen → Rechtsklick → **Run Python File in Terminal**
  (oder im Terminal `python 01_grundlagen.py`).
- Terminal öffnen: Menü **Terminal → New Terminal** (oder `Strg + ö` / `Ctrl + ~`).

## Die Übungen

| Datei | Thema |
|-------|-------|
| `01_grundlagen.py`   | Variablen, Datentypen, Ausgabe |
| `01b_strings.py`     | *Zusatz:* Strings zerlegen & formatieren |
| `02_filter.py`       | Schleifen & Bedingungen (IPs filtern) |
| `02b_ipfile.py`      | *Zusatz:* Datei `data/ips.txt` einlesen & auswerten |
| `03_refactor.py`     | Wiederholungen in Funktionen auslagern |
| `03b_netzmaske.py`   | *Zusatz:* mehr Funktionen (Netzmaske ⇄ CIDR, Defaults) |
| `04_module/`         | Code auf mehrere Dateien aufteilen + `venv` |
| `04_module/report.py`| *Zusatz:* zweites Modul, das `netutils` mitbenutzt |
| `05_api_debug.py`    | Bibliothek nutzen, REST-API abfragen |
| `05_api_debug_broken.py` | **Debugging:** drei Fehler finden |
| `05c_api_robust.py`  | *Zusatz:* zweite API + `try/except`-Fehlerbehandlung |

Jede Übung hat eine **Basis-Aufgabe** (für alle) und einen **★ Profi-Bonus**;
zu jedem Thema gibt es zusätzlich eine **Zusatzübung** (`…b` / `…c`) als Zeitpuffer.

> **Windows:** Alle Skripte laufen unverändert unter Windows. Pfade sind
> plattformunabhängig (`pathlib`), Dateien werden mit `encoding="utf-8"`
> geöffnet. venv aktivieren: `.venv\Scripts\Activate.ps1` (statt `source …`).

Spickzettel: `SPICKZETTEL.md`

## Lieber lokal arbeiten?

Dieser Ordner läuft genauso auf deinem eigenen Rechner. Zwei Wege:

**A) Einfach: Python + dein Editor** (kein Docker nötig)
```bash
# Python 3.12 installiert? -> diesen Ordner öffnen, dann:
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python 01_grundlagen.py
```

**B) Komfortabel: Dev Container** (Docker + VS Code mit „Dev Containers")
Ordner in VS Code öffnen → unten rechts **„Reopen in Container"**. Du bekommst
exakt dieselbe Umgebung wie im Browser-code-server – **plus** die volle
MS-Python-Extension, Pylance und den grafischen Debugger (die gibt's lokal,
im Browser nicht). Derselbe `.devcontainer` funktioniert auch in GitHub Codespaces.
