---
layout: exercise
num: '09 · Übung 2'
datei: '02_filter.py'
zeit: '~15 Min'
---

<div class="page-label">Block 2 · Übung 2</div>

# Filtern und <span class="accent">zählen</span><span class="dot">.</span>

<div class="ex-goal">
  <div class="label">Ziel</div>
  <div class="text">Adressen nach Präfix filtern und das Ergebnis zählen.</div>
</div>

<div class="ex-grid">

  <div class="ex-card">
    <div class="ex-tag">Basis</div>
    <ul>
      <li>Gib alle Adressen aus, die mit <code>"192.168."</code> beginnen.</li>
      <li>Zähle mit, <strong>wie viele</strong> das sind, und gib die Zahl am Ende aus.</li>
    </ul>
  </div>

  <div class="ex-card bonus">
    <div class="ex-tag">★ Profi-Bonus</div>
    <ul>
      <li>Baue ein Zähl-Dict <strong>pro Präfix</strong> (<code>"10."</code>, <code>"172."</code>, <code>"192.168."</code>, <code>"8."</code>).</li>
      <li>Tipp: <code>zaehler[p] = zaehler.get(p, 0) + 1</code></li>
    </ul>
  </div>

</div>

<!--
Aufbauend auf Übung 1: jetzt die Schleife selbst schreiben. Basis: startswith auf "192.168."
ändern und einen Zähler hochzählen (eine Variable count = 0 vor der Schleife, count += 1 im if,
am Ende ausgeben). Der Bonus führt das Zähl-Dict-Muster ein — das ist ein extrem häufiges Muster
in der Praxis (Häufigkeiten zählen). .get(p, 0) liefert 0, wenn der Präfix noch nicht im Dict
steht, sonst den bisherigen Wert. Für ganz Schnelle: man könnte den Präfix auch aus der IP
ableiten statt fest vorzugeben. 15 Minuten sind großzügig — wer früh fertig ist, macht den Bonus
oder hilft. Häufiger Stolperstein: count INNERHALB statt außerhalb der Schleife initialisiert.
-->
