# Python für das Netzwerkteam — Workshop Deck

Slidev-Präsentation für den eintägigen Python-Einsteiger-Workshop des Netzwerkteams
(fünf Übungen, drei Wege zu arbeiten). Inhalte und Speaker-Notes auf Deutsch; die
Code-Beispiele stammen 1:1 aus den echten Übungsdateien unter [`workshop/`](./workshop).

Gerendert über das [`stuttgart-things/dagger/slidev`](https://github.com/stuttgart-things/dagger/tree/main/slidev)
Modul — wie das `platform-engineering-harvester`-Deck. Nur die geschriebenen Inhalte liegen im
Git; `package.json`, `node_modules/`, `pnpm-lock.yaml` und `dist/` werden bei Bedarf im Container
erzeugt.

## Aufbau

```
.
├── slides.md        # Entry-Deck — Frontmatter + `src:`-Includes
├── slides/          # Kapitel-Partials (00_agenda.md, 01_modi.md, …)
├── layouts/         # eigene Vue-Layouts (cover, default, section, exercise)
├── setup/main.ts    # Slidev App-Setup-Hook (lädt style.css)
├── style.css        # globaler Hausstil (heller stuttgart-things-Look, Violett-Akzent)
├── workshop/        # die fünf echten Übungen + SPICKZETTEL.md (Quelle der Code-Slides)
└── theme.json       # lokale Theme-Metadaten (Fonts, Aspect Ratio)
```

## Voraussetzungen

- [Dagger CLI](https://docs.dagger.io/install) (≥ v0.20)
- Docker-Runtime

## Live-Dev-Server

Serviert das Deck auf <http://localhost:3030> mit Hot-Reload:

```bash
dagger call -m github.com/stuttgart-things/dagger/slidev serve \
  --slides ./slides.md \
  --style  ./style.css \
  --extras . \
  --addons @slidev/types \
  --port 3030 \
  up --progress plain
```

## Statischer Build

```bash
dagger call -m github.com/stuttgart-things/dagger/slidev build \
  --slides ./slides.md \
  --style  ./style.css \
  --extras . \
  --addons @slidev/types \
  export --path /tmp/python-netzwerk/dist
```

## Handout-PDF (ohne Notes)

```bash
dagger call -m github.com/stuttgart-things/dagger/slidev export \
  --slides ./slides.md \
  --style  ./style.css \
  --extras . \
  --addons @slidev/types \
  export --path /tmp/python-netzwerk/out
# → /tmp/python-netzwerk/out/slides-export.pdf
```

## Vor dem Workshop ausfüllen (Platzhalter)

Im Deck sind firmeninterne Werte bewusst als Platzhalter markiert:

| Platzhalter | Wo | Bedeutung |
|-------------|----|-----------|
| `<DATUM>`, `<TRAINER>` | `slides.md` (Cover-Notes) | Termin & Trainer:in |
| `<name>.<domain>`, `<PASSWORT>` | `slides/02_login.md` | code-server-URL & Passwort |
| `<KANAL>` | `slides/61_weiter.md` | interner Team-Chat-Kanal |
| `<proxy>:<port>` | `slides/90_anhang-troubleshooting.md` | Firmen-Proxy (Übung 5 / pip) |
