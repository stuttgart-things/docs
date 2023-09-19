# /GIT EXERCISES

## /GIT CONFIG
Git bietet neben den vorgestellten Konfigurationsmöglichkeiten noch
viele weitere Optionen. Suchen Sie selbstständig nach einer Möglichkeit,
um mit dem config-Befehl die Autokorrektur zu aktivieren. Diese führt
dazu, dass auch bei einem Tippfehler der korrekte Befehl ausgeführt wird.


```bash
git config --global help.autocorrect 1
```

Die Hilfe erreichen Sie über einen der folgenden Befehle: git help init, git
init --help, man git-init (nicht unter Windows) oder git init -h (in
verkürzter Form).

## /GIT COMMIT + TAG + PUSH


1. Legen Sie im Kommandozeileninterpreter ein neues Verzeichnis mit der
Bezeichnung aufgaben an. Wechseln Sie in dieses Verzeichnis und
erstellen Sie dort ein neues Git-Repository. Geben Sie die drei Befehle an,
die Sie hierfür benötigen.
2. Erstellen Sie drei Dateien mit den Bezeichnungen aufgabe.py,
aufgabe.java und beispiel.c. Fügen Sie mit einem einzigen Kommando
alle Dateien zum Repository hinzu, die mit dem Ausdruck aufgabe
beginnen. Lassen Sie sich den Status des Repositorys nach dem Erstellen
der Dateien und nach dem Hinzufügen ausgeben.
3. Erstellen Sie ein Commit für die beiden Dateien. Fügen Sie die CommitNachricht direkt über die Kommandozeile ein. Geben Sie anschließend
den Verlauf der Commits aus.
4. Erstellen Sie ein annotated Tag für den in Aufgabe 3 durchgeführten
Commit. Rufen Sie anschließend die Informationen zu diesem Tag ab.

```bash
# 1
mkdir aufgaben
cd aufgaben
git init

# 2
git status
git add aufgabe*
git status

# 3
git commit -m "aufgabe.java und aufgabe.py hinzugefügt"
git log

# 4
git tag -a version0.1 -m "Version 0.1 der Software"
git show version0.1
```