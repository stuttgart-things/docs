---
layout: default
num: '08 · Bedingungen & Schleifen'
meta: 'Block 2 · 02_filter.py'
---

<div class="page-label">Block 2 · Bedingungen & Schleifen</div>

# IPs <span class="accent">durchgehen</span> und <span class="accent">filtern</span><span class="dot">.</span>

<div style="display: grid; grid-template-columns: 0.8fr 1.2fr; gap: 40px; margin-top: 24px; align-items: start;">

<div>
<ul style="margin: 0; padding: 0; list-style: none; display: grid; gap: 16px; font-size: 22px; line-height: 1.4;">
  <li><span class="mono accent">for ip in liste:</span><br/><span class="muted">jedes Element nacheinander</span></li>
  <li><span class="mono accent">if bedingung:</span><br/><span class="muted">nur wenn sie zutrifft</span></li>
  <li><span class="mono accent">.startswith("10.")</span><br/><span class="muted">beginnt der Text mit …?</span></li>
  <li><span class="muted">Einrückung</span> = Zugehörigkeit<br/><span class="muted">(4 Leerzeichen, kein Tab-Mix)</span></li>
</ul>

<div class="mantra" style="margin-top: 24px;">
  <div class="label">Über Dicts iterieren</div>
  <div class="text"><span class="mono">for k, v in d.items():</span></div>
</div>
</div>

```python {1-4|6|7|8|9|all}
ip_addresses = [
    "10.0.1.11", "10.0.1.12", "192.168.5.4", "10.0.2.7",
    "172.16.0.9", "192.168.5.99", "10.0.1.250", "8.8.8.8",
]

print("Adressen im Netz 10.0.1.x:")
for ip in ip_addresses:
    if ip.startswith("10.0.1."):
        print(f"  {ip}")
```

</div>

<!--
Code aus 02_filter.py. Schritt für Schritt: zuerst die Liste der IP-Adressen (unsere Testdaten).
Dann die for-Schleife — betont, dass 'ip' ein frei gewählter Name ist, der bei jedem Durchlauf
die nächste Adresse enthält. Das if mit startswith filtert: nur Adressen aus 10.0.1.x werden
ausgegeben. Ganz wichtig für Einsteiger: die EINRÜCKUNG bestimmt, was zur Schleife und was zum if
gehört — Python ist da streng. Vier Leerzeichen sind Standard, niemals Tabs und Leerzeichen
mischen. Zweite Botschaft: Man kann nicht nur über Listen iterieren, sondern auch über Dicts
mit .items() (Schlüssel und Wert gleichzeitig) — das brauchen sie für den Bonus der Übung.
-->
