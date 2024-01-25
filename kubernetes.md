# stuttgart-things/docs/k8s

## KUBECTL

<details><summary>FORCE DELETE POD</summary>

```bash
# E.G. INFLUXDB (STUCK IN DELETING PHASE)
kubectl delete po influxdb-influxdb2-0 --force -n influxdb
```

</details>

<details><summary>PORTFORWARDING</summary>

```bash
kubectl --namespace longhorn-system port-forward --address 0.0.0.0 service/longhorn-frontend 5080:80
# CHECK LOCALHOST/FQDN
# e.g. http://nashville.tiab.labda.sva.de:5080/#/dashboard
# e.g. http://localhost:5080/#/dashboard
```

</details>

<details><summary>GET/DELETE ALL PODS OLDER THAN 24HOURS</summary>

```bash
# LIST ALL PODS OLDER THAN 1 DAY
kubectl -n tektoncd get pod | awk 'match($5,/[0-9]+d/) {print $0}'

# DELETE ALL PODS OLDER THAN 1 DAY
kubectl -n tektoncd delete pod $(kubectl -n tektoncd get pod | awk 'match($5,/[0-9]+d/) {print $1}')
```

</details>

<details><summary>STORAGECLASS EXAMPLE</summary>

```bash
# NFS CSI DEPLOYMENT
helm repo add csi-driver-nfs https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts
helm upgrade --install csi-driver-nfs csi-driver-nfs/csi-driver-nfs --namespace kube-system --version v4.5.0
```

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  labels:
    app.kubernetes.io/managed-by: Helm
    helm.toolkit.fluxcd.io/name: nfs-csi-configuration
    helm.toolkit.fluxcd.io/namespace: kube-system
  name: nfs4-csi
parameters:
  mountPermissions: "0777"
  server: pve-nfs-tekton.labul.sva.de
  share: /var/nfs/k8s
provisioner: nfs.csi.k8s.io
reclaimPolicy: Delete
volumeBindingMode: Immediate
---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  labels:
    app.kubernetes.io/managed-by: Helm
    helm.toolkit.fluxcd.io/name: nfs-csi-configuration
    helm.toolkit.fluxcd.io/namespace: kube-system
  name: nfs3-csi
parameters:
  mountPermissions: "0777"
  server: pve-nfs-tekton.labul.sva.de
  share: /var/nfs/k8s
provisioner: nfs.csi.k8s.io
reclaimPolicy: Delete
volumeBindingMode: Immediate
```

### PVC EXAMPLE

```yaml
# PVC
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pv-claim
spec:
  storageClassName: nfs4-csi
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
```

```yaml
# POD FOR MOUNTING PVC
apiVersion: v1
kind: Pod
metadata:
  name: task-pv-pod
spec:
  volumes:
    - name: task-pv-storage
      persistentVolumeClaim:
        claimName: task-pv-claim
  containers:
    - name: task-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-pv-storage
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

# CLIS

<details><summary>SAST W/ POLARIS</summary>

```yaml
# EXAMPLE POD.YAML
cat <<EOF > /tmp/pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
EOF
```

```bash
# CHECK POD.YAML
polaris audit --audit-path /tmp/pod.yaml --only-show-failed-tests --severity error
```

</details>

<details><summary>VCLUSTER</summary>

```bash
vcluster create my-vcluster --expose --set storage.className=openebs-hostpath
vcluster disconnect
vcluster connect my-vcluster -n vcluster-my-vcluster
```

</details>

<details><summary>OCI ARTIFACTS W/ ORAS</summary>

```bash
# PUSH
oras login zot.maverick.sthings-pve.labul.sva.de
echo "hello world" > artifact.txt
oras push zot.maverick.sthings-pve.labul.sva.de/hello-artifact:v1 \
--artifact-type application/vnd.acme.rocket.config \
artifact.txt:text/plain
```


```bash
# PULL
oras pull zot.maverick.sthings-pve.labul.sva.de/hello-artifact:v1
```

</details>

## DEPLOY VPA + PROMETHEUS

### DEPLOY VPA

```bash
kubectl create ns monitoring
helm repo add fairwinds-stable https://charts.fairwinds.com/stable && helm repo update
helm upgrade --install vpa fairwinds-stable/vpa -n monitoring  --version 3.0.2 --create-namespace
helm -n monitoring test vpa
```

### FORKED GIT-REPOSITORY: FOR RKE CLUSTERS (at least for =<52.1.0)

```bash
git clone https://github.com/mohamadkhani/helm-charts.git
cd helm-charts/kube-prometheus-stack && helm dep update
```

### HELM REPO: NON RKE/RANCHER K8S

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

### CREATE TLS CERTIFICATE

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: monitoring-ingress
  namespace: monitoring
spec:
  commonName: monitoring.dev43.sthings-pve.labul.sva.de
  dnsNames:
    - monitoring.dev43.sthings-pve.labul.sva.de
  issuerRef:
    kind: ClusterIssuer
    name: cluster-issuer-approle
  secretName: monitoring-tls
```

### CREATE VALUES FILE

```yaml
cat <<EOF > ./values.yaml
alertmanager:
  enabled: false
prometheus:
  prometheusSpec:
    scrapeInterval: 30s
    evaluationInterval: 30s
    retention: 24h
    resources:
      requests:
        cpu: 200m
        memory: 200Mi
    podMonitorNamespaceSelector: { }
    podMonitorSelector:
      matchLabels:
        app.kubernetes.io/component: monitoring
grafana:
  defaultDashboardsEnabled: true
  adminPassword: <CHANGEME>
  ingress:
    enabled: true
    ingressClassName: nginx
    hosts:
      - monitoring.dev43.sthings-pve.labul.sva.de
    path: /
    tls:
      - secretName: monitoring-tls
        hosts:
          - monitoring.dev43.sthings-pve.labul.sva.de
kube-state-metrics:
  rbac:
    extraRules:
      - apiGroups: ["autoscaling.k8s.io"]
        resources: ["verticalpodautoscalers"]
        verbs: ["list", "watch"]
  prometheus:
    monitor:
      enabled: true
  customResourceState:
    enabled: true
    config:
      kind: CustomResourceStateMetrics
      spec:
        resources:
          - groupVersionKind:
              group: autoscaling.k8s.io
              kind: "VerticalPodAutoscaler"
              version: "v1"
            labelsFromPath:
              verticalpodautoscaler: [metadata, name]
              namespace: [metadata, namespace]
              target_api_version: [apiVersion]
              target_kind: [spec, targetRef, kind]
              target_name: [spec, targetRef, name]
            metrics:
              - name: "vpa_containerrecommendations_target"
                help: "VPA container recommendations for memory."
                each:
                  type: Gauge
                  gauge:
                    path: [status, recommendation, containerRecommendations]
                    valueFrom: [target, memory]
                    labelsFromPath:
                      container: [containerName]
                commonLabels:
                  resource: "memory"
                  unit: "byte"
              - name: "vpa_containerrecommendations_target"
                help: "VPA container recommendations for cpu."
                each:
                  type: Gauge
                  gauge:
                    path: [status, recommendation, containerRecommendations]
                    valueFrom: [target, cpu]
                    labelsFromPath:
                      container: [containerName]
                commonLabels:
                  resource: "cpu"
                  unit: "core"
  selfMonitor:
    enabled: true
EOF
```

### DEPLOY KUBE-PROMETHEUS-STACK

```bash
helm upgrade --install kube-prometheus-stack . --values values.yaml --version 52.1.0 --namespace monitoring --create-namespace
# OR W/ HELM REPOSITORY
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack --values values.yaml --version 52.1.0 --namespace monitoring --create-namespace
```

### DEPLOY GOLDILOCKS

```bash
helm repo add fairwinds-stable https://charts.fairwinds.com/stable && helm repo update
helm upgrade --install goldilocks --namespace monitoring fairwinds-stable/goldilocks --version 8.0.0 --create-namespace
```

### LABEL NAMESPACE W/ GOLDILOCKS

```bash
kubectl label ns velero goldilocks.fairwinds.com/enabled=true
```

## NFS STORAGE CLASS / REMOUNT PVC

After pod was deleted, nfs based pvc cannot be mounted to the pod "applyFSGroup failed for vol".

Workaround: Not having fsGroup field in pod will also skip call to  SetVolumeOwnership function.

remove:

```yaml
...
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000 # remove this field!
...
```

### RANCHER ADD CERTS w/ PRIVATE CA

[rancher-certificate](https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/resources/update-rancher-certificate)

#### CREATE

```bash
kubectl -n cattle-system create secret tls tls-rancher-ingress \
--cert=tls.crt \
--key=tls.key

kubectl -n cattle-system create secret generic tls-ca \
--from-file=cacerts.pem
```

#### HELM VALUES

```yaml
#..
ingress:
  tls:
    source: secret
privateCA: true
```

#### UDPATE/UPGRADE CERTS

```bash
kubectl -n cattle-system create secret generic tls-ca \
--from-file=cacerts.pem

kubectl -n cattle-system create secret generic tls-ca \
--from-file=cacerts.pem \
--dry-run --save-config -o yaml | kubectl apply -f -

kubectl rollout restart deploy/rancher -n cattle-system
```

### GET ALL IMAGES IN CLUSTER

```bash
kubectl get pods --all-namespaces -o jsonpath="{.items[*].spec.containers[*].image}" |\
tr -s '[[:space:]]' '\n' |\
sort |\
uniq -c
```

## TEST REGISTRY SECRETS W/ HELM

```bash
kubectl run helm-pod -it --rm --image alpine/k8s:1.24.15 -- sh

mkdir -p ~/.docker/
cat <<EOF > ~/.docker/config.json
{"auths": #...
EOF

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm pull bitnami/nginx --version 15.1.0
tar xvfz nginx-15.1.0.tgz
yq e -i '.version = "9.9.9"' nginx/Chart.yaml
helm package nginx
helm push nginx-9.9.9.tgz oci://eu.gcr.io/stuttgart-things/
```

## DELETE ALL EVICTED PODS IN ALL NAMESPACES

```bash
kubectl get pods --all-namespaces | grep Evicted | awk '{print $2 " --namespace=" $1}' | xargs kubectl delete pod
```

## WORK W/ OFTEN MANUALY RESTARTED/DELETED PODS FOR DEV/TESTING

```bash
kubectl -n <NAMESPACE> get po | grep <PART-OF-POD-NAME> | awk '{ print $1}'
kubectl -n sweatshop delete po $(kubectl -n sweatshop get po | grep creator | awk '{ print $1}')
kubectl -n sweatshop logs -f $(kubectl -n sweatshop get po | grep creator | awk '{ print $1}')
```

## BUILDAH

BUILD OCI-IMAGE

```bash
buildah --storage-driver=overlay bud --format=oci \
--tls-verify=true --no-cache \
-f ~/projects/github/stuttgart-things/images/sthings-alpine/Dockerfile \
-t scr.app.4sthings.tiab.ssc.sva.de/sthings-alpine/alpine:123
```

## SKOPEO

### INSTALL

```bash
SKOPEO_VERSION=1.12.0
wget https://github.com/lework/skopeo-binary/releases/download/v${SKOPEO_VERSION}/skopeo-linux-amd64
sudo chmod +x skopeo-linux-amd64
sudo mv skopeo-linux-amd64 /usr/bin/skopeo && skopeo --version
```

### COPY IMAGE BETWEEN REGISTRIES (TAG)

* Copy images between registries

```bash
skopeo copy --insecure-policy docker://nginx:1.21
docker://whatever.cloud/gtc1fe/web:1.21
```

### COPY IMAGE BETWEEN REGISTRIES (DIGEST)

* Copy images between registries

```bash
skopeo copy --all --insecure-policy
docker://nginx@sha256:ff2a5d557ca22fa93669f5e70cfbeefda32b98f8fd3d33b38028c582d700f93a \ docker://whatever.cloud/gtc1fe/web@sha256:ff2a5d557ca22fa93669f5e70cfbeefda32b98f8fd3d33b38028c582d700f93a
```

### OVERWRITE ENTRYPOINT OF IMAGE W/ NERDCTL

```bash
nerdctl run -it --entrypoint sh eu.gcr.io/stuttgart-things/stagetime-server:23.1108.1227-0.3.22
```

## CLEANUP W/ NERDCTL

```bash
# STOP AND DELETE ALL RUNNING CONTAINERS
sudo nerdctl stop $(sudo nerdctl ps -a | awk '{ print $1 }' | grep -v CONTAINER); sudo nerdctl rm $(sudo nerdctl ps -a | awk '{ print $1 }' | grep -v CONTAINER)

# CLEAN IMAGES BY ID
sudo nerdctl rmi $(sudo nerdctl images | grep "2 months ago" | awk '{ print $3 }')

# CLEAN IMAGES BY NAME + TAG
sudo nerdctl rmi $(sudo nerdctl images | grep "7 weeks ago" | awk '{ print $1":"$2 }')
```

## CONTAINERD CTR

```bash
# pull image w/ crt
sudo ctr images pull docker.io/library/redis:alpine
# or for rke2 bundled containerd: sudo /var/lib/rancher/rke2/bin/ctr images pull docker.io/library/redis:alpine

# list images
ctr --namespace k8s.io images ls -q
# or for rke2 bundled containerd: sudo /var/lib/rancher/rke2/bin/ctr --address /run/k3s/containerd/containerd.sock --namespace k8s.io container ls

# load/import conatiner image
ctr -n=k8s.io images import <IMAGE_NAME>

 ctr image export <output-filename> <image-name>

```

## INSTALL CONTAINERD

### INSTALL CONTAINERD

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

### INSTALL RUNC

```bash
wget https://github.com/opencontainers/runc/releases/download/v1.1.7/runc.amd64
sudo install -m 755 runc.amd64 /usr/local/sbin/runc
sudo ls /usr/local/sbin/ #check
```

### INSTALL CNI PLUGINS

```bash
wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-amd64-v1.3.0.tgz
sudo mkdir -p /opt/cni/bin
sudo tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.3.0.tgz
```

## RKE2

```bash
# list images
journalctl -u rke2-server | grep Import
```

### IMPORT RKE2 IMAGES INTO CONTAINERD NAMESPACE

```bash
wget https://github.com/rancher/rke2/releases/download/v1.25.7%2Brke2r1/rke2-images-all.linux-amd64.txt
```

```bash
#!/bin/bash

FILES="./rke2-images-all.linux-amd64.txt"

while read image; do

  image=$(echo $image | cut -d'/' -f 3)
  tag=$(echo $image| cut -d':' -f 2)
  imagename=$(echo $image| cut -d':' -f 1)

  echo pulling "$image"

  sudo ctr image pull $image

  echo exporting "$image"

  sudo ctr image export $(echo $image | cut -d'/' -f 2)-$imagename-$tag.tar $image

  echo importing "$image"

  sudo ctr -n=k8s.io image import $(echo $image | cut -d'/' -f 2)-$imagename-$tag.tar

done <${FILES}
```

## CURL/TEST SERVICE INSIDE CLUSTER

```bash
kubectl run curler --image=radial/busyboxplus:curl -i --tty --rm
ping/curl/nslookup <SERVICE_NAME>.<NAMESPACE>.svc.cluster.local
curl elastic-cluster-master.elastic.svc.cluster.local:9200
```

## NAMESPACE STUCK IN DELETION

### OPTION1: DELETE PENDING APISERVICES

```bash
kubectl get apiservice|grep False
kubectl delete APIServices v1alpha1.apps.kio.kasten.io # example
```

### OPTIONW: CHANGE FINALIZER

```bash
kubectl get namespace "<NAMESPACE>" -o json \
  | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" \
  | kubectl replace --raw /api/v1/namespaces/<NAMESPACE>/finalize -f -
```

## DEPLOY INGRESS-NGINX W/ DEFAULT WILDCARD CERT

### CREATE TLS SECRET

```bash
# CMD
kubectl create secret tls tls-wildcard --cert=lab.crt --key=lab.key -n ingress-nginx

# OR AS FILE
---
cat <<EOF > tls-wildcard.yaml
apiVersion: v1
data:
  tls.crt: {{ ssl_cert_crt | b64encode }}
  tls.key: {{ ssl_cert_key | b64encode }}
kind: Secret
metadata:
  name: tls-wildcard
  namespace: ingress-nginx
type: kubernetes.io/tls
EOF

kubectl apply -f tls-wildcard.yaml
```

### DEPLOY

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install my-ingress-nginx ingress-nginx/ingress-nginx --version 4.7.0 \
--set controller.extraArgs.default-ssl-certificate="ingress-nginx/tls-wildcard"
```

## TEST INGRESS-NGINX DEPLOYMENTS

<details><summary><b>wildcard</b></summary>

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: kuard
spec:
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
  selector:
    app: kuard
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kuard
spec:
  selector:
    matchLabels:
      app: kuard
  replicas: 1
  template:
    metadata:
      labels:
        app: kuard
    spec:
      containers:
      - image: gcr.io/kuar-demo/kuard-amd64:1
        imagePullPolicy: Always
        name: kuard
        ports:
        - containerPort: 8080
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: guard-ingress
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - guard.<DOMAIN>
  rules:
  - host: guard.<DOMAIN>
    http:
      paths:
      - path: /
        pathType: ImplementationSpecific
        backend:
          service
            name: kuard
            port:
              number: 80
```

</details>

<details><summary><b>path-based</b></summary>

```yaml
---
kind: Pod
apiVersion: v1
metadata:
  name: apple-app
  labels:
    app: apple
spec:
  containers:
    - name: apple-app
      image: hashicorp/http-echo
      args:
        - "-text=apple"
---
kind: Pod
apiVersion: v1
metadata:
  name: banana-app
  labels:
    app: banana
spec:
  containers:
    - name: banana-app
      image: hashicorp/http-echo
      args:
        - "-text=banana"
---
kind: Service
apiVersion: v1
metadata:
  name: banana-service
spec:
  selector:
    app: banana
  ports:
    - port: 5678 # Default port for image
---
kind: Service
apiVersion: v1
metadata:
  name: apple-service
spec:
  selector:
    app: apple
  ports:
    - port: 5678 # Default port for image
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fruit-ingress
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /apple
        pathType: Prefix
        backend:
          service:
            name: apple-service
            port:
              number: 5678
      - path: /banana
        pathType: Prefix
        backend:
          service:
            name: banana-service
            port:
              number: 5678
```

</details>
