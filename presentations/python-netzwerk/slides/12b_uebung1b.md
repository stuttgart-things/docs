---
layout: exercise
num: '07 b · Zusatzübung 1'
datei: '01b_strings.py'
zeit: '~10 Min'
---

<div class="page-label">Block 1 · Zusatzübung 1</div>

# Strings <span class="accent">zerlegen & formatieren</span><span class="dot">.</span>

<div class="ex-goal">
  <div class="label">Ziel</div>
  <div class="text">Hostnamen aufteilen und Werte sauber formatiert ausgeben.</div>
</div>

<div class="ex-grid">

  <div class="ex-card">
    <div class="ex-tag">Basis</div>
    <ul>
      <li>Baue aus den Teilen von <code>"sw-stuttgart-07"</code> einen FQDN wie <code>sw07.stuttgart.example.com</code>.</li>
      <li>Gib eine CPU-Last <code>0.4267</code> als <code>42.7 %</code> aus. Tipp: <code>f"{w*100:.1f} %"</code></li>
    </ul>
  </div>

  <div class="ex-card bonus">
    <div class="ex-tag">★ Profi-Bonus</div>
    <ul>
      <li>Schreibe die MAC <code>a0:b1:c2:d3:e4:f5</code> ins Cisco-Format <code>a0b1.c2d3.e4f5</code> um.</li>
      <li>Doppelpunkte weg → 4er-Gruppen → mit Punkten verbinden.</li>
    </ul>
  </div>

</div>

<!--
Zusatzübung für Block 1 — reine String-Arbeit, gute Zeitreserve nach Übung 1. Die Basis übt
.split(), Indexzugriff und f-string-Formatierung mit Nachkommastellen (:.1f). Häufiger Aha-Moment:
dass man Strings mit + oder im f-string frei zusammenbauen kann. Der Bonus (Cisco-MAC-Format) ist
ein kleines Slicing-/Gruppierungs-Puzzle: mac.replace(":", "") und dann in 4er-Schritten schneiden.
Wer schnell ist, kann das auch über eine Schleife lösen. Datei: 01b_strings.py.
-->
