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

Setzen Sie ihren username und email in der git cli

```bash
git config --global user.name "Dr. Henry Jekyll"
git config --global user.email jekyll@example.com
```

* Erstellen Sie einen user, projekt und repository für sie in gitea
* Hinterlegen sie einen pub key in gitea
* Testen sie git clone via ssh
* Testen sie git init via git cli und das Anlegen einens Repos über die GUI

## /AUFGABE 2: GIT COMMIT + TAG + PUSH

1. Legen Sie im Kommandozeileninterpreter ein neues Verzeichnis mit der
Bezeichnung aufgaben an. Wechseln Sie in dieses Verzeichnis und
erstellen Sie dort ein neues Git-Repository. Geben Sie die drei Befehle an,
die Sie hierfür benötigen.
1. Erstellen Sie drei Dateien mit den Bezeichnungen aufgabe.py,
aufgabe.java und beispiel.c. Fügen Sie mit einem einzigen Kommando
alle Dateien zum Repository hinzu, die mit dem Ausdruck aufgabe
beginnen. Lassen Sie sich den Status des Repositorys nach dem Erstellen
der Dateien und nach dem Hinzufügen ausgeben.
1. Erstellen Sie ein Commit für die beiden Dateien. Fügen Sie die CommitNachricht direkt über die Kommandozeile ein. Geben Sie anschließend
den Verlauf der Commits aus.
1. Erstellen Sie ein annotated Tag für den in Aufgabe 3 durchgeführten
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
1. Gehen Sie nun davon aus, dass in der Zwischenzeit ein anderes Team- Mitglied eine neue Datei in den master-Zweig eingefügt hat. Da sich jedoch wahrscheinlich kein Mitarbeiter in der Nähe befindet, der diese Aufgabe erledigen kann, müssen Sie die Datei für dieses Beispiel ebenfalls selbst einfügen. Um mit Ihren eigenen Tätigkeiten fortzufahren, benötigen Sie diese Datei. Übernehmen Sie die Änderungen aus dem Hauptzweig mit dem rebase-Befehl.
1. Erstellen Sie daraufhin einen weiteren Beitrag in Ihrem Zweig. Tragen Sie daraufhin Ihren Beitrag in den Hauptzweig ein. Nutzen Sie hierfür den merge-Befehl. Da Sie damit Ihre Arbeit abgeschlossen haben, benötigen Sie den entsprechenden Zweig nicht mehr. Löschen Sie ihn, um die Ordnung im Repository aufrechtzuerhalten.

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

--
## Pull Requests

1. Each new feature starts on its own branch (the so-called **feature branch**).
1. When the feature is ready, a pull request is submitted to merge the feature branch into the `master` branch.
1. A code review happens
1. If something need to be changed based on the review, those
1. Once everything looks good, the feature branch is merged into `master`.

## Practicing Pull Requests

We're going to create a pull request that contains two individual commits involving different files.

### Fork And Clone This Repository

* Create a repo with the name exercises-git-pull-request-<YOURNAME> on gitea and create/add/commit a file into the master branch.

Next, clone **your repo** using the `git clone` command. This will create a copy of your repository on your computer (called a *local copy*).

```console
git clone gitea@<IP>:<PROJECT>/<REPO>.git
```

This will create a directory named `exercises-git-pull-request` inside the current working directory. Enter the directory with the following command:

```console
cd exercises-git-pull-request
```

### Create A Feature Branch

When we're inside a git repository, there is always an "active" branch. To see a list of all the branches run:

```console
git branch
```

The active branch is whichever one is prefixed with `*`. Because `master` is the only branch, you should see:

```console
$ git branch
* master
$
```

Let's create a new branch and switch to it. Run the following:

```console
git checkout -b first-feature
```

Run `git branch` again and you should see:

```console
$ git branch
* first-feature
  master
$
```

### Create `hello.txt`

**Note**: Remember to use commands like `ls` and `pwd` to verify you're in the correct directory and looking at the right files.

While on the `first-feature` branch, create a file named `hello.txt` that contains the following text:

```text
Hello! This is my first pull request.
```

Make sure to save the file. In the console, run the following command:

```console
git status
```

This gives you information about the current state of your git repository. It will show you which files have been modified, which files are new and have yet to be committed, etc.

Run the following `git add` command:

```console
git add hello.txt
```

Run `git status` again to see how the output changed.

### Commit `hello.txt`

Run the following command to create a new commit:

```console
git commit -m 'hello.txt is a lovely file'
```

Run `git status` and note how the output has changed.

### Create And Commit `goodbye.txt`

Let's create a second commit.

Create a file named `goodbye.txt` that contains the following text:

```text
Goodbye! About to submit my first pull request.
```

Again, run `git status` to see how the output has changed. Add and commit `goodbye.txt`.

To add it:

```console
git add goodbye.txt
```

Run `git status` and note how the output changed.

To commit it:

```console
git commit -m 'Time to say goodbye'
```

Run `git status` and note how the output changed.

### Push Your Local Changes Up To Gitea

Right now, your branch exists on your machine but doesn't yet exist on Gitea. To simultaneously push your changes up to Gitea and create the branch on Gitea, run the following command:

```console
git push --set-upstream origin first-feature
```

Here `origin` refers to Gitea.

Now visit your repository on Gitea!

### Create A Pull Request

On Gitea

Click the **Compare & Pull Request**. On the next page, click **Create Pull Request**.

Ta-da, first pull request!

## Requesting Code Review

You have two ways to request a code review:

1. Add one or more instructors as collaborators on your project and then select them from the "Request Review" dropdown
2. Leave a comment `@`-mentioning anyone you want a code review from.

   ```text
   @Colleague I'd like a review!
   ```

## Merging Pull Request

Once you're ready to go, merge your pull request into the `master` branch. Don't wait for a review to merge unless you think it's critical.
