# stuttgart-things/docs/containerization

containerization is a software deployment process that bundles an application's code with all the files and libraries it needs to run on any infrastructure.

## BUILD

<details><summary>BUILD w/BUILDX</summary>

```bash
docker buildx build . -f Dockerfile -o dest=hello-world.tar -t hello-world:v1
```

</details>

<details><summary>BUILD OCI-IMAGE W/ BUILDAH</summary>

```bash
buildah --storage-driver=overlay bud --format=oci \
--tls-verify=true --no-cache \
-f ~/projects/github/stuttgart-things/images/sthings-alpine/Dockerfile \
-t scr.app.4sthings.tiab.ssc.sva.de/sthings-alpine/alpine:123
```

</details>

<details><summary>BUILD CONTAINER IMAGE w/ KANIKO (NO PUSH)</summary>

```bash
nerdctl run gcr.io/kaniko-project/executor:v1.23.1 \
--dockerfile Dockerfile \
--context git://github.com/stuttgart-things/stuttgart-things \
--context-sub-path images/sthings-alpine/  \
--no-push
```

```bash
nerdctl run --entrypoint sh -it sthings-kaniko:v3

# BUILD LOCAL AS TAR
executor --dockerfile Dockerfile \
--context git://github.com/stuttgart-things/stuttgart-things \
--context-sub-path images/sthings-terraform \
--no-push \
--tar-path /tmp/bla.tar

# BUILD AS REMOTE (REGISTRY) DESTINATION
executor --dockerfile Dockerfile \
--context git://github.com/stuttgart-things/stuttgart-things \
--context-sub-path images/sthings-terraform \
--destination registry.app-dev.sthings-vsphere.labul.sva.de/terr:v1
```

```bash
skopeo login scr.cd43.sthings-pve.labul.sva.de -u admin -p <PASSWORD>

skopeo copy -f oci tarball:/tmp/bla.tar docker://scr.cd43.sthings-pve.labul.sva.de/crossplane-demo/test:v1
```

</details>

<details><summary>BUILD CONTAINER IMAGE w/ KANIKO, MOUNT LOCAL CONTEXT + REGISTRY CERT</summary>

```
nerdctl run \
-v $HOME/.docker/config.json:/kaniko/.docker/config.json:ro \
-v /home/sthings/projects/golang/homerun-react/react-app:/workspace/ \
gcr.io/kaniko-project/executor:v1.23.1 \
--dockerfile Dockerfile \
--destination scr.cd43.sthings-pve.labul.sva.de/homerun/frontend:v11 \
--skip-tls-verify
```

</details>


## RUN

<details><summary>GET HTPASSWD</summary>

```bash
nerdctl run --entrypoint htpasswd httpd:2 -Bbn <USERNAME> <PASSWORD>
```

</details>

<details><summary>OVERWRITE ENTRYPOINT OF IMAGE W/ NERDCTL</summary>

```bash
nerdctl run -it --entrypoint sh eu.gcr.io/stuttgart-things/stagetime-server:23.1108.1227-0.3.22
```

</details>

<details><summary>JUMP INTO (ALREADY) RUNNING CONTAINER W/ DOCKER</summary>

```bash
#https://blog.kubesimplify.com/getting-started-with-ko-a-fast-container-image-builder-for-your-go-applications

# RUN CONTAINER DETACHED
sudo docker run -d --name new-webserver nginx

# JUMP IN
sudo docker exec -it new-webserver sh
```

</details>

<details><summary>JUMP INTO (TO BE STARTED) CONTAINER W/ DOCKER</summary>

```bash
sudo docker run -it -v /home/test/stuttgart-things:/app/ eu.gcr.io/stuttgart-things/sthings-packer:1.10.2-9.4.0 sh
```

</details>

## IMAGE BUILD

<details><summary>GOLANG IMAGE BUILD IMAGE W/ KO</summary>

```bash
# REGISTRY LOGIN
ko login scr.cd43.sthings-pve.labul.sva.de -u sthings -p <PASSWORD>

# URL FOR PUBLISHING IMAGE
export KO_DOCKER_REPO=eu.gcr.io/stuttgart-things/machineshop

# KO CONFIG (NOT MANDATORY)
cat <<EOF > .ko.yaml
---
defaultBaseImage: eu.gcr.io/stuttgart-things/sthings-alpine:3.12.2-alpine3.19
EOF

# BUILD IMAGE
ko build github.com/stuttgart-things/machineshop
```

</details>


<details><summary>BUILD IMAGE W/ DOCKER</summary>

```bash
# CREATE DOCKERFILE
cat <<EOF > ./Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]
EXPOSE 3000
EOF
```

```bash
# BUILD IMAGE (DOCKERFILE) EXISTS IN CURRENT DIR = .
docker build -t myapp:v3 .

# DOCKERFILE IN DIFFERENT LOCATION THAN BUILD COMMAND IS EXECUTED
docker build -t myapp:v3 /apps/myapp/
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

<details><summary>HARBOR PULL THROUGH MIRROR</summary>

### HARBOR DEPLOYMENT

```bash
cat <<EOF > ./harbor.yaml
adminPassword: whatever
clusterDomain: example.com
exposureType: ingress
externalURL: harbor.example.com
global:
  defaultStorageClass: nfs4-csi
  storageClass: nfs4-csi
ingress:
  core:
    annotations:
      cert-manager.io/cluster-issuer: cluster-issuer-approle
      ingress.kubernetes.io/proxy-body-size: "0"
      ingress.kubernetes.io/ssl-redirect: "true"
      nginx.ingress.kubernetes.io/proxy-body-size: "0"
      nginx.ingress.kubernetes.io/ssl-redirect: "true"
    extraTls:
    - hosts:
      - harbor.example.com
      secretName: harbor.example.com-tls
    hostname: harbor.example.com
    ingressClassName: nginx
    tls: true
ipFamily:
  ipv4:
    enabled: true
  ipv6:
    enabled: false
persistence:
  enabled: true
  persistentVolumeClaim:
    jobservice:
      size: 1Gi
    registry:
      size: 12Gi
    trivy:
      size: 5Gi
  resourcePolicy: ""
service:
  type: ClusterIP
EOF

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm upgrade --install harbor -n harbor --create-namespace --values values.yaml --version 24.4.1 bitnami/harbor

```

### CREATE DOCKER PROXY MIRROR

* Go to the Registries tab.
* Create the endpoint for Dockerhub
* Create a new proxy cache project (e.g. name: docker) using the registry

### TEST DOCKER MIRROR

```bash
# THIS IS A LOCAL TEST IF THE MIRROR (named docker) IS WORKING
docker pull harbor.example/docker/nginx:1.26.3-alpine
```

### DEPLOY PROXY

```bash
cat <<EOF > ./mirror.yaml
---
ingress:
  enabled: true
  className: nginx
  annotations:
    kubernetes.io/ingress.class: nginx
    kubernetes.io/tls-acme: "true"
  hosts:
    - host: docker.harbor.example.com
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls:
   - secretName: docker-mirror
     hosts:
       - docker.harbor.example.com
EOF

helm upgrade --install harbor-mirror oci://ghcr.io/hiddenmarten/harbor-project-proxy --values mirror.yaml -n harbor
```

### CREATE DOCKER REGISTRY MIRROR

[proxy-cache-harbor](https://felipetrindade.com/proxy-cache-harbor/)
[harbor-project-proxy](https://github.com/hiddenmarten/harbor-project-proxy/tree/main)
[proxy-issue](https://github.com/goharbor/harbor/issues/8082)

```bash
sudo cat <<EOF > /etc/docker/daemon.json
{
  "registry-mirrors": ["https://docker.harbor.example.com"],
  "group": "dockerroot"
}
EOF

sudo systemctl restart docker
```


</details>

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

## COPY TAR TO CLUSTER INTERNAL-DOCKER-REGISTRY

```bash
# SHELL1
kubectl -n registry run skopeo \
  --image=bdwyertech/skopeo \
  --restart=Never \
  --overrides='
{
  "spec": {
    "containers": [{
      "name": "skopeo",
      "image": "bdwyertech/skopeo",
      "stdin": true,
      "tty": true,
      "securityContext": { "runAsUser": 0 }
    }]
  }
}' \
--stdin --tty --attach

# SHELL2 - COPY (PREBUILD IMAGE) TAR TO POD
kubectl -n registry cp base.tar skopeo2:/tmp

# SHELL1 - LOGIN, PUSH + VERIFY
skopeo login \
registry-docker-registry.registry.svc.cluster.local:5000 \
--tls-verify=false

skopeo copy \
docker-archive:/tmp/base.tar \
docker://registry-docker-registry.registry.svc.cluster.local:5000/shuffle/shuffle:app_sdk_0.0.25 \
--tls-verify=false

apk add curl
curl -u ${REG_USER}:${REG_PASSWORD} \
http://registry-docker-registry.registry.svc.cluster.local:5000/v2/_catalog
```

## SYSTEMD

<details><summary>PODMAN QUATLET</summary>

[redhat-multi-quatlet](https://www.redhat.com/sysadmin/multi-container-application-podman-quadlet)

```bash
# INSTALL PODLET
wget https://github.com/containers/podlet/releases/download/v0.3.0/podlet-x86_64-unknown-linux-gnu.tar.xz
tar -xf podlet-x86_64-unknown-linux-gnu.tar.xz
sudo mv podlet-x86_64-unknown-linux-gnu/podlet /usr/bin/podlet
sudo chmod +x /usr/bin/podlet
```

```bash
# GENERATE FROM RUN COMMAND
podlet --file . --install --description webserver podman run -d --name webserver -p 80:80 nginx:latest
```

```bash
# GENERATE FROM EXISTING CONTAINER
podlet generate container 17803fe422cd
```

```bash
# DRYRUN - ROOTFUL
sudo cp ./webserver.container /etc/containers/systemd
sudo /usr/libexec/podman/quadlet --dryrun webserver.container
```

```bash
# ENABLE/START SERVICE - ROOTFUL
sudo cp ./webserver.container /etc/containers/systemd
sudo systemctl daemon-reload
sudo systemctl enable --now webserver.service
sudo systemctl start webserver.service
```

```bash
# TEST SERVICE
sudo firewall-cmd --zone=public --add-port=80/tcp
sudo firewall-cmd --zone=public --add-service=http --permanent
curl localhost
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

</details>

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
