# stuttgart-things/docs/kubernetes

## CLUSTER

<details><summary>GATEWAY API (CILIUM)</summary>

```bash
# CHECK IF GATWAY API IS ENABLED
sthings@maverick rke2 → cilium config view | grep enable-gateway-api
enable-gateway-api                                true
enable-gateway-api-alpn                           false
enable-gateway-api-app-protocol                   false
enable-gateway-api-proxy-protocol                 false
enable-gateway-api-secrets-sync                   true

# CHECK IF GATWAY API CRDS ARE INSTALLED
sthings@maverick rke2 → kubectl get crd | grep gateway.networking.k8s.io
backendtlspolicies.gateway.networking.k8s.io   2026-02-15T08:28:50Z
gatewayclasses.gateway.networking.k8s.io       2026-02-15T08:28:50Z
gateways.gateway.networking.k8s.io             2026-02-15T08:28:50Z
grpcroutes.gateway.networking.k8s.io           2026-02-15T08:28:50Z
httproutes.gateway.networking.k8s.io           2026-02-15T08:28:50Z
referencegrants.gateway.networking.k8s.io      2026-02-15T08:28:51Z

# OPTIONAL: ADD HOSST ENTRY
echo "10.31.103.16 nginx.vre2.sthings.io" | sudo tee -a /etc/hosts

# CREATE WILDCARD CERT
kubectl apply -f - <<'EOF'
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: wildcard-whatever-tls
  namespace: default
spec:
  commonName: "*.whatever.sthings.example.com"
  dnsNames:
    - "*.whatever.sthings.example.com"
    - whatever.sthings.example.com
  issuerRef:
    kind: ClusterIssuer
    name: cluster-issuer-approle
  secretName: wildcard-whatever-tls
EOF

# CREATE GATEWAY + TEST NGINX
kubectl apply -f - <<'EOF'
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: whatever-gateway
  namespace: default
spec:
  gatewayClassName: cilium
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      hostname: "*.whatever.sthings.example.com"
      tls:
        mode: Terminate
        certificateRefs:
          - kind: Secret
            name: wildcard-whatever-tls
      allowedRoutes:
        namespaces:
          from: Same
    - name: http
      protocol: HTTP
      port: 80
      hostname: "*.whatever.sthings.example.com"
      allowedRoutes:
        namespaces:
          from: Same
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:alpine
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx
  namespace: default
spec:
  selector:
    app: nginx
  ports:
    - port: 80
      targetPort: 80
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: nginx-route
  namespace: default
spec:
  parentRefs:
    - name: whatever-gateway
      sectionName: https
  hostnames:
    - nginx.whatever.sthings.example.com
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /
      backendRefs:
        - name: nginx
          port: 80
EOF

#After applying, check:
kubectl get gateway whatever-gateway
kubectl get httproute nginx-route
kubectl get svc cilium-gateway-whatever-gateway

# CHECK ROUTE/ENDPOINT
curl -sk https://nginx.whatever.sthings.example.com/
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

</details>


<details><summary>CLOUD-INIT RKE2 CLUSTER</summary>

```bash
#cloud-config
package_update: true
package_upgrade: true
packages:
  - cloud-guest-utils
  - lvm2
runcmd:
  # Fix GPT and grow partition 3 (where LVM PV actually is)
  - growpart /dev/sda 3
  # Resize the LVM physical volume
  - pvresize /dev/sda3
  # Extend LV for /var with all free space
  - lvextend -l +100%FREE /dev/vg0/var
  # Resize XFS filesystem
  - xfs_growfs /var
  # Verify
  - df -h /var
  - vgs vg0
```

</details>


<details><summary>GOCV</summary>

### UPLOAD OVA TO VCENTER

```bash
wget https://cloud-images.ubuntu.com/plucky/current/plucky-server-cloudimg-amd64.ova

export GOVC_URL="https://${VCENTER_USER}:${VCENTER_PASSWORD}@${VCENTER_FQDN}/sdk"

govc import.ova -folder /LabUL/vm/stuttgart-things/vm-templates \
-ds "ESX03-Local" \
-pool "/LabUL/host/Cluster-V6.7/Resources" \
./plucky-server-cloudimg-amd64.ova
```

</details>

<details><summary>TALOS (VMWARE)</summary>

[TALOS DOCS (VMWARE)
](https://www.talos.dev/v1.9/talos-guides/install/virtualized-platforms/vmware/)

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
sudo mv k3d-linux-amd64 /usr/bin/k3d
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

# CREATE STANDALONE KUBECONFIG
k3d kubeconfig get dev > ~/.kube/k3d-dev

# MERGE KUBECONFIG INTO EXISTING ONES
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

<details><summary>K3S IMPORT IMAGE</summary>

```bash
docker save docker.io/minio/kes:2025-03-12T09-35-18Z -o kes.tar
sudo k3s ctr images import kes.tar

#containers:
#  - name: kes
#    image: docker.io/minio/kes:2025-03-12T09-35-18Z
#    imagePullPolicy: Never
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

