---
layout: exercise
num: '13 · Übung 3'
datei: '03_refactor.py'
zeit: '~15 Min'
---

<div class="page-label">Block 3 · Übung 3</div>

# Schreib deine erste <span class="accent">Funktion</span><span class="dot">.</span>

<div class="ex-goal">
  <div class="label">Ziel</div>
  <div class="text">Die Copy-Paste-Blöcke durch <span class="mono">klassifiziere(ip)</span> ersetzen.</div>
</div>

<div class="ex-grid">

  <div class="ex-card">
    <div class="ex-tag">Basis</div>
    <ul>
      <li>Schreibe <code>def klassifiziere(ip):</code>, die privat/öffentlich entscheidet.</li>
      <li>Rufe sie für <code>ip1</code>, <code>ip2</code>, <code>ip3</code> auf.</li>
    </ul>
  </div>

  <div class="ex-card bonus">
    <div class="ex-tag">★ Profi-Bonus</div>
    <ul>
      <li>Ergänze einen <strong>Docstring</strong> und einen sinnvollen Rückgabewert (<code>bool</code> oder <code>str</code>).</li>
      <li>Verarbeite eine ganze <strong>Liste</strong> von IPs in einer Schleife.</li>
    </ul>
  </div>

</div>

<!--
Jetzt selbst machen, was wir gerade gezeigt haben. Basis: eine Funktion mit einem Parameter,
die das if/else aus dem Vorher-Block enthält und den Wert ausgibt oder zurückgibt. Wichtig zu
beobachten: dass sie den Parameter (ip) im Funktionskörper benutzen und nicht aus Versehen wieder
die globale Variable. Bonus: return statt print (Trennung von Logik und Ausgabe — ein wichtiges
Konzept), plus Docstring. Wer die Liste-in-Schleife schafft, hat das Muster für den ganzen Rest
des Tages verstanden. Häufiger Fehler: vergessene Klammern beim Aufruf — klassifiziere ist die
Funktion, klassifiziere(ip) ruft sie auf. Das ist auch in Übung 5 ein Debugging-Thema. Co-Coaches
kümmern sich gezielt um die, die mit der Funktionssyntax hadern.
-->
