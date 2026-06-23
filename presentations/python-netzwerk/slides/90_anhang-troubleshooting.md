---
layout: default
class: 'is-appendix'
num: 'Anhang A · Troubleshooting'
meta: 'Login · Proxy · Dev Container · venv/Windows'
---

<div class="page-label">Anhang A · Setup-Troubleshooting</div>

# Wenn's beim <span class="accent">Setup</span> klemmt<span class="dot">.</span>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 26px; margin-top: 28px;">

  <div class="surface" style="padding: 24px 30px;">
    <div class="mono accent" style="font-size: 14px; letter-spacing: 0.14em;">CODE-SERVER LOGIN</div>
    <ul style="margin: 12px 0 0; padding: 0; list-style: none; display: grid; gap: 9px; font-size: 18px; line-height: 1.4;">
      <li>· Seite lädt nicht? URL <span class="mono">&lt;name&gt;.&lt;domain&gt;</span> exakt prüfen (Wildcard-DNS, kein Sub-Pfad).</li>
      <li>· Passwort kommt nicht? Groß/klein beachten, vom Trainer neu geben lassen.</li>
      <li>· Kein „Run in Terminal"? Terminal manuell: <span class="mono">python datei.py</span>.</li>
    </ul>
  </div>

  <div class="surface" style="padding: 24px 30px;">
    <div class="mono accent" style="font-size: 14px; letter-spacing: 0.14em;">OUTBOUND / PROXY</div>
    <ul style="margin: 12px 0 0; padding: 0; list-style: none; display: grid; gap: 9px; font-size: 18px; line-height: 1.4;">
      <li>· Übung 5 / <span class="mono">pip</span> hängt? Firmen-Proxy nötig:</li>
      <li><span class="mono" style="font-size: 16px;">export HTTPS_PROXY=http://&lt;proxy&gt;:&lt;port&gt;</span></li>
      <li>· <span class="mono">requests</span> nutzt <span class="mono">HTTPS_PROXY</span> automatisch.</li>
    </ul>
  </div>

  <div class="surface" style="padding: 24px 30px;">
    <div class="mono accent" style="font-size: 14px; letter-spacing: 0.14em;">DEV CONTAINER</div>
    <ul style="margin: 12px 0 0; padding: 0; list-style: none; display: grid; gap: 9px; font-size: 18px; line-height: 1.4;">
      <li>· VS Code: Befehlspalette → <span class="mono">„Reopen in Container"</span>.</li>
      <li>· Erst dann gibt es MS-Python + Pylance + GUI-Debugger.</li>
      <li>· Docker muss laufen; erster Build dauert etwas.</li>
    </ul>
  </div>

  <div class="surface" style="padding: 24px 30px;">
    <div class="mono accent" style="font-size: 14px; letter-spacing: 0.14em;">VENV UNTER WINDOWS</div>
    <ul style="margin: 12px 0 0; padding: 0; list-style: none; display: grid; gap: 9px; font-size: 18px; line-height: 1.4;">
      <li>· Aktivieren: <span class="mono">.venv\Scripts\Activate.ps1</span></li>
      <li>· „Skript deaktiviert"? In PowerShell:</li>
      <li><span class="mono" style="font-size: 15px;">Set-ExecutionPolicy -Scope CurrentUser RemoteSigned</span></li>
    </ul>
  </div>

</div>

<!--
Diese Slide ist Nachschlagewerk, nicht zum Vortragen — auf sie verweisen, wenn jemand hängt.
Wichtigster realer Stolperstein: code-server läuft über Open VSX, deshalb gibt es im Browser KEINE
MS-Python-Extension und keinen GUI-Debugger; das ist normal, nicht kaputt. Wer den vollen Debugger
will, nutzt den Dev Container oder lokal. Zweiter Klassiker: Übung 5 und pip brauchen Outbound-
HTTPS; im Firmennetz über HTTPS_PROXY. Das ist sogar ein guter Lehrmoment über Netz und Proxys.
Windows-PowerShell blockt teils die Aktivierung — ExecutionPolicy-Befehl hilft. Platzhalter
<name>.<domain>, <proxy>:<port> vorab füllen, soweit bekannt.
-->
