---
layout: default
num: '15a · Funktion auslagern'
meta: 'Block 4 · 04_module/ · from netutils import …'
---

<div class="page-label">Block 4 · Funktion auslagern</div>

# Eine Funktion in ihre <span class="accent">eigene Datei</span><span class="dot">.</span>

<div class="vn">

  <div class="vn-col">
    <div class="vn-tag vorher">Vorher · alles in main.py</div>

```python
# main.py — Funktion UND Ablauf in einer Datei
def is_private(ip: str) -> bool:
    return ip.startswith(("10.", "192.168.", "172.16."))

for ip in ["10.0.1.5", "8.8.8.8"]:
    print(ip, "privat" if is_private(ip) else "öffentlich")
```

  </div>

  <div class="vn-col" v-click>
    <div class="vn-tag nachher">Nachher · Werkzeug im Modul, Ablauf in main</div>

```python
# netutils.py — der Werkzeugkasten
def is_private(ip: str) -> bool:
    return ip.startswith(("10.", "192.168.", "172.16."))
```

```python
# main.py — holt das Werkzeug herein
from netutils import is_private

for ip in ["10.0.1.5", "8.8.8.8"]:
    print(ip, "privat" if is_private(ip) else "öffentlich")
```

  </div>

</div>

<div class="mantra" style="margin-top: 22px;">
  <div class="label">import-Regel</div>
  <div class="text"><span class="mono">from netutils import is_private</span> — Dateiname <strong>ohne</strong> <span class="mono">.py</span>, Funktionsname genau wie definiert. Beide Dateien im selben Ordner.</div>
</div>

<style scoped>
.vn { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 24px; align-items: start; }
.vn-tag { font-family: var(--font-mono); font-size: 15px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 12px; }
.vn-tag.vorher { color: #C0392B; }
.vn-tag.nachher { color: var(--accent); }
.vn .slidev-code { font-size: 17px !important; padding: 20px !important; }
.vn-col > .slidev-code + .slidev-code { margin-top: 14px; }
</style>

<!--
Das ist die direkte Antwort auf die Frage „wie teile ich Funktionen auf mehrere Dateien auf?".
Links: alles steckt in main.py — funktioniert, wird aber schnell unübersichtlich und die Funktion
lässt sich in keinem anderen Skript nutzen. Per Klick die rechte Seite aufdecken: die Funktion
wandert unverändert nach netutils.py (das Modul aus der vorigen Slide). main.py holt sie mit
'from netutils import is_private' herein und bleibt schlank — nur noch der Ablauf. Wichtig für
Einsteiger und der häufigste Stolperstein: beim import den DATEINAMEN ohne .py schreiben
(netutils, nicht netutils.py), der Funktionsname muss exakt passen (Groß/Klein), und beide
Dateien müssen im selben Ordner liegen, sonst gibt es ModuleNotFoundError. Faustregel wie bei
Funktionen, nur eine Ebene höher: was woanders wiederverwendbar ist, kommt in ein eigenes Modul.
-->
