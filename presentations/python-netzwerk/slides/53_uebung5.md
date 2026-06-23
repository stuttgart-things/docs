---
layout: exercise
num: '21 · Übung 5'
datei: '05_api_debug.py · _broken.py'
zeit: '~20 Min'
---

<div class="page-label">Block 5 · Übung 5</div>

# API abfragen & <span class="accent">drei Fehler</span> jagen<span class="dot">.</span>

<div class="ex-goal">
  <div class="label">Ziel</div>
  <div class="text">Die API erweitern — und im kaputten Skript drei Fehler per Traceback finden.</div>
</div>

<div class="ex-grid">

  <div class="ex-card">
    <div class="ex-tag">Basis · 05_api_debug.py</div>
    <ul>
      <li>Gib zusätzlich den HTTP-Statuscode aus (<code>response.status_code</code>).</li>
      <li>Prüfe, ob die IP mit <code>"10."</code> beginnt → „privat" / „öffentlich".</li>
    </ul>
  </div>

  <div class="ex-card bonus">
    <div class="ex-tag">★ Bonus + Debugging · _broken.py</div>
    <ul>
      <li>Bonus: <code>api.github.com/meta</code> abfragen, CIDR-Bereiche unter <code>"hooks"</code> zählen.</li>
      <li>Debug: in <code>05_api_debug_broken.py</code> stecken <strong>drei</strong> Fehler — per Traceback finden: Tippfehler im <code>import</code>, fehlende <code>()</code>, falscher Key.</li>
    </ul>
  </div>

</div>

<!--
Die Abschlussübung bündelt den ganzen Tag. Basis auf dem heilen Skript: Statuscode ausgeben und
eine Bedingung auf die IP — wiederholt if/else und f-strings. Dann der Clou: das broken-Skript.
Es enthält genau drei Fehler, die sie nur über die Tracebacks finden sollen, EINEN nach dem
anderen: (1) import request statt requests → ModuleNotFoundError; (2) response.json ohne Klammern
→ es wird die Methode statt des Ergebnisses zugewiesen, später TypeError beim Indexieren;
(3) falscher Key data['address'] statt data['ip'] → KeyError. Nach jedem Fix neu ausführen.
Der GitHub-Bonus ist anspruchsvoll (User-Agent ist dort Pflicht, ohne Login rate-limited) — gutes
Futter für die Fortgeschrittenen. Lass Stefan und Adrian gezielt die Schnellen am Tisch
unterstützen, damit du dich um die Einsteiger kümmern kannst. Outbound/Proxy hier nochmal im Blick.
-->
