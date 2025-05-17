# stuttgart-things/docs/dagger

## SNIPPETS

<details><summary><b>LIST DIRECTORY CONTENTS</b></summary>

```go
// LIST ALL ENTRIES
entries, err := src.Entries(ctx)
if err != nil {
	panic(err)
}

// PRINT ALL ENTRIES
for _, entry := range entries {
	println(entry)
}
```

</details>

<details><summary><b>PERSIST CONTAINER STATE OVER MULTIPLE CI-STEPS</b></summary>

```go
// MOUNT BUILDDIR AND SET WORKING DIRECTORY
base := m.container(packerVersion, arch).
    WithMountedDirectory("/src", buildDir).
    WithWorkdir("/src")

// RUN PACKER INIT AND PERSIST CONTAINER STATE
initContainer := base.WithExec([]string{"packer", "init", "hello.pkr.hcl"})

// OPTIONALLY GET INIT OUTPUT (FROM A SEPARATE EXECUTION)
initOut, err := initContainer.WithExec([]string{"packer", "version"}).Stdout(ctx)
if err != nil {
    panic(fmt.Errorf("failed to verify init: %w", err))
}
fmt.Println("Init complete - Packer version:", initOut)
```

</details>

<details><summary><b>BROWSE DAGGER DIRECTORY</b></summary>

```go
// CLONE
repoContent, err := m.ClonePrivateRepo(ctx, repoURL, branch, token)
if err != nil {
	fmt.Errorf("failed to clone repo: %w", err)
}

// BROWSE
entries, err := repoContent.Entries(ctx)
if err != nil {
    panic(err)
}
fmt.Println("Top-level entries:", entries)
```

</details>


<details><summary><b>TROUBLESHOOTING</b></summary>

```bash
# ERROR
rpc error: code = NotFound desc = socket /run/user/1112/vscode-ssh-auth-sock-713734249 not found
# SOLUTION
unset SSH_AUTH_SOCK
```

</details>

<details><summary><b>DEPLOY CUSTOM ENGINE</b></summary>

[custom-ca](https://docs.dagger.io/configuration/custom-ca)
[connection-interface](https://docs.dagger.io/configuration/custom-runner/#connection-interface)

```bash
## STOP ANY EXISTING/RUNNING ENGINE(S) w/ DOCKER STOP.. 

docker run -d --rm \
-v /var/lib/dagger \
-v /usr/local/share/ca-certificates/:/usr/local/share/ca-certificates/ \
--name dagger-engine-custom \
--privileged \
registry.dagger.io/engine:v0.16.2

export _EXPERIMENTAL_DAGGER_RUNNER_HOST=docker-container://$(docker ps -qf "name=dagger-engine-custom")
```

</details>

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
