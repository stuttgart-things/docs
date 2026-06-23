---
layout: default
num: '23 · Spickzettel'
meta: 'Kernsyntax kompakt · zum Mitnehmen'
---

<div class="page-label">23 · Spickzettel</div>

# Alles Wichtige auf <span class="accent">einen Blick</span><span class="dot">.</span>

<div class="cheat">

<div class="cheat-card">
<div class="cheat-h">Variablen & Typen</div>

```python
name   = "router-01"   # str
ports  = 48            # int
load   = 0.73          # float
online = True          # bool
hosts  = ["a", "b"]    # list
ip_of  = {"a": "10.0.0.1"}  # dict
```
</div>

<div class="cheat-card">
<div class="cheat-h">Bedingungen & Schleifen</div>

```python
if load > 0.9:
    print("kritisch")
elif load > 0.7:
    print("hoch")

for host in hosts:
    print(host)
for k, v in ip_of.items():
    print(k, v)
```
</div>

<div class="cheat-card">
<div class="cheat-h">Funktionen</div>

```python
def is_private(ip: str) -> bool:
    return ip.startswith(
        ("10.", "192.168."))
```
</div>

<div class="cheat-card">
<div class="cheat-h">Bibliothek / API</div>

```python
import requests
r = requests.get(url, timeout=10)
r.raise_for_status()
data = r.json()   # -> dict
```
</div>

<div class="cheat-card">
<div class="cheat-h">venv</div>

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
</div>

<div class="cheat-card">
<div class="cheat-h">Debugging</div>

```text
Traceback von UNTEN lesen.
Letzte Zeile = Fehlertyp.
print(typ, wert)
import pdb; pdb.set_trace()
```
</div>

</div>

<style scoped>
.cheat { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; margin-top: 22px; }
.cheat-card { background: var(--surface); border: 1px solid var(--rule); border-radius: 12px; padding: 16px 20px; }
.cheat-h { font-family: var(--font-mono); font-size: 14px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent); margin-bottom: 8px; }
.cheat .slidev-code { font-size: 15px !important; padding: 14px 16px !important; line-height: 1.45 !important; }
</style>

<!--
Das ist die Foto-Slide zum Mitnehmen — sag den Leuten ausdrücklich: jetzt abfotografieren. Es ist
der komplette Spickzettel aus SPICKZETTEL.md auf einer Seite. Geh nicht jede Box durch, das wäre
Wiederholung; verweise nur darauf, dass hier alles vom heutigen Tag kompakt steht und auch im
Repo unter workshop/SPICKZETTEL.md liegt. Kurzer Moment Pause zum Fotografieren.
-->
