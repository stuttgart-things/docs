# stuttgart-things/docs/containerization

containerization is a software deployment process that bundles an application's code with all the files and libraries it needs to run on any infrastructure.

## RUN

<details><summary>JUMP INTO (ALREADY) RUNNING CONTAINER W/ DOCKER</summary>

```bash
# RUN CONTAINER DETACHED
sudo docker run -d --name new-webserver nginx
# JUMP IN
sudo docker exec -it new-webserver sh
``` 
</details>

<details><summary>JUMP INTO (NO) RUNNING NEW CONTAINER W/ DOCKER</summary>

```bash
sudo docker run -it -v /home/openlab/test/stuttgart-things/packer/builds:/app/ <IMAGE-ID>
``` 
</details>


## IMAGE BUILD

<details><summary>BUILD IMAGE W/ DOCKER</summary>
  
```bash
docker build - < Dockerfile
```
</details>

<details><summary>BUILD ARM64 IMAGE W/ NERDCTL</summary>

```bash
# REGISTER QEMU
sudo systemctl start containerd
sudo nerdctl run --privileged --rm tonistiigi/binfmt --install all
ls -1 /proc/sys/fs/binfmt_misc/qemu*
```

```bash
# EXAMPLE DOCKERFILE
FROM arm64v8/golang:1.20 AS gobuilder
WORKDIR /tmp/build
COPY . .
RUN go build -o app

FROM arm64v8/alpine
ENTRYPOINT [ "/usr/local/bin/app" ]
COPY --from=gobuilder /tmp/build/app /usr/local/bin/app
```

```bash
# EXAMPLE BUILD
nerdctl build --platform=arm64 --output type=image,name=eu.gcr.io/stuttgart-things/wled-informer:0.1,push=true .
```

```bash
# EXAMPLE RUN
sudo nerdctl run eu.gcr.io/stuttgart-things/wled-informer:0.1 --platform=arm64
```

</details>

## IMAGE HANDLING

<details><summary>PULL IMAGES W/ CTR</summary>

```bash
# PULL IMAGE W/ CRT
sudo ctr images pull docker.io/library/redis:alpine
# OR FOR RKE2 BUNDLED CONTAINERD: SUDO /VAR/LIB/RANCHER/RKE2/BIN/CTR IMAGES PULL DOCKER.IO/LIBRARY/REDIS:ALPINE
```

</details>

<details><summary>LOAD IMAGES W/ CTR</summary>

```bash
# LOAD/IMPORT CONATINER IMAGE
ctr -n=k8s.io images import <IMAGE_NAME>
ctr image export <output-filename> <image-name>
```

</details>

<details><summary>LIST IMAGES W/ CTR</summary>

```bash
ctr --namespace k8s.io images ls -q
# OR FOR RKE2 BUNDLED CONTAINERD: SUDO /VAR/LIB/RANCHER/RKE2/BIN/CTR --ADDRESS /RUN/K3S/CONTAINERD/CONTAINERD.SOCK --NAMESPACE K8S.IO CONTAINER LS
```

</details>

<details><summary>SKOPEO</summary>

## INSTALL

```bash
SKOPEO_VERSION=1.12.0
wget https://github.com/lework/skopeo-binary/releases/download/v${SKOPEO_VERSION}/skopeo-linux-amd64
sudo chmod +x skopeo-linux-amd64
sudo mv skopeo-linux-amd64 /usr/bin/skopeo && skopeo --version
```

## COPY IMAGE BETWEEN REGISTRIES (TAG)

```bash
skopeo copy --insecure-policy docker://nginx:1.21
docker://whatever.cloud/gtc1fe/web:1.21
```

## COPY IMAGES BETWEEN REGISTRIES

```bash
skopeo copy --all --insecure-policy
docker://nginx@sha256:ff2a5d557ca22fa93669f5e70cfbeefda32b98f8fd3d33b38028c582d700f93a \ docker://whatever.cloud/gtc1fe/web@sha256:ff2a5d557ca22fa93669f5e70cfbeefda32b98f8fd3d33b38028c582d700f93a
```

</details>

## HOUSE-KEEPING

<details><summary>CLEANUP W/ NERDCTL</summary>

```bash
# STOP AND DELETE ALL RUNNING CONTAINERS
sudo nerdctl stop $(sudo nerdctl ps -a | awk '{ print $1 }' | grep -v CONTAINER); sudo nerdctl rm $(sudo nerdctl ps -a | awk '{ print $1 }' | grep -v CONTAINER)

# CLEAN IMAGES BY ID
sudo nerdctl rmi $(sudo nerdctl images | grep "2 months ago" | awk '{ print $3 }')

# CLEAN IMAGES BY NAME + TAG
sudo nerdctl rmi $(sudo nerdctl images | grep "7 weeks ago" | awk '{ print $1":"$2 }')
```

</details>

## CONTAINERD

<details><summary>INSTALL CONTAINERD</summary>

```bash
wget https://github.com/containerd/containerd/releases/download/v1.7.1/containerd-1.7.1-linux-amd64.tar.gz
sudo tar Cxzvf /usr/local containerd-1.7.1-linux-amd64.tar.gz
wget https://raw.githubusercontent.com/containerd/containerd/main/containerd.service
sudo mv containerd.service /usr/lib/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable --now containerd
sudo systemctl status containerd

sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl status containerd
sudo journalctl -u containerd
```

<details><summary>INSTALL RUNC</summary>

```bash
wget https://github.com/opencontainers/runc/releases/download/v1.1.7/runc.amd64
sudo install -m 755 runc.amd64 /usr/local/sbin/runc
sudo ls /usr/local/sbin/ #check
```

</details>

<details><summary>INSTALL CNI PLUGINS</summary>

```bash
wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-amd64-v1.3.0.tgz
sudo mkdir -p /opt/cni/bin
sudo tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.3.0.tgz
```

</details>