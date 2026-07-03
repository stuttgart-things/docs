---
layout: default
num: '15b · Anatomie eines Skripts'
meta: 'Block 4 · Aufbau · if __name__ == "__main__"'
---

<div class="page-label">Block 4 · Anatomie eines Skripts</div>

# Jedes Skript hat die <span class="accent">gleiche Ordnung</span><span class="dot">.</span>

<div style="display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 40px; margin-top: 24px; align-items: start;">

<div>

```python {1-2|4-5|7-10|12-13|all}
# 1 · Imports — was das Skript braucht
from netutils import is_private

# 2 · Konstanten — feste Werte, GROSS geschrieben
HOSTS = ["10.0.1.5", "8.8.8.8"]

# 3 · Funktionen — die Bausteine (Prozeduren)
def main() -> None:
    for ip in HOSTS:
        print(ip, "privat" if is_private(ip) else "öffentlich")

# 4 · Startpunkt — nur bei direktem Ausführen
if __name__ == "__main__":
    main()
```

</div>

<div>
<ul style="margin: 0; padding: 0; list-style: none; display: grid; gap: 16px; font-size: 21px; line-height: 1.4;">
  <li><span class="accent" style="font-weight: 600;">1 Imports</span> immer oben — man sieht sofort die Abhängigkeiten.</li>
  <li><span class="accent" style="font-weight: 600;">2 Konstanten</span> darunter, <span class="mono">GROSS</span> geschrieben.</li>
  <li><span class="accent" style="font-weight: 600;">3 Funktionen</span> definieren, was passiert — noch nichts läuft.</li>
  <li><span class="accent" style="font-weight: 600;">4 Der Guard</span> startet <span class="mono">main()</span> nur beim direkten Aufruf.</li>
</ul>

<div class="mantra" style="margin-top: 24px;">
  <div class="label"><span class="mono">if __name__ == "__main__":</span></div>
  <div class="text"><span class="mono">python main.py</span> → läuft. <span class="mono">from main import …</span> → läuft <strong>nicht</strong> automatisch mit.</div>
</div>
</div>

</div>

<!--
Diese Slide beantwortet „Aufbau / Struktur eines Programms". Kernbotschaft: fast jedes gute
Python-Skript hat dieselben vier Abschnitte in dieser Reihenfolge — Imports, Konstanten,
Funktionen, Startpunkt. Geh die Highlights durch. Wichtig zu betonen: Funktionen zu DEFINIEREN
führt noch nichts aus; erst der Aufruf am Ende startet das Programm. Der Clou ist der Guard
if __name__ == "__main__". Erkläre ihn an der vorigen Slide: netutils.py wollen wir importieren,
ohne dass sein Code losläuft. Python setzt die Variable __name__ auf "__main__", WENN die Datei
direkt gestartet wird (python main.py) — und auf den Modulnamen, wenn sie importiert wird. So
kann dieselbe Datei sowohl als Programm laufen als auch als Werkzeugkasten importiert werden,
ohne Nebenwirkungen. Das ist DER Standard-Rahmen; ab jetzt bauen wir jedes Skript so.
-->
