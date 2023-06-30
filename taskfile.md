# TASKFILE

A task runner / simpler Make alternative written in Go

<details><summary><b>INIT GO PROJECT</b></summary>

```yaml
cat <<EOF > ./taskfile.yaml
version: 3
vars:
  REPOSITORY_NAME: stuttgart-things
  MODULE: github.com/{{ .REPOSITORY_NAME }}/{{ .PROJECT_NAME }}
  PROJECT_NAME:
    sh: pwd | grep -o "[^/]*$"
  GIT_COMMIT:
    sh: git log -n 1 --format=%h
  DATE:
    sh: date +"%y.%m%d.%H%M"

tasks:
  project-init-go:
    desc: Bootstrap project
    cmds:
      - go mod init {{ .Module }}
      - go mod tidy
      - git add go.mod
      - git commit -am 'initialized go module {{ .Module }} on {{ .DATE }}'
      - git push
      - git tag -a v0.1.0 -m 'initialized go module {{ .Module }} on {{ .DATE }}'
      - git push origin --tags
EOF      
```

</details>
