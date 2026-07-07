---
layout: exercise
num: '21 b · Zusatzübung 5'
datei: '05c_api_robust.py'
zeit: '~20 Min'
---

<div class="page-label">Block 5 · Zusatzübung 5</div>

# Zweite API — und <span class="accent">Fehler abfangen</span><span class="dot">.</span>

<div class="ex-goal">
  <div class="label">Ziel</div>
  <div class="text">Eine API robust mit <span class="mono">try/except</span> abfragen — nichts stürzt mehr ab.</div>
</div>

<div class="ex-grid">

  <div class="ex-card">
    <div class="ex-tag">Basis</div>
    <ul>
      <li>Gib zusätzlich die Ziel-URL aus (<code>data["url"]</code>).</li>
      <li>Setze die URL auf <code>httpbin.org/status/404</code> und beobachte, wie der Fehler im <code>except</code>-Zweig landet.</li>
    </ul>
  </div>

  <div class="ex-card bonus">
    <div class="ex-tag">★ Profi-Bonus</div>
    <ul>
      <li>Baue in eine <strong>Kopie</strong> selbst zwei Fehler ein (Tippfehler im Key, fehlende Klammern).</li>
      <li>Sitznachbar findet sie per Traceback — dann Rollen tauschen.</li>
    </ul>
  </div>

</div>

<!--
Zusatzübung Block 5 — hebt das API-Thema auf „robust". Das Skript nutzt httpbin.org (offen, ohne
Login) und zeigt das try/except-Muster um die Abfrage. Basis: ein Feld mehr auslesen und den
Fehlerfall bewusst provozieren (status/404) — schöner Aha-Moment, dass raise_for_status den Fehler
sauber ins except leitet, statt das Programm zu killen. Der Bonus dreht Übung 5 um: sie bauen selbst
Bugs ein und debuggen gegenseitig — das festigt „Traceback von unten lesen" spielerisch. Outbound/
Proxy im Blick behalten (Anhang). Läuft plattformunabhängig, auch Windows. Datei: 05c_api_robust.py.
-->
