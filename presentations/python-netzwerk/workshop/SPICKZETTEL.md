# Python-Spickzettel

## Variablen & Datentypen
```python
name = "router-01"      # str  (Text)
ports = 48              # int  (Ganzzahl)
load = 0.73             # float
online = True           # bool
hosts = ["a", "b"]      # list (Reihenfolge, veränderbar)
ip_of = {"a": "10.0.0.1"}  # dict (Schlüssel -> Wert)
```

## Ausgabe / f-strings
```python
print(f"{name} hat {ports} Ports")
```

## Bedingungen
```python
if load > 0.9:
    print("kritisch")
elif load > 0.7:
    print("hoch")
else:
    print("ok")
```

## Schleifen
```python
for host in hosts:
    print(host)

for key, value in ip_of.items():
    print(key, value)
```

## Funktionen
```python
def is_private(ip: str) -> bool:
    return ip.startswith("10.") or ip.startswith("192.168.")
```

## Bibliothek importieren / API
```python
import requests
r = requests.get("https://api.github.com/meta")
data = r.json()           # JSON -> dict
```

## venv (Übung 4)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Debugging
- **Traceback von UNTEN nach OBEN lesen** – die letzte Zeile nennt den Fehler.
- `print(typ, wert)` zum Zwischenstand prüfen.
- `import pdb; pdb.set_trace()` setzt einen Haltepunkt.
