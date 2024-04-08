# stuttgart-things/docs/containerization

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
