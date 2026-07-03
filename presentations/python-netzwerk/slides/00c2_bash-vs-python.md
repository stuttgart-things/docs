---
layout: default
num: 'Bash vs. Python'
meta: 'Dieselbe Aufgabe · zwei Sprachen · wann was'
---

<div class="page-label">Bash vs. Python</div>

# Wann <span class="accent">Bash</span> aufhört, Spaß zu machen<span class="dot">.</span>

<p class="lede" style="margin-top: 10px; max-width: 88ch;">
Aufgabe: Aus der JSON-Antwort einer Geräte-API alle Geräte mit <strong>CPU-Last über 80 %</strong>
herausfiltern — und sauber abbrechen, wenn die API einen Fehler liefert.
</p>

<div class="vn">

  <div class="vn-col">
    <div class="vn-tag bash">Bash · schnell am Limit</div>

```bash
resp=$(curl -s http://api/devices)

# JSON von Hand? Nur mit jq erträglich —
# Zahlenvergleich, verschachtelte Felder:
echo "$resp" | jq -r '.devices[]
  | select(.cpu > 0.8) | .name'

# kein Fehler-Handling (HTTP 500?),
# schwer erweiterbar, nicht auf Windows
```

  </div>

  <div class="vn-col" v-click>
    <div class="vn-tag python">Python · wächst mit</div>

```python
import requests

resp = requests.get("http://api/devices", timeout=10)
resp.raise_for_status()        # scheitert sauber bei HTTP-Fehler

for dev in resp.json()["devices"]:
    if dev["cpu"] > 0.8:       # echter Zahlenvergleich
        print(dev["name"])
# lesbar · typsicher · testbar · überall lauffähig
```

  </div>

</div>

<div class="mantra" style="margin-top: 22px;">
  <div class="label">Faustregel</div>
  <div class="text">Für Einzeiler ist Bash unschlagbar. Sobald <strong>Logik, Zahlen, JSON oder Fehlerbehandlung</strong> dazukommen, ist Python die klarere Wahl.</div>
</div>

<style scoped>
.vn { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 22px; align-items: start; }
.vn-tag { font-family: var(--font-mono); font-size: 15px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 12px; }
.vn-tag.bash   { color: #C0392B; }
.vn-tag.python { color: var(--accent); }
.vn .slidev-code { font-size: 18px !important; padding: 22px !important; }
</style>

<!--
Diese Slide macht die abstrakte Aussage der Vergleichs-Folie („mächtiger als ein Shell-Skript")
konkret — und zwar an einer Aufgabe aus dem echten Netzwerk-Alltag, die genau zu Block 5 passt
(REST-API + JSON). WICHTIG: kein Bash-Bashing. Betone, dass Bash für Einzeiler und das Verketten
von Befehlen unschlagbar ist. Links zeigen wir die faire, realistische Bash-Lösung MIT jq — und
trotzdem sieht man die Schwächen: JSON und Zahlenvergleiche sind fummelig, es gibt kein sauberes
Fehler-Handling (was, wenn die API HTTP 500 liefert oder leer antwortet?), und sobald die Logik
wächst (zwei Bedingungen, Daten zusammenführen, sortieren) explodiert die Lesbarkeit. Rechts per
Klick die Python-Variante aufdecken: requests holt die Daten, raise_for_status bricht bei Fehlern
sauber ab, der Vergleich ist ein echter Zahlenvergleich, die Struktur liest sich wie Prosa. Und:
läuft identisch auf Windows/Linux/macOS. Kernbotschaft = die Faustregel unten. Das ist der
Motivations-Haken für einen Raum voller Leute, die Bash schon können: Python ist der nächste
logische Schritt, kein Bruch.
-->
