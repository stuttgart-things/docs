---
layout: default
num: '06 · Sammlungen'
meta: 'Block 1 · 01_grundlagen.py · list · dict'
---

<div class="page-label">Block 1 · Variablen & Datentypen (2/2)</div>

# Viele Werte auf einmal: <span class="accent">list</span> &amp; <span class="accent">dict</span><span class="dot">.</span>

<div style="display: grid; grid-template-columns: 0.72fr 1.28fr; gap: 44px; margin-top: 26px; align-items: start;">

<div>
<ul style="margin: 0; padding: 0; list-style: none; display: grid; gap: 20px; font-size: 25px; line-height: 1.35;">
  <li><span class="mono accent">list</span> &nbsp;geordnete Reihe<br/><span class="muted" style="font-size: 20px;">Geräteliste — mit <span class="mono">len()</span> zählbar</span></li>
  <li><span class="mono accent">dict</span> &nbsp;Schlüssel → Wert<br/><span class="muted" style="font-size: 20px;">Host → IP — Nachschlagen per Schlüssel</span></li>
</ul>

<div class="mantra" style="margin-top: 28px;">
  <div class="label">Zugriff</div>
  <div class="text"><span class="mono">hosts[0]</span> über Position · <span class="mono">ip_of["sw-02"]</span> über Schlüssel.</div>
</div>
</div>

```python {1|3-7|9|10|all}
hosts = ["sw-01", "sw-02", "fw-01", "rtr-01"]   # list

ip_of = {                                        # dict
    "sw-01": "10.0.1.11",
    "sw-02": "10.0.1.12",
    "fw-01": "10.0.0.1",
}

print(f"Wir verwalten {len(hosts)} Geräte")
print(f"IP von sw-02: {ip_of['sw-02']}")
```

</div>

<style scoped>
.slidev-code { font-size: 26px !important; line-height: 1.6 !important; padding: 32px !important; }
</style>

<!--
Zweite Datentyp-Slide: die beiden Sammlungen. list = geordnete Reihe von Werten, Zugriff über die
Position (hosts[0] ist das erste Element, Zählung ab 0!), Länge mit len(). dict = Nachschlage-
tabelle aus Schlüssel-Wert-Paaren, Zugriff über den Schlüssel (ip_of["sw-02"]). Genau diese beiden
Strukturen brauchen sie gleich in Übung 1 (Dictionary-Eintrag ergänzen) und immer wieder — eine
API-Antwort ist am Ende auch nur ein dict aus Listen und dicts. Highlights: erst die Liste, dann
das dict über mehrere Zeilen (gut lesbar, ein Paar pro Zeile), dann len() und der Schlüsselzugriff.
Auf das Detail hinweisen: im f-string die Anführungszeichen des Schlüssels anders setzen als die
des Strings (hier ' innen, " außen), sonst Syntaxfehler.
-->
