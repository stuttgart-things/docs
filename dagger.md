# stuttgart-things/docs/dagger

## SNIPPETS

<details><summary><b>CALL HELP FUNCTION (OF SUBCOMMAND)</b></summary>

```bash
dagger call -m "github.com/sagikazarmark/daggerverse/gh@main" release create --help
```

</details>

<details><summary><b>INIT MODULE</b></summary>

```bash
dagger init --sdk=go --source=./cicd --name cicd
```

</details>

<details><summary><b>CALL LOCAL MODULE</b></summary>

```bash
dagger call -m cicd/ go-pipeline --src ./
```

</details>

<details><summary><b>INSTALL DEPENDECY/b></summary>

```bash
dagger install github.com/stuttgart-things/dagger/go@v0.1.0
```

</details>

<details><summary><b>CALL FUNCTION (FROM DAGGERVERSE)</b></summary>

```bash
# OUTPUT TEXT
dagger call -m github.com/shykes/daggerverse/hello@v0.1.2 hello --giant=false --name=pat

# SCAN IMAGE REF W/ AQUA TRIVY
dagger call -m github.com/jpadams/daggerverse/trivy@v0.3.0 scan-image --image-ref alpine/git:latest

# BUILD GO BINARY
dagger call -m github.com/felipecruz91/daggerverse/go build --source . --goVersion 1.23.1 -o bin

# LINT DOCKERFILE
dagger call -m github.com/disaster37/dagger-library-go/image lint --source . --dockerfile images/sthings-packer/Dockerfile

# BUILD & PUSH CONTAINER IMAGE
dagger call -m github.com/disaster37/dagger-library-go/image build --source . --dockerfile images/sthings-packer/Dockerfile push --repository-name stuttgart-things/test --registry-url ttl.sh --version 60m

# CLONE A GITHUB REPO
export GITHUB_TOKEN=whatever
dagger call --progress plain -m github.com/sagikazarmark/daggerverse/gh@main \
repo clone \
--repository stuttgart-things/stuttgart-things \
--token=env:GITHUB_TOKEN export --path=/tmp/repo/sthings
```

</details>

<details><summary><b>INSTALL DAGGER-CLI</b></summary>

```bash
curl -fsSL https://dl.dagger.io/dagger/install.sh | BIN_DIR=$HOME/.local/bin sh
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
