# stuttgart-things/docs/golang

## GORELEASER

### GITHUB ENTERPRISE

```yaml
# .goreleaser.yaml
github_urls:
  api: https://git.company.com/api/v3/
  upload: https://git.company.com/api/uploads/
  download: https://git.company.com/
  # set to true if you use a self-signed certificate
  skip_tls_verify: false
```

## CLI w/ COBRA

### INIT CLI

```bash
go install github.com/spf13/cobra-cli@latest
PROJECT_NAME=toolkit-chart-creator
mkdir ./${PROJECT_NAME} && cd ${PROJECT_NAME}
go mod init ${PROJECT_NAME}
cobra-cli init

# install locally
go install ./${PROJECT_NAME} # build binary to $GOPATH/bin
# or build binary
go build -o ./${PROJECT_NAME} # build binary to target dir
```

### ADD CMD

```bash
cobra-cli add version
```

### ADD SUB-CMD

```bash
cobra-cli add vm
cobra-cli add create -p 'vmCmd' # like sthings vm create
```

## BUILD ARM64 IMAGE W/ NERDCTL

### REGISTER QEMU

```bash
sudo systemctl start containerd
sudo nerdctl run --privileged --rm tonistiigi/binfmt --install all
ls -1 /proc/sys/fs/binfmt_misc/qemu*
```

### EXAMPLE DOCKERFILE

```bash
FROM arm64v8/golang:1.20 AS gobuilder
WORKDIR /tmp/build
COPY . .
RUN go build -o app

FROM arm64v8/alpine
ENTRYPOINT [ "/usr/local/bin/app" ]
COPY --from=gobuilder /tmp/build/app /usr/local/bin/app
```

### EXAMPLE BUILD

```bash
nerdctl build --platform=arm64 --output type=image,name=eu.gcr.io/stuttgart-things/wled-informer:0.1,push=true .
```

### EXAMPLE RUN

```bash
sudo nerdctl run eu.gcr.io/stuttgart-things/wled-informer:0.1 --platform=arm64
```
