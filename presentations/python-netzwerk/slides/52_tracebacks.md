---
layout: default
num: '20 · Tracebacks lesen'
meta: 'Block 5 · „Es tut nicht"'
---

<div class="page-label">Block 5 · Tracebacks lesen</div>

# „Es tut nicht" — <span class="accent">von unten lesen</span><span class="dot">.</span>

<div style="display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 40px; margin-top: 26px; align-items: center;">

<div class="traceback">Traceback (most recent call last):
  File "05_api_debug_broken.py", line 12, in &lt;module&gt;
    import request
<span class="tb-err">ModuleNotFoundError: No module named 'request'</span>
<span class="tb-hint">↑  Lies von UNTEN nach OBEN.</span></div>

<div>
<ul style="margin: 0; padding: 0; list-style: none; display: grid; gap: 16px; font-size: 22px; line-height: 1.4;">
  <li><strong>Letzte Zeile</strong> = der Fehlertyp + Klartext.</li>
  <li>Darüber: <strong>Datei + Zeile</strong>, wo es knallt.</li>
  <li>Erst <strong>verstehen</strong>, dann ändern — eine Sache pro Versuch.</li>
</ul>

<div class="mantra" style="margin-top: 24px;">
  <div class="label">Werkzeuge</div>
  <div class="text"><span class="mono">print(typ, wert)</span> für Zwischenstände · <span class="mono">import pdb; pdb.set_trace()</span> als Haltepunkt.</div>
</div>
</div>

</div>

<!--
Das ist die Lebensversicherung für Einsteiger: Ein Traceback sieht erschreckend aus, ist aber
ein freundlicher Wegweiser. DIE Regel: von unten nach oben lesen. Die unterste Zeile nennt den
Fehlertyp (hier ModuleNotFoundError) und sagt im Klartext, was los ist (kein Modul 'request' —
weil es requests heißt, mit s). Die Zeile darüber zeigt Datei und Zeilennummer, wo es passiert.
Goldene Regel beim Beheben: immer nur EINEN Fehler auf einmal beheben und neu ausführen — sonst
weiß man nicht, was geholfen hat. Genau das machen sie gleich in Übung 5 mit dem broken-Skript.
Werkzeuge: print ist das simpelste Debugging (Zwischenwerte ausgeben), pdb ist der eingebaute
Debugger fürs Terminal — im Browser-code-server der Weg, weil der GUI-Debugger dort fehlt.
Wer lokal/Dev-Container arbeitet, kann zusätzlich den grafischen Debugger zeigen.
-->
