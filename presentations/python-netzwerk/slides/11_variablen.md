---
layout: default
num: '06 · Variablen & Datentypen'
meta: 'Block 1 · 01_grundlagen.py'
---

<div class="page-label">Block 1 · Variablen & Datentypen</div>

# Sechs Bausteine, mehr <span class="accent">braucht's erstmal nicht</span><span class="dot">.</span>

<div style="display: grid; grid-template-columns: 0.85fr 1.15fr; gap: 40px; margin-top: 24px; align-items: start;">

<div>
<ul style="margin: 0; padding: 0; list-style: none; display: grid; gap: 14px; font-size: 23px; line-height: 1.35;">
  <li><span class="mono accent">str</span> &nbsp;Text — <span class="muted">Hostname</span></li>
  <li><span class="mono accent">int</span> &nbsp;Ganzzahl — <span class="muted">Port-Anzahl</span></li>
  <li><span class="mono accent">float</span> &nbsp;Kommazahl — <span class="muted">CPU-Last</span></li>
  <li><span class="mono accent">bool</span> &nbsp;<span class="mono">True/False</span> — <span class="muted">online?</span></li>
  <li><span class="mono accent">list</span> &nbsp;Reihenfolge — <span class="muted">Geräteliste</span></li>
  <li><span class="mono accent">dict</span> &nbsp;Schlüssel→Wert — <span class="muted">Host→IP</span></li>
</ul>

<div class="mantra" style="margin-top: 26px;">
  <div class="label">f-string</div>
  <div class="text"><span class="mono">f"...{variable}..."</span> setzt Werte direkt in den Text ein.</div>
</div>
</div>

```python {1-4|6-9|11|12|14-15|all}
hostname   = "router-stuttgart-01"   # str
port_count = 48                      # int
cpu_load   = 0.41                    # float
is_online  = True                    # bool

print("=== Geräte-Info ===")
print(f"Hostname : {hostname}")
print(f"CPU-Last : {cpu_load * 100:.0f} %")
print(f"Online   : {is_online}")

hosts = ["sw-01", "sw-02", "fw-01", "rtr-01"]      # list
ip_of = {"sw-01": "10.0.1.11", "sw-02": "10.0.1.12"}  # dict

print(f"Wir verwalten {len(hosts)} Geräte")
print(f"IP von sw-02: {ip_of['sw-02']}")
```

</div>

<!--
Das ist der Code aus 01_grundlagen.py. Geht die Highlights Schritt für Schritt durch:
Erst die vier Einzelwerte (str/int/float/bool) — betont, dass man den Typ NICHT deklariert,
Python erkennt ihn am Wert. Dann die print-Zeilen mit f-strings: der Ausdruck in den
geschweiften Klammern wird ausgewertet, auch Rechnungen wie cpu_load * 100. Dann die list
(geordnete Sammlung, mit len() zählbar) und das dict (Nachschlagen über den Schlüssel,
ip_of['sw-02']). Tipp für die REPL-vs-Skript-Frage: man kann jede Zeile auch interaktiv im
Python-Prompt ausprobieren (python eingeben, Enter) — zum Lernen super, für echte Programme
schreibt man sie aber in eine .py-Datei und führt sie als Ganzes aus.
-->
