---
layout: exercise
num: '17 b · Zusatzübung 4'
datei: '04_module/report.py'
zeit: '~20 Min'
---

<div class="page-label">Block 4 · Zusatzübung 4</div>

# Ein <span class="accent">zweites Modul</span>, das mitbenutzt<span class="dot">.</span>

<div class="ex-goal">
  <div class="label">Ziel</div>
  <div class="text"><span class="mono">report.py</span> importiert <span class="mono">netutils</span> — ein Modul, viele Nutzer.</div>
</div>

<div class="ex-grid">

  <div class="ex-card">
    <div class="ex-tag">Basis</div>
    <ul>
      <li>Ergänze in <code>report.py</code> eine Zählung <strong>pro Subnetz</strong> (nutze <code>subnet_prefix</code>).</li>
      <li>Rufe <code>summary()</code> zusätzlich aus <code>main.py</code> auf.</li>
    </ul>
  </div>

  <div class="ex-card bonus">
    <div class="ex-tag">★ Profi-Bonus</div>
    <ul>
      <li>Schreibe das Ergebnis in <code>report.txt</code> — <code>open(..., "w", encoding="utf-8")</code>.</li>
      <li>Prüfen: <code>type report.txt</code> (Windows) · <code>cat report.txt</code> (Linux/macOS).</li>
    </ul>
  </div>

</div>

<!--
Zusatzübung Block 4 — festigt das Modul-Konzept: dasselbe netutils.py wird jetzt von main.py UND
report.py importiert. Das ist der eigentliche Wert von Modulen (einmal schreiben, mehrfach nutzen).
Basis: eine kleine Auswertung pro Subnetz plus Cross-Import. Windows-Hinweise bewusst mit drin:
encoding="utf-8" beim Schreiben (sonst cp1252-Überraschungen), und zum Anschauen 'type' statt 'cat'.
Wer venv aus Übung 4 noch nicht aktiviert hat: unter Windows .venv\Scripts\Activate.ps1 (siehe
Theorie-Slide/Anhang). Datei: 04_module/report.py.
-->
