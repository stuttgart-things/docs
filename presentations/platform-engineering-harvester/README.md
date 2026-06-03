# Platform Engineering · Harvester — Workshop Deck

Slidev presentation covering Harvester, Backstage and Platform Engineering.

Rendered through the [`stuttgart-things/dagger/slidev`](https://github.com/stuttgart-things/dagger/tree/main/slidev) module, so only authored content lives in git. `package.json`, `node_modules/`, `pnpm-lock.yaml`, and `dist/` are generated on demand inside a container.

## Layout

```
.
├── slides.md       # entry deck — frontmatter + `src:` includes
├── slides/         # chapter partials (00_intro.md, …)
├── layouts/        # custom Vue layouts (cover, default, section)
├── setup/main.ts   # Slidev app setup hook (loads style.css)
├── style.css       # global style overrides
└── theme.json      # local theme metadata (fonts, aspect ratio)
```

## Prerequisites

- [Dagger CLI](https://docs.dagger.io/install) (≥ v0.20)
- Docker runtime

## Live Dev Server

Serves the deck on <http://localhost:3030> with hot reload:

```bash
dagger call -m github.com/stuttgart-things/dagger/slidev serve \
  --slides ./slides.md \
  --style  ./style.css \
  --extras . \
  --addons @slidev/types \
  --port 3030 \
  up --progress plain
```

## Static Build

```bash
dagger call -m github.com/stuttgart-things/dagger/slidev build \
  --slides ./slides.md \
  --style  ./style.css \
  --extras . \
  --addons @slidev/types \
  export --path /tmp/platform-engineering-harvester/dist
```
