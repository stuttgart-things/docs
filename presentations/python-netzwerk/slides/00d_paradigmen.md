---
layout: default
num: 'Paradigmen'
meta: 'Prozedural · objektorientiert · funktional · async'
---

<div class="page-label">Mehr als nur Skripte</div>

# Python lässt dir <span class="accent">die Wahl</span><span class="dot">.</span>

<p class="lede">
Python ist <strong>multi-paradigmatisch</strong>: Du kannst simpel Schritt für Schritt skripten —
oder mit Klassen, funktionalem Stil und Nebenläufigkeit arbeiten. Alles in derselben Sprache.
</p>

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 22px; margin-top: 28px;">

  <div class="surface" v-click style="padding: 24px 28px;">
    <div class="mono accent" style="font-size: 15px; letter-spacing: 0.14em;">PROZEDURAL</div>
    <div style="font-size: 21px; font-weight: 600; margin-top: 8px;">Schritt für Schritt</div>
    <div class="muted" style="font-size: 17px; margin-top: 6px;">Das machen wir heute — einfache, lesbare Skripte.</div>
    <div class="mono" style="font-size: 16px; margin-top: 10px;">for host in hosts: ping(host)</div>
  </div>

  <div class="surface" v-click style="padding: 24px 28px;">
    <div class="mono accent" style="font-size: 15px; letter-spacing: 0.14em;">OBJEKTORIENTIERT</div>
    <div style="font-size: 21px; font-weight: 600; margin-top: 8px;">Ja — voll OOP</div>
    <div class="muted" style="font-size: 17px; margin-top: 6px;"><em>Alles</em> ist ein Objekt: Klassen, Vererbung, Methoden.</div>
    <div class="mono" style="font-size: 16px; margin-top: 10px;">class Router: ...&nbsp;&nbsp;r.reboot()</div>
  </div>

  <div class="surface" v-click style="padding: 24px 28px;">
    <div class="mono accent" style="font-size: 15px; letter-spacing: 0.14em;">FUNKTIONAL</div>
    <div style="font-size: 21px; font-weight: 600; margin-top: 8px;">Kompakt & elegant</div>
    <div class="muted" style="font-size: 17px; margin-top: 6px;">Comprehensions, <span class="mono">map</span>, <span class="mono">filter</span>, <span class="mono">lambda</span>.</div>
    <div class="mono" style="font-size: 16px; margin-top: 10px;">[ip for ip in netz if aktiv(ip)]</div>
  </div>

  <div class="surface" v-click style="padding: 24px 28px;">
    <div class="mono accent" style="font-size: 15px; letter-spacing: 0.14em;">ASYNC</div>
    <div style="font-size: 21px; font-weight: 600; margin-top: 8px;">Vieles gleichzeitig</div>
    <div class="muted" style="font-size: 17px; margin-top: 6px;"><span class="mono">async/await</span> seit 3.5 — 100 Hosts parallel abfragen.</div>
    <div class="mono" style="font-size: 16px; margin-top: 10px;">await check(host)</div>
  </div>

</div>

<div class="mantra" style="margin-top: 26px;">
  <div class="label">Für heute</div>
  <div class="text">Wir bleiben bewusst beim <strong>prozeduralen</strong> Stil — der reicht für 90 % des Netzwerk-Alltags. Die anderen drei sind da, wenn ihr sie irgendwann braucht.</div>
</div>

<!--
Diese Folie nimmt eine häufige Einsteiger-Frage vorweg: „Ist Python objektorientiert oder nicht?"
Antwort: beides — und mehr. Python zwingt kein Paradigma auf. Intern ist alles ein Objekt (auch
ints und Funktionen), volle OOP mit Klassen und Vererbung ist vorhanden. Gleichzeitig kann man
rein prozedural skripten (so machen wir es heute) oder funktional arbeiten (Comprehensions sind
sehr „pythonic"). Async/await (seit Python 3.5) ist der Joker für Netzwerk-Aufgaben: viele
langsame I/O-Operationen — z. B. 100 Geräte abfragen — laufen nebenläufig statt nacheinander.
Wichtig zu betonen: Für den Workshop brauchen sie davon NICHTS außer dem prozeduralen Stil.
Das hier ist ein „gut zu wissen, wie weit man kommen kann"-Ausblick, kein Lernstoff für heute.
-->
