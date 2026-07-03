---
layout: default
num: '06 · Einzelwerte'
meta: 'Block 1 · 01_grundlagen.py · str · int · float · bool'
---

<div class="page-label">Block 1 · Variablen & Datentypen (1/2)</div>

# Vier Werte — und Python <span class="accent">kennt den Typ selbst</span><span class="dot">.</span>

<div style="display: grid; grid-template-columns: 0.72fr 1.28fr; gap: 44px; margin-top: 26px; align-items: start;">

<div>
<ul style="margin: 0; padding: 0; list-style: none; display: grid; gap: 18px; font-size: 25px; line-height: 1.35;">
  <li><span class="mono accent">str</span> &nbsp;Text — <span class="muted">Hostname</span></li>
  <li><span class="mono accent">int</span> &nbsp;Ganzzahl — <span class="muted">Port-Anzahl</span></li>
  <li><span class="mono accent">float</span> &nbsp;Kommazahl — <span class="muted">CPU-Last</span></li>
  <li><span class="mono accent">bool</span> &nbsp;<span class="mono">True/False</span> — <span class="muted">online?</span></li>
</ul>

<div class="mantra" style="margin-top: 28px;">
  <div class="label">f-string</div>
  <div class="text"><span class="mono">f"...{variable}..."</span> setzt Werte direkt in den Text ein — auch Rechnungen.</div>
</div>
</div>

```python {1-4|6-9|8|all}
hostname   = "router-stuttgart-01"   # str   · Text
port_count = 48                      # int   · Ganzzahl
cpu_load   = 0.41                    # float · Kommazahl
is_online  = True                    # bool  · True/False

print("=== Geräte-Info ===")
print(f"Hostname : {hostname}")
print(f"CPU-Last : {cpu_load * 100:.0f} %")
print(f"Online   : {is_online}")
```

</div>

<style scoped>
.slidev-code { font-size: 26px !important; line-height: 1.6 !important; padding: 32px !important; }
</style>

<!--
Erste von zwei Datentyp-Slides — hier nur die vier Einzelwerte, damit der Code groß und lesbar
ist. Kernbotschaft: man deklariert den Typ NICHT, Python erkennt ihn am Wert (dynamisch typisiert,
Anknüpfung an die Vergleichs-Folie). Highlights durchgehen: erst die vier Zuweisungen, dann die
print-Zeilen mit f-strings. Betone bei Zeile 8, dass in den geschweiften Klammern ein echter
Ausdruck steht — cpu_load * 100 wird gerechnet, :.0f rundet auf ganze Prozent. REPL-Tipp: jede
Zeile lässt sich auch interaktiv im python-Prompt ausprobieren; für echte Programme aber in eine
.py-Datei schreiben und als Ganzes ausführen. Sammlungen (list/dict) kommen auf der nächsten Slide.
-->
