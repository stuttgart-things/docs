---
layout: default
num: '16 · venv & Bibliotheken'
meta: 'Block 4 · isolierte Umgebungen'
---

<div class="page-label">Block 4 · venv & Bibliotheken</div>

# Jedes Projekt in seiner <span class="accent">eigenen Blase</span><span class="dot">.</span>

<div style="display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 40px; margin-top: 26px; align-items: start;">

<div>

```bash {1|2|3|all}
python -m venv .venv                    # Umgebung anlegen
source .venv/bin/activate               # aktivieren (Linux/macOS)
pip install -r requirements.txt         # Bibliotheken installieren
```

<div style="margin-top: 22px;">

```powershell
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

</div>
</div>

<div>
<ul style="margin: 0; padding: 0; list-style: none; display: grid; gap: 16px; font-size: 21px; line-height: 1.4;">
  <li>· Pakete landen <strong>im Projekt</strong>, nicht systemweit.</li>
  <li>· Kein Versions-Chaos zwischen Projekten.</li>
  <li>· <span class="mono">requirements.txt</span> macht es reproduzierbar.</li>
  <li>· Aktive venv erkennst du am <span class="mono">(.venv)</span> im Prompt.</li>
</ul>

<div class="mantra" style="margin-top: 24px;">
  <div class="label">Merke</div>
  <div class="text">Erst <span class="mono">activate</span>, dann <span class="mono">pip install</span> — sonst landet das Paket im System.</div>
</div>
</div>

</div>

<!--
Warum venv? Stell dir vor, Projekt A braucht requests in Version 1, Projekt B in Version 2.
Installierst du systemweit, behindern sie sich. Eine venv ist eine isolierte Python-Umgebung pro
Projekt — eigene installierte Pakete, kein Durcheinander. Geh die drei Befehle einzeln durch:
venv anlegen (erzeugt den Ordner .venv), aktivieren (ab jetzt zeigt python/pip auf diese Blase),
installieren aus requirements.txt. Windows-Hinweis nicht vergessen: dort heißt der Aktivierungs-
befehl anders (Activate.ps1), und in PowerShell muss evtl. die ExecutionPolicy angepasst werden —
steht im Troubleshooting-Anhang. Häufiger Anfängerfehler: pip install OHNE vorher zu aktivieren;
dann fehlt das Paket in der venv und man wundert sich über ModuleNotFoundError.
-->
