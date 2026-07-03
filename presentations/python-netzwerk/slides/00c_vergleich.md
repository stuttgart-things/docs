---
layout: default
num: 'Im Vergleich'
meta: 'Python neben Bash, Go, JavaScript & C'
---

<div class="page-label">Python im Vergleich</div>

# Welche Sprache <span class="accent">wofür</span><span class="dot">.</span>

<p class="lede">
Jede Sprache hat ihren Sweet Spot. Python liegt im goldenen Mittelweg: viel mächtiger als ein
Shell-Skript, aber deutlich einfacher zu schreiben als Go, Java oder C.
</p>

<table class="agenda" style="margin-top: 22px;">
  <tr style="opacity: 0.55; font-size: 15px; text-transform: uppercase; letter-spacing: 0.08em;">
    <td class="t-slot">Sprache</td>
    <td class="t-time">Jahr</td>
    <td class="t-slot">Von</td>
    <td class="t-slot">Typischer Einsatz</td>
    <td class="t-meta">Stärke / Schwäche</td>
  </tr>
  <tr>
    <td class="t-slot" style="font-weight: 600;"><span class="mono accent">Python</span></td>
    <td class="t-time">1991</td>
    <td class="t-slot">Guido van Rossum</td>
    <td class="t-slot">Automatisierung, APIs, Datenauswertung, KI</td>
    <td class="t-meta">lesbar, riesige Bibliothek</td>
  </tr>
  <tr>
    <td class="t-slot" style="font-weight: 600;"><span class="mono">Bash</span></td>
    <td class="t-time">1989</td>
    <td class="t-slot">Brian Fox · GNU</td>
    <td class="t-slot">Kurze Einzeiler, Dateien & Befehle verketten</td>
    <td class="t-meta">stark im Terminal, schnell unübersichtlich</td>
  </tr>
  <tr>
    <td class="t-slot" style="font-weight: 600;"><span class="mono">Go</span></td>
    <td class="t-time">2009</td>
    <td class="t-slot">Google</td>
    <td class="t-slot">Schnelle CLI-Tools, Netzwerk-Services</td>
    <td class="t-meta">sehr schnell, eine fertige Binärdatei</td>
  </tr>
  <tr>
    <td class="t-slot" style="font-weight: 600;"><span class="mono">JavaScript</span></td>
    <td class="t-time">1995</td>
    <td class="t-slot">Brendan Eich · Netscape</td>
    <td class="t-slot">Web-Oberflächen, Browser & Frontend</td>
    <td class="t-meta">Sprache des Webs</td>
  </tr>
  <tr>
    <td class="t-slot" style="font-weight: 600;"><span class="mono">C / C++</span></td>
    <td class="t-time">1972 / 85</td>
    <td class="t-slot">Ritchie · Stroustrup</td>
    <td class="t-slot">Systemnahes, maximale Performance</td>
    <td class="t-meta">mächtig, aber aufwändig & fehleranfällig</td>
  </tr>
</table>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-top: 28px;">
  <div class="mantra" style="margin: 0;">
    <div class="label">Python ist…</div>
    <div class="text">interpretiert (kein Kompilieren), dynamisch typisiert (Typ ergibt sich aus dem Wert) und auf Lesbarkeit getrimmt.</div>
  </div>
  <div class="mantra" style="margin: 0;">
    <div class="label">Faustregel</div>
    <div class="text">Zu viel für Bash, aber kein Hochleistungs-Dienst? → Python ist fast immer die richtige Wahl.</div>
  </div>
</div>

<!--
Einordnung, keine Glaubensdiskussion. Ziel: Die Gruppe versteht, WANN Python die richtige Wahl
ist. Bash kennen viele aus dem Netzwerk-Alltag — super für Einzeiler, wird aber bei echter Logik
(Schleifen, Fehlerbehandlung, Datenstrukturen) schnell unleserlich. Genau da setzt Python an.
Go und C sind kompiliert und schneller, aber für unsere Automatisierungs-Aufgaben Overkill.
Die zwei Begriffe unten kurz erklären: „interpretiert" = wir führen den Code direkt aus, kein
extra Übersetzungsschritt; „dynamisch typisiert" = wir schreiben nicht hin, ob etwas Text oder
Zahl ist, Python merkt es selbst (Anknüpfung an die Variablen-Folie später). Faustregel betonen.
-->
