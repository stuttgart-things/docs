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

## K8S-OPERATOR

### INSTALL OPERATOR SDK

```bash
OPERATOR_SDK_VERSION=v1.28.1
curl -LO https://github.com/operator-framework/operator-sdk/releases/download/${OPERATOR_SDK_VERSION}/operator-sdk_linux_amd64
sudo chmod +x operator-sdk_linux_amd64
sudo mv operator-sdk_linux_amd64 /usr/bin/operator-sdk
go version
operator-sdk version
```

### INIT/SCAFFOLD OPERATOR STRUCTURE

```bash
mkdir -p ~/projects/go/src/shipyard-operator && ~/projects/go/src/shipyard-operator
operator-sdk init \
--plugins go/v3 \
--domain sthings.tiab.ssc.sva.de \
--owner "patrick hermann" \
--project-name shipyard-operator \
--repo github.com/stuttgart-things/shipyard-operator

go mod tidy

go get sigs.k8s.io/controller-runtime@v0.14.1
```

### CREATE API/KIND

```bash
operator-sdk create api --group machineshop --version v1beta1 --kind Ansible #example
```

### EDIT TYPES

```bash
<OPERATOR-PATH>/api/<API-VERSION>/<KIND>_types.go

# example struct snippet
...
type AnsibleSpec struct {
	// +kubebuilder:default:="localhost"
	Hosts string   `json:"hosts,omitempty"`
	Vars  []string `json:"vars"`
	Roles []string `json:"roles,omitempty"`
}
...

```

### CREATE MANIFESTS

```bash
make manifests
```

### EDIT CONTROLLER

```bash
<OPERATOR-PATH>/controllers/<KIND>_controller.go

# example controller snippet

func (r *ShipyardTerraformReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	_ = log.FromContext(ctx)

	log := ctrllog.FromContext(ctx)
	log.Info("⚡️ Event received! ⚡️")
	log.Info("Request: ", "req", req)
...
}

```

### CREATE CONTAINER IMAGE

```bash
nerdctl build -t <IMG-ADDRESS:IMG-TAG> . && nerdctl push <IMG-ADDRESS:IMG-TAG>
```

### DEPLOY

```bash
make deploy IMG=<IMG-ADDRESS:IMG-TAG>
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
