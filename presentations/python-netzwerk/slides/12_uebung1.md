---
layout: exercise
num: '07 · Übung 1'
datei: '01_grundlagen.py'
zeit: '~10 Min'
---

<div class="page-label">Block 1 · Übung 1</div>

# Variablen & ein <span class="accent">Dict-Eintrag</span><span class="dot">.</span>

<div class="ex-goal">
  <div class="label">Ziel</div>
  <div class="text">Eigene Werte anlegen und das Host→IP-Dictionary erweitern.</div>
</div>

<div class="ex-grid">

  <div class="ex-card">
    <div class="ex-tag">Basis</div>
    <ul>
      <li>Lege eine Variable <code>standort</code> an und gib sie mit aus.</li>
      <li>Füge dem Dictionary <code>ip_of</code> einen Eintrag für <code>"rtr-01"</code> hinzu.</li>
    </ul>
  </div>

  <div class="ex-card bonus">
    <div class="ex-tag">★ Profi-Bonus</div>
    <ul>
      <li>Gib für <strong>jedes</strong> Gerät aus <code>hosts</code> die IP aus.</li>
      <li>Fehlt ein Eintrag → <code>"unbekannt"</code> ausgeben.</li>
      <li>Tipp: <code>ip_of.get(host, "unbekannt")</code> in einer Schleife.</li>
    </ul>
  </div>

</div>

<!--
Erste eigene Übung — bewusst klein, damit jede:r ein Erfolgserlebnis hat. Die Basis ist in
wenigen Minuten machbar: eine neue Variable, ein neuer Dict-Eintrag mit
ip_of["rtr-01"] = "10.0.0.254". Beim Bonus kommt zum ersten Mal eine Schleife ins Spiel —
das nehmen wir gleich in Block 2 systematisch durch, hier dürfen die Schnellen schon
vorgreifen. .get() mit Default ist der elegante Weg, fehlende Schlüssel abzufangen, ohne dass
das Programm abstürzt. Geht herum, schaut auf die Bildschirme, lobt Zwischenergebnisse.
Wer fertig ist, hilft dem Sitznachbarn (Pair-Programming).
-->
