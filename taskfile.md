# stuttgart-things/docs/taskfile

A task runner / simpler Make alternative written in Go

## INSTALLATION

<details><summary><b>INSTALLATION</b></summary>

```bash
go install github.com/go-task/task/v3/cmd/task@latest
```

</details>

## SNIPPETS

<details><summary><b>PROTO (GO GEN)</b></summary>

```bash
cat <<EOF > ./Taskfile.yaml
version: 3
tasks:
  proto:
    desc: Generate Go code from proto file
    cmds:
      - go install google.golang.org/protobuf/cmd/protoc-gen-go@v{{ .PROTOC_GEN_GO_VERSION }}
      - go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v{{ .PROTOC_GEN_GO_GRPC_VERSION }}
      - protoc -I{{ .PROTOC_DIR }} --go_opt=module={{ .GO_MODULE }} --go_out={{ .OUTPUT_DIR }} --go-grpc_opt=require_unimplemented_servers=false,module={{ .GO_MODULE }} --go-grpc_out={{ .OUTPUT_DIR }} {{ .PROTOC_DIR }}/*.proto
    vars:
      PROTOC_GEN_GO_VERSION: 1.28
      PROTOC_GEN_GO_GRPC_VERSION: 1.2
      PROTOC_DIR: fetcher/repository
      GO_MODULE: github.com/stuttgart-things/sweatShop-fetcher/reposerver/apiclient
      OUTPUT_DIR: fetcher/apiclient
```

</details>

<details><summary><b>GIT TASKS</b></summary>

```bash
cat <<EOF > ./Taskfile.yaml
version: 3
vars:
  PROJECT_NAME:
    sh: pwd | grep -o "[^/]*$"
  DATE:
    sh: date +"%y.%m%d.%H%M"
  UPDATED_TAG:
    sh: old_tag=$(git describe --tags --abbrev=0 | cut -d "." -f3 | cut -d "-" -f1); new_tag=$((old_tag+1)); echo $new_tag
  UPDATED_TAG_VERSION:
    sh: t1=$(git describe --tags --abbrev=0 | cut -f1 -d'.'); t2=$(git describe --tags --abbrev=0 | cut -f2 -d'.'); echo $t1.$t2.{{ .UPDATED_TAG }}
  BRANCH:
    sh: if [ $(git rev-parse --abbrev-ref HEAD) != "main" ]; then echo -$(git rev-parse --abbrev-ref HEAD) ; fi

tasks:
  git-push:
    desc: Commit & push the module
    cmds:
      - go mod tidy
      - git pull
      - git config advice.addIgnoredFile false
      - git add *
      - git commit -am 'updated {{ .PROJECT_NAME }} {{ .DATE }} for tag version {{ .UPDATED_TAG_VERSION }}{{ .BRANCH }}'
      - git push

  tag:
    desc: Commit, push & tag the module
    deps: [lint, test]
    cmds:
      - task: git-push
      - rm -rf dist
      - go mod tidy
      - git pull --tags
      - git tag -a {{ .UPDATED_TAG_VERSION }}{{ .BRANCH }} -m 'updated for stuttgart-things {{ .DATE }} for tag version {{ .UPDATED_TAG_VERSION }}{{ .BRANCH }}'
      - git push origin --tags

EOF
```

</details>

<details><summary><b>LINT & TEST</b></summary>

```bash
cat <<EOF > ./Taskfile.yaml
version: 3
tasks:
  lint:
    desc: Lint code
    cmds:
      - cmd: golangci-lint run
        ignore_error: true
  test:
    desc: Test code
    cmds:
      - go mod tidy
      - go test ./... -v
EOF
```

</details>

<details><summary><b>BUILD W/ LDFLAGS</b></summary>

```yaml
cat <<EOF > ./Taskfile.yaml
version: 3
vars:
  PROJECT_NAME:
    sh: pwd | grep -o "[^/]*$"
  REGISTRY: eu.gcr.io
  REPOSITORY_NAME: stuttgart-things
  MODULE: github.com/{{ .REPOSITORY_NAME }}/{{ .PROJECT_NAME }}
  GIT_COMMIT:
    sh: git log -n 1 --format=%h
  DATE:
    sh: date +"%y.%m%d.%H%M"

tasks:
  build:
    desc: Build the app
    deps: [lint, test]
    cmds:
      - go install -ldflags="-X {{ .MODULE }}/internal.date={{ .DATE }} -X {{ .MODULE }}/internal.version={{ .UPDATED_TAG_VERSION }} -X {{ .MODULE }}/internal.commit={{ .GIT_COMMIT }}"
      - "{{ .PROJECT_NAME }}"
  lint:
    desc: Lint code
    cmds:
      - cmd: golangci-lint run
        ignore_error: true
  test:
    desc: Test code
    cmds:
      - go mod tidy
      - go test ./... -v
EOF
```

</details>

<details><summary><b>GORELEASER</b></summary>

```yaml
cat <<EOF > ./Taskfile.yaml
version: 3
vars:
  PROJECT_NAME:
    sh: pwd | grep -o "[^/]*$"
  REPOSITORY_NAME: stuttgart-things
  MODULE: github.com/{{ .REPOSITORY_NAME }}/{{ .PROJECT_NAME }}
  DATE:
    sh: date +"%y.%m%d.%H%M"
  UPDATED_TAG:
    sh: old_tag=$(git describe --tags --abbrev=0 | cut -d "." -f3 | cut -d "-" -f1); new_tag=$((old_tag+1)); echo $new_tag
  UPDATED_TAG_VERSION:
    sh: t1=$(git describe --tags --abbrev=0 | cut -f1 -d'.'); t2=$(git describe --tags --abbrev=0 | cut -f2 -d'.'); echo $t1.$t2.{{ .UPDATED_TAG }}
  BRANCH:
    sh: if [ $(git rev-parse --abbrev-ref HEAD) != "main" ]; then echo -$(git rev-parse --abbrev-ref HEAD) ; fi

tasks:
  tag:
    desc: Commit, push & tag the module
    deps: [lint, test]
    cmds:
      - go mod tidy
      - git pull && git pull --tags
      - git add *
      - git config advice.addIgnoredFile false
      - git commit -am 'updated {{ .PROJECT_NAME }} {{ .DATE }} for tag version {{ .UPDATED_TAG_VERSION }}{{ .BRANCH }} '
      - git push
      - git tag -a {{ .UPDATED_TAG_VERSION }}{{ .BRANCH }} -m 'updated for stuttgart-things {{ .DATE }} for tag version {{ .UPDATED_TAG_VERSION }}{{ .BRANCH }}'
      - git push origin --tags

  release:
    desc: Relase binaries
    deps: [tag]
    cmds:
      - go install github.com/goreleaser/goreleaser@v{{ .GO_RELEASER_VERSION }}
      - unset GITLAB_TOKEN
      - goreleaser healthcheck
      - goreleaser check
      - goreleaser release --skip-publish --snapshot --clean
      - goreleaser release --clean
      - rm -rf ./dist
    vars:
      GO_RELEASER_VERSION: 1.20.0

EOF
```

</details>

<details><summary><b>INIT GO PROJECT</b></summary>

```yaml
cat <<EOF > ./Taskfile.yaml
version: 3
vars:
  PROJECT_NAME:
    sh: pwd | grep -o "[^/]*$"
  REPOSITORY_NAME: stuttgart-things
  MODULE: github.com/{{ .REPOSITORY_NAME }}/{{ .PROJECT_NAME }}
  GIT_COMMIT:
    sh: git log -n 1 --format=%h
  DATE:
    sh: date +"%y.%m%d.%H%M"

tasks:
  project-init-go:
    desc: Bootstrap project
    cmds:
      - go install github.com/goreleaser/goreleaser@latest
      - go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
      - go mod init {{ .MODULE }}
      - go mod tidy
      - goreleaser init
      - git add *
      - git add .goreleaser.yaml
      - git commit -am 'initialized go module {{ .Module }} on {{ .DATE }}'
      - git push
      - git tag -a v0.1.1 -m 'initialized go module {{ .Module }} on {{ .DATE }}'
      - git push origin --tags
EOF
```

</details>
