# stuttgart-things/docs/kubernetes

## CLUSTER

<details><summary>TALOS (VMWARE)</summary>

[TALOS DOCS (VMWARE)
](https://www.talos.dev/v1.9/talos-guides/install/virtualized-platforms/vmware/)

### UPLOAD OVA TO VCENTER

```bash
# SET GOVC VARS
export GOVC_INSECURE='TRUE'
export GOVC_URL='https://<USER>:<PW>@10.31.101.51/sdk'
export GOVC_DATACENTER=LabWhatever
export CLUSTER_NAME=talos1
export GOVC_DATASTORE=DD1

# DOWNLOAD TALOS VMWARE SCRIPT
curl -fsSL "https://raw.githubusercontent.com/siderolabs/talos/master/website/content/v1.9/talos-guides/install/virtualized-platforms/vmware/vmware.sh" | sed s/latest/v1.9.2/ > vmware.sh

# UPLOAD OVA
export CLUSTER_NAME=talos1
chmod +x ./vmware.sh
./vmware.sh upload_ova
```

</details>


<details><summary>K3D</summary>

#### INSTALL K3D

```bash
K3D_VERSION=v5.8.3
wget https://github.com/k3d-io/k3d/releases/download/${K3D_VERSION}/k3d-linux-amd64
sudo mv /usr/bin/k3d-linux-amd64 /usr/bin/k3d
sudo chmod +x /usr/bin/k3d
```

### CREATE (EXAMPLE) CLUSTER

```bash
CLUSTER_NAME=dev
cat <<EOF > k3d-${CLUSTER_NAME}.yaml
apiVersion: k3d.io/v1alpha5
kind: Simple
metadata:
  name: ${CLUSTER_NAME}
servers: 1
agents: 2
ports:
  - port: 80:80   # Expose HTTP
    nodeFilters:
      - loadbalancer
  - port: 443:443 # Expose HTTPS
    nodeFilters:
      - loadbalancer
options:
  k3d:
    wait: true
  k3s:
    extraArgs:
      - arg: "--disable=traefik"   # Disable default Traefik Ingress
        nodeFilters:
          - server:0
volumes:
  - volume: /etc/rancher/k3s
    nodeFilters:
      - server:0
EOF
k3d cluster create --config k3d-${CLUSTER_NAME}.yaml
kubectl cluster-info
k3d kubeconfig merge k3d-${CLUSTER_NAME} --kubeconfig-switch-context
kubectl config use-context k3d-${CLUSTER_NAME} && kubectl get nodes
```

#### CONFIGURE METALLB

```bash
CLUSTER_NAME=dev
docker network inspect k3d-${CLUSTER_NAME} | grep Subnet
# e.g. 172.19.0.0/16 = 172.19.255.200-172.19.255.250
IP_RANGE=172.19.255.200-172.19.255.250

kubectl apply -f kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/main/config/manifests/metallb-native.yaml

kubectl apply -f - <<EOF
---
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: my-ip-pool
  namespace: metallb-system
spec:
  addresses:
    - ${IP_RANGE}
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: my-l2-advertisement
  namespace: metallb-system
EOF
```

#### TEST/CONFIGURE LOADBALANCING

```bash
kubectl create deployment nginx --image=nginx
kubectl expose deployment nginx --port=80 --type=LoadBalancer
kubectl get svc nginx

# LOCAL
curl ${EXTERNAL_IP_OF_DOCKER_NETWORK} # e.g. 172.19.255.200
# REMOTE (e.g. VM) - Forward traffic from the VM's external IP to the internal MetalLB IP (172.18.255.200):
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 172.18.255.200:80
sudo iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 172.18.255.200:443
curl ${EXTERNAL_IP_OF_VM} # e.g. 10.31.103.41 from outside
```

</details>

## CERTIFICATES

<details><summary>CERT MANAGER + DEFAULT CERT INGRESS-NGINX</summary>

GENERATE ROOT CERTIFICATE

```bash
# CREATE A FOLDER TO STORE CERTIFICATE FILES
mkdir -p .ssl
# GENERATE AN RSA KEY
openssl genrsa -out .ssl/root-ca-key.pem 2048
# GENERATE ROOT CERTIFICATE
openssl req -x509 -new -nodes -key .ssl/root-ca-key.pem \
  -days 3650 -sha256 -out .ssl/root-ca.pem -subj "/CN=kube-ca"
```

DEPLOY CERT-MANAGER

```bash
helm upgrade --install --wait --timeout 15m \
  --namespace cert-manager --create-namespace \
  --repo https://charts.jetstack.io cert-manager cert-manager \
  --values - <<EOF
installCRDs: true
EOF
```

CREATE ROOT CERTIFICATE SECRET

```bash
kubectl create secret tls -n cert-manager root-ca \
  --cert=.ssl/root-ca.pem \
  --key=.ssl/root-ca-key.pem
```

CREATE CLUSTER ISSUER

```bash
kubectl apply -n cert-manager -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: ca-issuer
spec:
  ca:
    secretName: root-ca
EOF
```

CREATE INGRESS CERT

```bash
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: default-ssl-certificate-tls
  namespace: ingress-nginx
spec:
  dnsNames:
  - hello.server.com
  issuerRef:
    group: cert-manager.io
    kind: ClusterIssuer
    name: ca-issuer
  secretName: default-ssl-certificate-tls
  usages:
  - digital signature
  - key encipherment
EOF
```

UPDATE INGRESS NGINX DEPLOYMENT ARGS

```
spec:
  containers:
  - args:
    - --default-ssl-certificate=ingress-nginx/default-ssl-certificate-tls
```

+ add root-ca.pem to your system trust store

</details>

## KUBECTL

<details><summary>FORCE DELETE POD</summary>

```bash
# E.G. INFLUXDB (STUCK IN DELETING PHASE)
kubectl delete po influxdb-influxdb2-0 --force -n influxdb
```

</details>

<details><summary>NGINX INGRESS RETURNS 413 ENTITY TOO LARGE</summary>

```yaml
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: cs-ingress
  annotations:
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/use-regex: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: 16m
```

</details>


<details><summary>PORTFORWARDING</summary>

```bash
# CHANGE storageclass.kubernetes.io/is-default-class to: "false"
kubectl edit configmap longhorn-storageclass -n longhorn-system
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

<details><summary>DELETE ALL EVICTED PODS IN ALL NAMESPACES</summary>

```bash
kubectl get pods --all-namespaces | grep Evicted | awk '{print $2 " --namespace=" $1}' | xargs kubectl delete pod
```

</details>

<details><summary>WORK W/ OFTEN MANUALY RESTARTED/DELETED PODS FOR DEV/TESTING</summary>

```bash
kubectl -n <NAMESPACE> get po | grep <PART-OF-POD-NAME> | awk '{ print $1}'
kubectl -n sweatshop delete po $(kubectl -n sweatshop get po | grep creator | awk '{ print $1}')
kubectl -n sweatshop logs -f $(kubectl -n sweatshop get po | grep creator | awk '{ print $1}')
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

<details><summary>GET ALL IMAGES IN CLUSTER</summary>

```bash
kubectl get pods --all-namespaces -o jsonpath="{.items[*].spec.containers[*].image}" |\
tr -s '[[:space:]]' '\n' |\
sort |\
uniq -c
```

</details>

<details><summary>NFS STORAGE CLASS / REMOUNT PVC</summary>

After pod was deleted, nfs based pvc cannot be mounted to the pod "applyFSGroup failed for vol".

Workaround: Not having fsGroup field in pod will also skip call to SetVolumeOwnership function.

remove:

```yaml
#...
securityContext:
  runAsUser: 1000
  runAsGroup: 3000
  fsGroup: 2000 # remove this field!
#...
```

</details>

<details><summary>COPY FILE FROM POD TO FILESYSTEM</summary>

```bash
# EXAMPLE COPY
kubectl -n crossplane-system cp provider-terraform-e816b322200e-7564f79bc4-2ggvn:/etc/ssl/certs/ca-certificates.crt ./ca-certificates.crt
```

</details>

<details><summary>DELETE NAMESPACE STUCKING IN DELETION</summary>

```bash
# OPTION 1
NAMESPACE=crossplane-system # EXAMPLE
kubectl get namespace ${NAMESPACE} -o json \
  | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" \
  | kubectl replace --raw /api/v1/namespaces/${NAMESPACE}/finalize -f -
```

```bash
# OPTION 2
kubectl get apiservice|grep False
kubectl delete APIServices v1alpha1.apps.kio.kasten.io # EXAMPLE
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

## CLI

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

## MICROSERVICES

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

<details><summary>GOLDILOCKS, VPA + PROMETHEUS</summary>

## DEPLOY VPA

```bash
kubectl create ns monitoring
helm repo add fairwinds-stable https://charts.fairwinds.com/stable && helm repo update
helm upgrade --install vpa fairwinds-stable/vpa -n monitoring  --version 3.0.2 --create-namespace
helm -n monitoring test vpa
```

## FORKED GIT-REPOSITORY: FOR RKE CLUSTERS (at least for =<52.1.0)

```bash
git clone https://github.com/mohamadkhani/helm-charts.git
cd helm-charts/kube-prometheus-stack && helm dep update
```

## HELM REPO: NON RKE/RANCHER K8S

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

## CREATE TLS CERTIFICATE

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

## CREATE VALUES FILE

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

## DEPLOY KUBE-PROMETHEUS-STACK

```bash
helm upgrade --install kube-prometheus-stack . --values values.yaml --version 52.1.0 --namespace monitoring --create-namespace
# OR W/ HELM REPOSITORY
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack --values values.yaml --version 52.1.0 --namespace monitoring --create-namespace
```

## DEPLOY GOLDILOCKS

```bash
helm repo add fairwinds-stable https://charts.fairwinds.com/stable && helm repo update
helm upgrade --install goldilocks --namespace monitoring fairwinds-stable/goldilocks --version 8.0.0 --create-namespace
```

## LABEL NAMESPACE W/ GOLDILOCKS

```bash
kubectl label ns velero goldilocks.fairwinds.com/enabled=true
```

</details>

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

## K3S

<details><summary><b>INSTALLATION</b></summary>

```bash
cat <<EOF > ~/k3s.yaml
flannel-backend: "none"
disable-kube-proxy: true
disable-network-policy: true
cluster-init: true
disable:
  - servicelb
  - traefik
EOF

curl -sfL https://get.k3s.io | sh -s - --config=$HOME/k3s.yaml
```

</details>

<details><summary><b>GET KUBECONFIG</b></summary>

```bash
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl  get nodes
```

</details>

<details><summary><b>INSTALL CILIUM CLI</b></summary>

```bash
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz
```

</details>

<details><summary><b>INSTALL CILIUM ON CLUSTER</b></summary>

```bash
API_SERVER_IP=10.31.102.162 # <IP>
API_SERVER_PORT=6443 # <PORT>
cilium install \
  --set k8sServiceHost=${API_SERVER_IP} \
  --set k8sServicePort=${API_SERVER_PORT} \
  --set kubeProxyReplacement=true \
  --helm-set=operator.replicas=1 # FOR SINGLE NODE CLUSTER

cilium status --wait
```

</details>

<details><summary><b>INSTALL INGRESS NGINX (HOSTNETWORK - NOT LB)</b></summary>

```bash
helm upgrade --install my-ingress-nginx ingress-nginx/ingress-nginx --version 4.11.2 --set controller.hostNetwork=true -n ingress-nginx --create-namespace
```

</details>


<details><summary><b>CERT-MANAGER SELF SIGNED</b></summary>

```bash
helm repo add cert-manager https://charts.jetstack.io
helm upgrade --install cert-manager cert-manager/cert-manager --version 1.16.0 --set installCRDs=true -n cert-manager --create-namespace
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
EOF

cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: test-ca
spec:
  isCA: true
  commonName: test-ca
  subject:
    organizations:
      - stuttgart-things
    organizationalUnits:
      - Widgets
  secretName: test-ca-secret
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: selfsigned-issuer
    kind: Issuer
    group: cert-manager.io
EOF

cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: test-ca-issuer
spec:
  ca:
    secretName: test-ca-secret
EOF

cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: test-server
spec:
  secretName: test-server-tls
  isCA: false
  usages:
    - server auth
    - client auth
  dnsNames:
  - "michigan.labul.sva.de"
  - "test-server"
  issuerRef:
    name: test-ca-issuer
EOF
```
</details>


## LB-IPAM

```bash
cat <<EOF | kubectl apply -f -
apiVersion: "cilium.io/v2alpha1"
kind: CiliumLoadBalancerIPPool
metadata:
  name: "first-pool"
spec:
  blocks:
    - start: "10.31.102.18"
      stop: "10.31.102.19"
EOF
```

```bash
cat <<EOF > ~/cilium-config.yaml
k8sServiceHost: "10.31.102.162" # <IP>
k8sServicePort: "6443" # <PORT>
kubeProxyReplacement: true
l2announcements:
  enabled: true

externalIPs:
  enabled: true

operator:
  replicas: 1  # Uncomment this if you only have one node
  rollOutPods: true
  rollOutCiliumPods: true

k8sClientRateLimit:
  qps: 50
  burst: 200

ingressController:
  enabled: true
  default: true
  loadbalancerMode: shared
  service:
    annotations:
      io.cilium/lb-ipam-ips: 10.31.102.18
EOF

cilium upgrade -f ~/cilium-config.yaml
cilium connectivity test
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cilium.io/v2alpha1
kind: CiliumL2AnnouncementPolicy
metadata:
  name: default-l2-announcement-policy
  namespace: kube-system
spec:
  externalIPs: true
  loadBalancerIPs: true
EOF
```

<details><summary><b>UNISTALLATION</b></summary>

```bash
/usr/local/bin/k3s-uninstall.sh
```

</details>



```bash


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
