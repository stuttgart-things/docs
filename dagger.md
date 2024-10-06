# stuttgart-things/docs/dagger

## SNIPPETS

<details><summary><b>CALL FUNCTION (FROM DAGGERVERSE)</b></summary>

```bash
# OUTPUT TEXT
dagger call -m github.com/shykes/daggerverse/hello@v0.1.2 hello --giant=false --name=pat

# SCAN IMAGE REF W/ AQUA TRIVY
dagger call -m github.com/jpadams/daggerverse/trivy@v0.3.0 scan-image --image-ref alpine/git:latest

# BUILD GO BINARY
dagger call -m github.com/felipecruz91/daggerverse/go build --source . --goVersion 1.23.1 -o bin
```

</details>


<details><summary><b>BASIC COMMANDS</b></summary>

https://docs.dagger.io/quickstart/daggerize

```bash
# CREATE MODULE (GO); SOURCE: ./hello; NAME: modules
dagger init --sdk=go --source=./hello --name modules

# RUN PIPELINE (PUBLISH=METHOD NAME)
dagger call publish --source=.
```


</details>
