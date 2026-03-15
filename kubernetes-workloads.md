# stuttgart-things/docs/kubernetes-workloads

## MICROSERVICES

<details><summary>DEPLOY APK-MIRROR</summary>

```bash
# APK MIRROR

## FETCH .apk FILES (DOCKER)

```bash
# CREATE LOCAL DIR
mkdir -p ./apk/v3.19/main/x86_64
```

```bash
# OPTION1: GET PACKAGES MANUALY FROM ALPINE CONTAINER
docker run --rm -it \
  -v "$(pwd)/apk/v3.19/main/x86_64:/mirror" \
  alpine sh

# INSIDE CONTAINER
cd /mirror

# Optional: set desired repo
echo "http://dl-cdn.alpinelinux.org/alpine/v3.19/main" > /etc/apk/repositories

# Update index
apk update

# Fetch packages + dependencies (stored in /mirror)
apk fetch --recursive --output . busybox curl

# Also fetch APKINDEX
wget http://dl-cdn.alpinelinux.org/alpine/v3.19/main/x86_64/APKINDEX.tar.gz
```

```bash
# OPTION2: USE SCRIPT

## CREATE SCRIPT
cat <<EOF > apk-schleuser.sh
# !/bin/sh
set -eux

BASE_IMAGE=$1
APK_PACKAGES=$2

# STEP 1: GET APK FROM BASE
VERSION_ID=$(docker run --rm $BASE_IMAGE sh -c \
  "grep '^VERSION_ID=' /etc/os-release | cut -d= -f2 | tr -d '\"' | cut -d. -f1,2")
echo ${VERSION_ID}

# --- Step 3: run container and fetch APK_PACKAGES ---
MIRROR_DIR="$(pwd)/apk/v${VERSION_ID}/main/x86_64"
rm -rf "$MIRROR_DIR" || true
mkdir -p "$MIRROR_DIR"

docker run --rm -it \
  -v "$MIRROR_DIR:/mirror" \
  "$BASE_IMAGE" sh -euxc "
    cd /mirror

    echo '[INFO] Using Alpine v${VERSION_ID} repository'
    echo 'http://dl-cdn.alpinelinux.org/alpine/v${VERSION_ID}/main' > /etc/apk/repositories

    apk update

    echo '[INFO] Fetching APK_PACKAGES: $APK_PACKAGES'
    apk fetch --recursive --output . $APK_PACKAGES

    echo '[INFO] Fetching APKINDEX'
    wget -q http://dl-cdn.alpinelinux.org/alpine/v${VERSION_ID}/main/x86_64/APKINDEX.tar.gz
  "

echo "[INFO] APK_PACKAGES and index saved under: $MIRROR_DIR"

zip -r ./apk-packages.zip $MIRROR_DIR
EOF

## RUN SCRIPT
sh apk-schleuser.sh python:3.10.0-alpine "curl git"
```

## TEST APK-MIRROR IN ALPINE CONTAINER (DOCKER)

```bash
# RUN ALPINE CONTAINER
docker run --rm -it alpine sh
```

```bash
# using host ip
echo "http://10.100.136.150:8080/v3.19/main" > /etc/apk/repositories
apk update
apk add busybox curl
```

## DEPLOY ON KUBERNETES

```bash
kubectl crate ns apk

kubectl -n apk apply -f - <<EOF
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: apk-mirror-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Mi
---
apiVersion: v1
kind: Pod
metadata:
  name: apk-mirror
  namespace: default
  labels:
    app: apk-mirror
spec:
  containers:
    - name: nginx
      image: docker.io/bitnami/nginx:1.29.0-debian-12-r2
      ports:
        - containerPort: 80
      volumeMounts:
        - name: apk-data
          mountPath: /usr/share/nginx/html/apk
  volumes:
    - name: apk-data
      persistentVolumeClaim:
        claimName: apk-mirror-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: apk-mirror
  namespace: default
spec:
  selector:
    app: apk-mirror
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
EOF
```

## UPLOAD .APK PACKAGES TO PVC

```bash
kubectl -n apk cp ./apk/. apk-mirror/apk-mirror:/usr/share/nginx/html/apk/ -c nginx
```

```bash
# TO VERIFY STRUCTURE ON NGINX POD-FILESYSTEM
kubectl exec -it apk-mirror -- sh

/usr/share/nginx/html/apk # tree
.
└── v3.19
    └── main
        └── x86_64
            ├── APKINDEX.tar.gz
            ├── busybox-1.36.1-r19.apk
            └── musl-1.2.4_git20230717-r5.apk

3 directories, 3 files
```

## TEST MIRROR INSIDE POD

```bash
kubectl run apk-test \
--image=alpine:3.22.1 \
--restart=Never \
--rm -it -- sh
```

```bash
echo "http://apk-mirror.default.svc.cluster.local/apk/v3.19/main" > /etc/apk/repositories

apk update
apk add busybox curl
```

</details>


<details><summary>DEPLOY SFTP/HTTPS CADDY-WEBSERVER</summary>

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: file-server
  labels:
    app: file-server
spec:
  replicas: 1
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: file-server
  template:
    metadata:
      labels:
        app: file-server
    spec:
      securityContext:
        fsGroup: 911 # ssh server user
      containers:
        - name: caddy
          image: caddy:2.6.4
          ports:
            - containerPort: 80
          volumeMounts:
            - name: file-server
              mountPath: /var/www/html/
              subPath: public
            - name: caddyfile
              mountPath: /etc/caddy/Caddyfile
              subPath: Caddyfile
        - name: openssh-server
          image: linuxserver/openssh-server:version-9.0_p1-r2
          ports:
            - containerPort: 2222
          env:
            - name: USER_NAME
              value: "ankit"
            - name: PUBLIC_KEY
              value: ""
            - name: PASSWORD_ACCESS
              value: "true"
            - name: USER_PASSWORD
              value: "<CHANGEME>"
          volumeMounts:
            - name: file-server
              mountPath: /var/www/html/
              subPath: public
      volumes:
        - name: file-server
          persistentVolumeClaim:
            claimName: file-server-pvc
        - name: caddyfile
          configMap:
            name: caddyfile-v3
            defaultMode: 0644
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: caddyfile-v3
data:
  Caddyfile: |
    :80 {
            # Set this path to your site's directory.
            root * /var/www/html
            # Enable the static file server, with file browsing
            file_server browse
    }
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: file-server-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2G
---
apiVersion: v1
kind: Service
metadata:
  name: file-server-http
  labels:
    app: file-server-http
spec:
  type: ClusterIP
  selector:
    app: file-server
  ports:
    - name: http
      port: 80
      targetPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: file-server-ssh
  labels:
    app: file-server-ssh
spec:
  type: LoadBalancer
  selector:
    app: file-server
  ports:
    - name: ssh
      port: 22
      targetPort: 2222
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: files-ingress-tls
  namespace: default
spec:
  commonName: files.dev43.sthings-pve.labul.sva.de
  dnsNames:
    - files.dev43.sthings-pve.labul.sva.de
  issuerRef:
    kind: ClusterIssuer
    name: cluster-issuer-approle
  secretName: files-ingress-tls
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: files-ingress
  namespace: default
  labels:
    app: file-server-ssh
spec:
  ingressClassName: nginx
  rules:
    - host: files.dev43.sthings-pve.labul.sva.de
      http:
        paths:
          - backend:
              service:
                name: file-server-http
                port:
                  number: 80
            path: /
            pathType: Prefix
  tls:
    - hosts:
        - files.dev43.sthings-pve.labul.sva.de
      secretName: files-ingress-tls
```

```bash
# UPLOAD FILE
sudo apt -y install lftp
touch ./bla.txt && echo hello > ./bla.txt # JUST A FILE EXAMPLE
lftp sftp://ankit:<PASSWORD>@10.31.101.17 -e "cd /var/www/html/; put bla.txt; bye"

# DOWNLOAD/ACCESS FILE VIA HTTPS
wget wget https://files.dev43.sthings-pve.labul.sva.de/bla.txt
```

</details>

<details><summary>VCLUSTER</summary>

```bash
vcluster create my-vcluster --expose --set storage.className=openebs-hostpath
vcluster disconnect
vcluster connect my-vcluster -n vcluster-my-vcluster


helm upgrade --install xplane-vlcuster \
vcluster \
--repo https://charts.loft.sh \
--namespace vcluster \
--repository-config='' \
--create-namespace

vcluster connect xplane-vlcuster -n vcluster

helm uninstall xplane-vlcuster -n vcluster
```

</details>

<details><summary>OCI ARTIFACTS W/ ORAS</summary>

```bash
# LOGIN
oras login zot.maverick.sthings-pve.labul.sva.de
# OR
oras login ghcr.io -u patrick-hermann-sva -p ${GITHUB_TOKEN}
```

```bash
# PUSH FILE
echo "hello world" > artifact.txt
oras push zot.maverick.sthings-pve.labul.sva.de/hello-artifact:v1 \
--artifact-type application/vnd.acme.rocket.config \
artifact.txt:text/plain
```

```bash
# PUSH FOLDER
cd /tmp/hugo/static/dagger
oras push \
ghcr.io/stuttgart-things/static:v1 \
--artifact-type=application/vnd.unknown.layer.v1+tar .

```bash
# PULL ARTIFACT
oras pull zot.maverick.sthings-pve.labul.sva.de/hello-artifact:v1
oras pull ghcr.io/stuttgart-things/static:v1
```

```bash
# EXTRACT CONTENT FROM IMAGE

# Step 1: Copy to OCI layout
oras copy ghcr.io/stuttgart-things/idp:20250612-093912 --to-oci-layout ./tmp-layout

# Step 2: Find and extract the blob
cd ./tmp-layout/blobs/sha256

# List blobs by size (to find the tar.gz layer)
ls -lhS

# Assume it's called e.g. 8f5701f6b2... (your tar.gz)
mkdir /tmp/idp-content
tar -xzf 8f5701f6b22e07d8a64e3d6f713a00705e4d0323ed2d32069ebde4d08fe888bd -C /tmp/idp-content
```

</details>

<details><summary>BUILDAH</summary>

```bash
# RUN DEBUG CONTAINER
kubectl run buildah-debug --namespace registry --image=quay.io/buildah/stable:v1 --restart=Never --overrides='
{
  "apiVersion": "v1",
  "spec": {
    "containers": [{
      "name": "buildah",
      "image": "quay.io/buildah/stable:v1",
      "securityContext": {
        "privileged": true
      },
      "stdin": true,
      "tty": true
    }]
  }
}'   --stdin --tty --attach
```

```
# USE ALIAS FOR PULLED IMAGE
buildah pull python:3.11-slim
buildah tag python:3.11-slim registry-docker-registry.registry.svc.cluster.local:5000/python:3.11-slim
buildah --tls-verify=false push registry-docker-registry.registry.svc.cluster.local:5000/python:3.11-slim

buildah login registry-docker-registry.registry.svc.cluster.local:5000 --tls-verify=false

# change alias in /etc/containers/registries.conf.d/000-shortnames.conf
# e.g.
"python" = "registry-docker-registry.registry.svc.cluster.local:5000/python"

curl -u admin:<PW> -X GET http://registry-docker-registry.registry.svc.cluster.local:5000/v2/_catalog
```

</details>


<details><summary>GOLDILOCKS, VPA + PROMETHEUS</summary>


## KUBEVIRT

<details><summary><b>INSTALLATION</b></summary>

```bash
# POINT AT LATEST RELEASE
export RELEASE=$(curl https://storage.googleapis.com/kubevirt-prow/release/kubevirt/kubevirt/stable.txt)

# DEPLOY THE KUBEVIRT OPERATOR
kubectl apply -f https://github.com/kubevirt/kubevirt/releases/download/${RELEASE}/kubevirt-operator.yaml

# CREATE THE KUBEVIRT CR (INSTANCE DEPLOYMENT REQUEST) WHICH TRIGGERS THE ACTUAL INSTALLATION
wget https://github.com/kubevirt/kubevirt/releases/download/${RELEASE}/kubevirt-cr.yaml

yq eval '.spec.configuration.developerConfiguration.useEmulation = true' -i kubevirt-cr.yaml

kubectl apply -f kubevirt-cr.yaml

# WAIT UNTIL ALL KUBEVIRT COMPONENTS ARE UP
kubectl -n kubevirt wait kv kubevirt --for condition=Available
```

```bash
# INSTALL VIRTCTL
export VERSION=$(curl https://storage.googleapis.com/kubevirt-prow/release/kubevirt/kubevirt/stable.txt)
wget https://github.com/kubevirt/kubevirt/releases/download/${VERSION}/virtctl-${VERSION}-linux-amd64
sudo chmod +x virtctl-${VERSION}-linux-amd64
sudo mv virtctl-${VERSION}-linux-amd64 /usr/local/bin/virtctl
```

</details>

<details><summary><b>EASY-VM</b></summary>

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: testvm
spec:
  running: false
  template:
    metadata:
      labels:
        kubevirt.io/size: small
        kubevirt.io/domain: testvm
    spec:
      domain:
        devices:
          disks:
            - name: containerdisk
              disk:
                bus: virtio
            - name: cloudinitdisk
              disk:
                bus: virtio
          interfaces:
          - name: default
            masquerade: {}
        resources:
          requests:
            memory: 64M
      networks:
      - name: default
        pod: {}
      volumes:
        - name: containerdisk
          containerDisk:
            image: quay.io/kubevirt/cirros-container-disk-demo
        - name: cloudinitdisk
          cloudInitNoCloud:
            userDataBase64: SGkuXG4=
```

```bash
kubectl get vms
virtctl console testvm
```

</details>

<details><summary><b>UBUNTU-VM WITH NODEPORT SERVICE</b></summary>

```yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachineInstance
metadata:
  name: vm1
  labels:
    vmi : vm1
spec:
  architecture: amd64
  terminationGracePeriodSeconds: 30
  domain:
    machine:
      type: q35
    resources:
      requests:
        memory: 2056M
    devices:
      interfaces:
        - masquerade: {}
          name: default
      disks:
      - name: containerdisk
        disk:
          bus: virtio
      - disk:
          bus: virtio
        name: cloudinitdisk
  networks:
    - name: default
      pod: {}
  volumes:
  - name: containerdisk
    containerDisk:
      image: mcas/kubevirt-ubuntu-20.04:latest
  - name: cloudinitdisk
    cloudInitNoCloud:
      userData: |-
        #cloud-config
        password: ubuntu
        chpasswd: { expire: False }
        ssh_authorized_keys:
        - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCsHiyet7tO+qXYKEy6XBiHNICRfGsBZYIo/JBQ2i16WgkC7rq6bkGwBYtni2j0X2pp0JVtcMO+hthqj37LcGH02hKa24eAoj2UdnFU+bhYxA6Mau1B/5MCkvs8VvBjxtM3FVJE7mY5bZ19YrKJ9ZIosAQaVHiGUu1kk49rzQqMrwT/1PNbUYW19P8J2LsfnaYJIl4Ljbxr0k52MGdbKwgxdph3UKciQz2DhutrmO0gf3Ncn4zpdClldaBtDB0EMMqD3BAtEVsucttzqdeYQwixMTtyuGpAKAJNUqhpleeVhShPZLke0vXxlA6/fyfkSM78gN2FQcRGVPN6hOMkns/b
        package_update: false
        package_upgrade: false
        packages:
        - qemu-guest-agent
        runcmd:
        - [ systemctl, start, qemu-guest-agent ]
---
apiVersion: v1
kind: Service
metadata:
  name: vm1-svc
spec:
  ports:
  - port: 22
    name: ssh
    protocol: TCP
    targetPort: 22
  - port: 1234
    name: jupyter
    protocol: TCP
    targetPort: 1234
  selector:
    vmi : vm1
  type: NodePort
# kubectl get VirtualMachineInstance
# virtctl console vm1
# ssh ubuntu@10.31.103.22 -p 30866
```

</details>

