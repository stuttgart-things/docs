---
layout: default
num: '12 · Vorher / Nachher'
meta: 'Block 3 · 03_refactor.py · Refactoring'
---

<div class="page-label">Block 3 · Vorher / Nachher</div>

# Drei Copy-Paste-Blöcke → <span class="accent">eine Funktion</span><span class="dot">.</span>

<div class="vn">

  <div class="vn-col">
    <div class="vn-tag vorher">Vorher · dreimal fast dasselbe</div>

```python
ip1 = "10.0.1.5"
if ip1.startswith("10.") or ip1.startswith("192.168.") or ip1.startswith("172.16."):
    print(f"{ip1} ist privat")
else:
    print(f"{ip1} ist öffentlich")

ip2 = "8.8.8.8"
if ip2.startswith("10.") or ip2.startswith("192.168.") or ip2.startswith("172.16."):
    print(f"{ip2} ist privat")
else:
    print(f"{ip2} ist öffentlich")

# … und das Ganze nochmal für ip3
```

  </div>

  <div class="vn-col" v-click>
    <div class="vn-tag nachher">Nachher · einmal definieren, oft nutzen</div>

```python
def klassifiziere(ip: str) -> str:
    """Privat oder öffentlich? Gibt einen Text zurück."""
    privat = ("10.", "192.168.", "172.16.")
    if ip.startswith(privat):
        return f"{ip} ist privat"
    return f"{ip} ist öffentlich"

for ip in ["10.0.1.5", "8.8.8.8", "192.168.0.10"]:
    print(klassifiziere(ip))
```

  </div>

</div>

<style scoped>
.vn { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 24px; align-items: start; }
.vn-tag { font-family: var(--font-mono); font-size: 15px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 12px; }
.vn-tag.vorher { color: #C0392B; }
.vn-tag.nachher { color: var(--accent); }
.vn .slidev-code { font-size: 18px !important; padding: 22px !important; }
</style>

<!--
Das ist der Kern des Tages — nimm dir Zeit dafür. Links der Code aus 03_refactor.py wie er ist:
dreimal derselbe if/else-Block, nur die IP ändert sich. Frag die Gruppe: „Was stört euch hier?"
— die Antwort (Wiederholung!) sollen sie selbst geben. Dann per Klick die rechte Seite aufdecken:
EINE Funktion klassifiziere(ip). Erkläre die Bestandteile: def + Name + Parameter (ip), der
Doppelpunkt und die Einrückung markieren den Funktionskörper, der Docstring beschreibt sie,
return gibt einen Wert zurück. Nebenbei zwei Profi-Kniffe: startswith akzeptiert ein Tupel von
Präfixen (privat = (...)), und das frühe return spart das else. Unten die Schleife zeigt den
Lohn: drei IPs, eine Zeile. Genau das bauen sie jetzt selbst in Übung 3.
-->
