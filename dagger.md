# stuttgart-things/docs/dagger

## SNIPPETS

<details><summary><b>CALL FUNCTION FROM GIT</b></summary>

```bash
# OUTPUT TEXT
dagger call -m github.com/shykes/daggerverse/hello@v0.1.2 hello --giant=false --name=pat

# SCAN IMAGE REF W/ AQUA TRIVY
dagger call -m github.com/jpadams/daggerverse/trivy@v0.3.0 scan-image --image-ref alpine/git:latest

# BUILD GO BINARY
dagger call -m github.com/felipecruz91/daggerverse/go build --source . --goVersion 1.23.1 -o bin
```

</details>
