"""Zusatzübung 1b – Strings & Formatierung mit Netzwerkdaten.

Hostnamen zerlegen, Werte sauber formatieren, Texte zusammenbauen.
Ausführen:  python 01b_strings.py
"""

# Ein Hostname nach Schema <rolle>-<standort>-<nummer>
hostname = "sw-stuttgart-07"

teile = hostname.split("-")
print(f"Rolle    : {teile[0]}")
print(f"Standort : {teile[1]}")
print(f"Nummer   : {teile[2]}")

# Eine MAC-Adresse einheitlich formatieren
mac = "a0:b1:c2:d3:e4:f5"
print(f"MAC gross: {mac.upper()}")

# ----------------------------------------------------------------------------
# AUFGABE:
#   1) Baue aus 'teile' einen FQDN zusammen, z. B. "sw07.stuttgart.example.com"
#      (Tipp: f-string, Teile neu zusammensetzen).
#   2) Formatiere eine CPU-Last 0.4267 als Prozent mit einer Nachkommastelle –
#      erwartete Ausgabe "42.7 %".  (Tipp: f"{wert * 100:.1f} %")
#
# ★ PROFI-BONUS:
#   Schreibe die MAC-Adresse ins Cisco-Format aaaa.bbbb.cccc um:
#   Doppelpunkte entfernen -> in 4er-Gruppen aufteilen -> mit Punkten verbinden.
# ----------------------------------------------------------------------------
