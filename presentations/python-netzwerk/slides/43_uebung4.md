---
layout: exercise
num: '17 · Übung 4'
datei: '04_module/'
zeit: '~20 Min'
---

<div class="page-label">Block 4 · Übung 4</div>

# Aufteilen & eine <span class="accent">venv</span> bauen<span class="dot">.</span>

<div class="ex-goal">
  <div class="label">Ziel</div>
  <div class="text">Code in <span class="mono">main.py</span> + <span class="mono">netutils.py</span> trennen und eine venv anlegen.</div>
</div>

<div class="ex-grid">

  <div class="ex-card">
    <div class="ex-tag">Basis</div>
    <ul>
      <li>Ergänze in <code>netutils.py</code> eine Funktion <code>is_in_subnet(ip, prefix)</code> und nutze sie in <code>main.py</code> (Import nicht vergessen!).</li>
      <li>Lege eine venv an und installiere <code>requirements.txt</code>.</li>
    </ul>
  </div>

  <div class="ex-card bonus">
    <div class="ex-tag">★ Profi-Bonus</div>
    <ul>
      <li>Gib die Ergebnisse mit <code>rich</code> als hübsche <strong>Tabelle</strong> aus.</li>
      <li>Tipp: <code>from rich.table import Table</code></li>
    </ul>
  </div>

</div>

<!--
Die erste „große" Übung — 20 Minuten, weil hier auch venv-Setup mit drin ist. Basis-Teil 1: eine
neue Funktion ins Modul schreiben und in main.py importieren — das übt das Modul-Konzept aus dem
Theorieteil. Basis-Teil 2: die drei venv-Befehle ausführen und requests/rich installieren. Genau
hier tauchen erfahrungsgemäß Umgebungsprobleme auf: Wer im Browser-code-server ist, hat ein
Terminal — super. Wer Windows lokal nutzt, braucht den anderen Aktivierungsbefehl. Bei
Proxy/Outbound-Problemen beim pip install auf den Anhang verweisen. Der Bonus mit rich gibt ein
schönes Erfolgserlebnis (bunte Tabelle) und zeigt, wie einfach externe Bibliotheken den Code
aufwerten. Co-Coaches sollten in dieser Phase besonders aktiv durch die Reihen gehen.
-->
