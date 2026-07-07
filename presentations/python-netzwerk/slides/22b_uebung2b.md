---
layout: exercise
num: '09 b · Zusatzübung 2'
datei: '02b_ipfile.py'
zeit: '~15 Min'
---

<div class="page-label">Block 2 · Zusatzübung 2</div>

# Echte Datei einlesen & <span class="accent">auswerten</span><span class="dot">.</span>

<div class="ex-goal">
  <div class="label">Ziel</div>
  <div class="text">Die Datei <span class="mono">data/ips.txt</span> zeilenweise lesen und zählen.</div>
</div>

<div class="ex-grid">

  <div class="ex-card">
    <div class="ex-tag">Basis</div>
    <ul>
      <li>Gib nur die Adressen aus, die <strong>nicht</strong> mit <code>"10."</code> beginnen.</li>
      <li>Zähle private (10./192.168./172.16.) vs. öffentliche und gib beide Zahlen aus.</li>
    </ul>
  </div>

  <div class="ex-card bonus">
    <div class="ex-tag">★ Profi-Bonus</div>
    <ul>
      <li>Finde mit einer <code>while</code>-Schleife die <strong>erste</strong> öffentliche Adresse, dann <code>break</code>.</li>
      <li>Gib ihre Position (Index) aus.</li>
    </ul>
  </div>

</div>

<!--
Zusatzübung Block 2 — erstes Mal eine Datei einlesen, gute Zeitreserve. Das Datei-Öffnen und der
Pfad sind bereits vorgegeben (pathlib, plattformunabhängig) — das Skript läuft auf Windows genauso
aus jedem Verzeichnis, weil der Pfad relativ zur Datei gebaut wird. Betone kurz: encoding="utf-8"
setzt man unter Windows besser explizit, sonst rät Python (cp1252) und Umlaute können kippen. Fokus
der Aufgabe ist die Auswertung: negierte Bedingung (not startswith bzw. else-Zweig) und Zählen.
Der Bonus führt while + break ein — Abbruch, sobald eine Bedingung erfüllt ist. Datei: 02b_ipfile.py.
-->
