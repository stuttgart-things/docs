---
layout: default
num: '15 · Ordnerstruktur & Module'
meta: 'Block 4 · 04_module/'
---

<div class="page-label">Block 4 · Ordnerstruktur & Module</div>

# Ein Projekt hat eine <span class="accent">Struktur</span><span class="dot">.</span>

<div style="display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 44px; margin-top: 24px; align-items: center;">

<div style="display: flex; justify-content: center;">

```mermaid {scale: 0.95}
flowchart TD
  M["main.py<br/><i>steuert den Ablauf</i>"]
  N["netutils.py<br/><i>IP-Hilfsfunktionen</i>"]
  D["data/ips.txt<br/><i>Eingabedaten</i>"]
  R["requirements.txt<br/><i>Abhängigkeiten</i>"]
  V[".venv/<br/><i>isolierte Umgebung</i>"]
  M -- "from netutils import …" --> N
  M -. "liest" .-> D
  R -- "pip install -r" --> V
```

</div>

<div>
<ul style="margin: 0; padding: 0; list-style: none; display: grid; gap: 18px; font-size: 22px; line-height: 1.4;">
  <li><span class="mono accent">main.py</span> — der Einstieg, ruft die Bausteine auf.</li>
  <li><span class="mono accent">netutils.py</span> — ein <strong>Modul</strong>: thematisch zusammengehörige Funktionen.</li>
  <li><span class="mono accent">data/</span> — Eingabedaten getrennt vom Code.</li>
  <li><span class="mono accent">requirements.txt</span> — welche Bibliotheken das Projekt braucht.</li>
</ul>

<div class="mantra" style="margin-top: 24px;">
  <div class="label">Modul = Werkzeugkasten</div>
  <div class="text">Was woanders gebraucht wird, kommt in eine eigene Datei. <span class="mono">import</span> holt es herein.</div>
</div>
</div>

</div>

<!--
Das entspricht dem echten Ordner 04_module/. Erkläre das Diagramm: main.py ist der Dirigent —
es importiert Funktionen aus netutils.py (from netutils import is_private, subnet_prefix) und
ruft sie auf. netutils.py ist ein Modul: ein Bündel zusammengehöriger Funktionen rund um
IP-Adressen, das man auch in anderen Skripten wiederverwenden könnte. Daten (ips.txt) liegen
getrennt vom Code im data/-Ordner — Code und Daten nicht vermischen. requirements.txt listet die
externen Bibliotheken; aus ihr installiert pip in die .venv. Die Leitfrage „was gehört in ein
eigenes Modul?": alles, was eine abgrenzbare Aufgabe hat und potenziell wiederverwendbar ist.
Faustregel wie bei Funktionen, nur eine Ebene höher.
-->
