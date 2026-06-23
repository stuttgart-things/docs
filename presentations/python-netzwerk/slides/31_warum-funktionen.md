---
layout: default
num: '11 · Warum Funktionen?'
meta: 'Block 3 · DRY · Single Responsibility · Lesbarkeit'
---

<div class="page-label">Block 3 · Warum Funktionen?</div>

# Was gehört in eine <span class="accent">eigene Funktion</span><span class="dot">?</span>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px; margin-top: 40px;">

  <div class="surface" style="padding: 30px 34px;">
    <div class="mono accent" style="font-size: 15px; letter-spacing: 0.14em;">DRY</div>
    <div style="font-size: 26px; font-weight: 600; margin-top: 10px;">Don't Repeat Yourself</div>
    <p style="font-size: 19px; line-height: 1.45; margin-top: 12px;">
      Logik nur an <strong>einer</strong> Stelle. Änderung → einmal ändern, überall wirksam.
    </p>
  </div>

  <div class="surface" style="padding: 30px 34px;">
    <div class="mono accent" style="font-size: 15px; letter-spacing: 0.14em;">SRP</div>
    <div style="font-size: 26px; font-weight: 600; margin-top: 10px;">Eine Aufgabe</div>
    <p style="font-size: 19px; line-height: 1.45; margin-top: 12px;">
      Eine Funktion tut <strong>genau eine</strong> Sache — und die gut. Name sagt, was sie tut.
    </p>
  </div>

  <div class="surface" style="padding: 30px 34px;">
    <div class="mono accent" style="font-size: 15px; letter-spacing: 0.14em;">LESBAR</div>
    <div style="font-size: 26px; font-weight: 600; margin-top: 10px;">Lesbarkeit</div>
    <p style="font-size: 19px; line-height: 1.45; margin-top: 12px;">
      <span class="mono">klassifiziere(ip)</span> liest sich wie ein Satz — der Code erklärt sich selbst.
    </p>
  </div>

</div>

<div class="mantra" style="margin-top: 34px;">
  <div class="label">Faustregel</div>
  <div class="text">Wenn du Code kopierst und nur <strong>einen Wert</strong> änderst → das gehört in eine Funktion (der Wert wird ein Parameter).</div>
</div>

<!--
Bevor wir Code zeigen, die Prinzipien — aber knapp und in Alltagssprache. DRY: Stell dir vor,
die Regel „was ist eine private IP" ändert sich. Steht sie an drei Stellen, musst du dreimal
ändern und vergisst garantiert eine. In einer Funktion änderst du sie einmal. Single
Responsibility: eine Funktion = eine klar benennbare Aufgabe; wenn du „und" im Namen brauchst,
sind es wahrscheinlich zwei Funktionen. Lesbarkeit: gute Funktionsnamen machen den Hauptcode
lesbar wie Prosa. Die Faustregel ganz unten ist das, was hängen bleiben soll — sie ist die
Brücke zur nächsten Slide, wo wir genau so einen Copy-Paste-Block in eine Funktion verwandeln.
-->
