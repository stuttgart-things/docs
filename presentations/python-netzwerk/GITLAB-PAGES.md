# Idee: Deck über GitLab Pages ausliefern

Notiz für später — das Slidev-Deck als statische Website auf GitLab Pages hosten,
damit Teilnehmer:innen die Slides einfach per Link im Browser ansehen können
(ohne code-server, ohne lokalen `dagger`/`slidev serve`).

## Warum das funktioniert

`slidev build` erzeugt eine **rein statische Site** (HTML/JS/CSS) — genau das, was
GitLab Pages ausliefert. Kein Server, kein Browser/Playwright nötig (das braucht nur
der PDF-Export). Der Pages-Build ist damit leicht und schnell.

## Bausteine

- **`.gitlab-ci.yml`** (liegt im Deck-Ordner) — Job `pages`, der Slidev installiert,
  nach `public/` baut und von GitLab automatisch deployt wird.
- **Output-Ordner `public/`** — GitLab Pages liefert ausschließlich diesen Ordner aus.
- **`--base`-Pfad** — muss zur Pages-URL passen.

## Ablauf (Kurzform)

1. Deck-Inhalt in ein GitLab-Repo laden (am einfachsten: dieser Ordner als eigenes
   Repo, Deck im Root → `.gitlab-ci.yml` liegt direkt richtig).
2. Push auf den Default-Branch → Pipeline baut + deployt.
3. Ergebnis unter `https://<namespace>.gitlab.io/<projekt>/`
   (die genaue URL steht im Pipeline-Log).

## Die zwei Stolpersteine

| Thema | Problem | Lösung (in der CI gesetzt) |
|-------|---------|----------------------------|
| **Base-Pfad** | Projekt-Pages liegen unter `/<projekt>/`; ohne passenden `--base` laden Assets nicht (404, weiße Seite). | `--base "/$CI_PROJECT_NAME/"` · Root-Pages-Repo (`<namespace>.gitlab.io`) → `--base "/"` |
| **Keine Deps im Repo** | Es gibt bewusst kein `package.json`/`node_modules` (wird sonst im Container erzeugt). | CI installiert frisch: `@slidev/cli`, `@slidev/theme-default`, `@slidev/types`. `setup/main.ts` + `layouts/` + `style.css` ziehen automatisch mit. |

## Deck in einem Unterordner?

Falls das Deck **nicht** im Repo-Root liegt: in der `.gitlab-ci.yml` vor dem Build
`cd <pfad>` und mit `--out ../../public` ins Repo-Root schreiben (auskommentierte
Variante ist in der Datei enthalten). `artifacts.paths` bleibt `public`.

## Alternative: GitHub Pages

Dasselbe Prinzip läuft auf **GitHub Pages** mit einem GitHub-Actions-Workflow
(`actions/deploy-pages`) — gleicher `slidev build`, gleicher `--base`-Trick
(dort `/<repo>/`). Das gehen wir separat an.

## Offene To-dos

- [ ] Ziel klären: eigenes GitLab-Repo vs. Unterordner vs. GitHub Pages.
- [ ] Platzhalter im Deck prüfen (URL/Passwort/Proxy) — nichts Internes öffentlich stellen.
- [ ] Sichtbarkeit/Zugriff der Pages-Site festlegen (öffentlich vs. intern).
- [ ] Optional: PDF-Handout als zusätzliches CI-Artefakt.
