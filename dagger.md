# stuttgart-things/docs/dagger

## SNIPPETS

<details><summary><b>CALL MODULE FROM GIT</b></summary>

```bash
# OUTPUT TEXT
dagger call -m github.com/shykes/daggerverse/hello@v0.1.2 hello --giant=false --name=pat

# SCAN IMAGE REF W/ AQUA TRIVY
dagger call -m github.com/jpadams/daggerverse/trivy@v0.3.0 scan-image --image-ref alpine/git:latest
```

</details>
