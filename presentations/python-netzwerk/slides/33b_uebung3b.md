---
layout: exercise
num: '13 b · Zusatzübung 3'
datei: '03b_netzmaske.py'
zeit: '~15 Min'
---

<div class="page-label">Block 3 · Zusatzübung 3</div>

# Zwei Funktionen, die <span class="accent">zusammenspielen</span><span class="dot">.</span>

<div class="ex-goal">
  <div class="label">Ziel</div>
  <div class="text">Rückgabewerte, Umkehr-Funktionen und ein Default-Parameter.</div>
</div>

<div class="ex-grid">

  <div class="ex-card">
    <div class="ex-tag">Basis</div>
    <ul>
      <li>Schreibe <code>cidr_to_maske(cidr)</code> als Umkehrung zur vorgegebenen <code>maske_to_cidr()</code> — z. B. <code>24 → "255.255.255.0"</code>.</li>
      <li>Rufe beide mit ein paar Werten auf und vergleiche.</li>
    </ul>
  </div>

  <div class="ex-card bonus">
    <div class="ex-tag">★ Profi-Bonus</div>
    <ul>
      <li><code>host_erreichbar(host, versuche=3)</code> mit <strong>Default-Parameter</strong>.</li>
      <li>Einmal mit, einmal ohne <code>versuche</code> aufrufen; in einer Schleife auf mehrere Hosts anwenden.</li>
    </ul>
  </div>

</div>

<!--
Zusatzübung Block 3 — vertieft Funktionen. Die Basis (maske_to_cidr) ist schon vorgegeben und
zählt die 1-Bits; die Teilnehmer schreiben die Umkehrung. Das übt Rückgabewerte und ein bisschen
Zahlen-/String-Handling. Der eigentliche Lernpunkt im Bonus: Default-Parameter (versuche=3) — die
Funktion lässt sich mit ODER ohne dieses Argument aufrufen. Der Ping wird nur simuliert, damit es
ohne Netz/Rechte läuft (Windows-freundlich, kein echtes ping-Kommando nötig). Datei: 03b_netzmaske.py.
-->
