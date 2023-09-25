# /GIT Aufgaben

## /AURGABE 1: GIT CONFIG
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

+ GITTEA


## /AUFGABE 2: GIT COMMIT + TAG + PUSH

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

## /AUFGABE 3: BRANCHING

Verwenden Sie wieder das Repository, das Sie für die Übungsaufgaben in Kapitel 3 angelegt haben. Gehen Sie nun davon aus, dass im master-Zweig mehrere Team-Mitglieder gemeinsam an der Entwicklung einer Software arbeiten.

1. Erstellen Sie zunächst einen Zweig für Ihre eigenen Beiträge und nennen Sie ihn meinZweig. Ändern Sie darin eine Datei und erstellen Sie darin einen Commit.
2. Gehen Sie nun davon aus, dass in der Zwischenzeit ein anderes Team- Mitglied eine neue Datei in den master-Zweig eingefügt hat. Da sich jedoch wahrscheinlich kein Mitarbeiter in der Nähe befindet, der diese Aufgabe erledigen kann, müssen Sie die Datei für dieses Beispiel ebenfalls selbst einfügen. Um mit Ihren eigenen Tätigkeiten fortzufahren, benötigen Sie diese Datei. Übernehmen Sie die Änderungen aus dem Hauptzweig mit dem rebase-Befehl.
3. Erstellen Sie daraufhin einen weiteren Beitrag in Ihrem Zweig. Tragen Sie daraufhin Ihren Beitrag in den Hauptzweig ein. Nutzen Sie hierfür den merge-Befehl. Da Sie damit Ihre Arbeit abgeschlossen haben, benötigen Sie den entsprechenden Zweig nicht mehr. Löschen Sie ihn, um die Ordnung im Repository aufrechtzuerhalten.

```bash
# 1
git branch meinZweig
git checkout meinZweig
{Änderung an der Datei}
git commit -a -m "Commit für Aufgabe 4.1"

# 2
git checkout master
{Hinzufügen einer neuen Datei}
git add neueDatei.py
git commit -a -m "Commit für Aufgabe 4.2" git checkout meinZweig

git rebase master

# 3
{Änderung an der Datei}
git commit -a -m "Commit für Aufgabe 4.3" git checkout master
git merge meinZweig
git branch -d meinZweig
```