---
layout: default
num: '01 · Wie wir heute arbeiten'
meta: 'Ein Übungs-Repo · drei Umgebungen · freie Wahl'
---

<div class="page-label">01 · Wie wir heute arbeiten</div>

# Gleiche Aufgaben, <span class="accent">freie Wahl</span> der Umgebung<span class="dot">.</span>

<p class="lede" style="margin-top: 14px; max-width: 86ch;">
Es gibt <strong>ein</strong> Übungs-Repo und drei Wege, es zu öffnen. Such dir den Weg aus,
der zu dir passt — die Aufgaben sind überall identisch.
</p>

<div style="display: flex; justify-content: center; margin-top: 28px;">

```mermaid {scale: 0.92}
flowchart LR
  R["📦 Übungs-Repo<br/>01 … 05 + Spickzettel"]
  R --> A["🌐 Browser-Pod<br/>code-server<br/><i>null Setup</i>"]
  R --> B["🐳 Dev Container<br/>Docker + VS Code<br/><i>voller Debugger</i>"]
  R --> C["💻 Lokal pur<br/>eigenes Python + venv<br/><i>ohne Docker</i>"]
  A --> Z(["Dieselben fünf Übungen"])
  B --> Z
  C --> Z
```

</div>

<div class="mantra" style="margin-top: 26px;">
  <div class="label">Empfehlung</div>
  <div class="text">Einsteiger → Browser-Link (sofort startklar). Fortgeschrittene → lokal / Dev Container mit vollem GUI-Debugger.</div>
</div>

<!--
Die wichtigste Botschaft des Tages: Ihr müsst euch nicht mit Setup aufhalten. Wer einfach
loslegen will, nimmt den Browser-Pod — Link aufrufen, Passwort eingeben, fertig. Wer es lokal
„richtig" will und Docker hat, nimmt den Dev Container — dort gibt es die echte MS-Python-
Extension, Pylance und den grafischen Debugger. Wer schon ein Python auf dem Rechner hat, kann
auch komplett lokal mit venv arbeiten. Wichtig für später: Im Browser-code-server gibt es den
GUI-Debugger NICHT (Open VSX statt MS-Marketplace) — dort debuggen wir über Terminal und pdb.
Das ist gleich bei Block 5 relevant. Einsteiger zum Browser-Link lotsen, Fortgeschrittene gern
lokal — die helfen dann auch am Tisch mit.
-->
