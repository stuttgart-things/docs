# ARGOCD

## DEPLOYMENT

<details><summary>CREATE ARGOCD KIND TESTING CLUSTER (KIND)</summary>

```bash
cat <<EOF > argocd-cluster.yaml
---
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  disableDefaultCNI: true
  kubeProxyMode: none
nodes:
  - role: control-plane
    image: kindest/node:v1.32.3
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - containerPort: 80
        hostPort: 80
        protocol: TCP
      - containerPort: 443
        hostPort: 443
        protocol: TCP
  - role: worker
    image: kindest/node:v1.32.3
    extraMounts:
      - hostPath: /mnt/data-node1  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
  - role: worker
    image: kindest/node:v1.32.3
    extraMounts:
      - hostPath: /mnt/data-node2  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
  - role: worker
    image: kindest/node:v1.32.3
    extraMounts:
      - hostPath: /mnt/data-node3  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
EOF

mkdir -p ~/.kube || true
sudo systemctl restart containerd
kind create cluster --name argocd --config argocd-cluster.yaml --kubeconfig ~/.kube/kind-argocd
```

</details>

<details><summary>DEPLOY CLUSTER-INFRA (KIND)</summary>

```bash
cat <<EOF > cluster-infra.yaml
---
helmDefaults:
  verify: false
  wait: true
  timeout: 600
  recreatePods: false
  force: true

helmfiles:
  - path: git::https://github.com/stuttgart-things/helm.git@infra/cilium.yaml
    values:
      - config: kind
      - configureLB: true
      - ipRangeStart: 172.18.250.0
      - ipRangeEnd: 172.18.250.50
      - clusterName: argocd

  - path: git::https://github.com/stuttgart-things/helm.git@infra/ingress-nginx.yaml
    values:
      - enableHostPort: true

  - path: git::https://github.com/stuttgart-things/helm.git@infra/cert-manager.yaml
    values:
      - config: selfsigned
EOF

export KUBECONFIG=~/.kube/kind-argocd
export HELMFILE_CACHE_HOME=/tmp/helmfile-cacher/argocd

helmfile init --force

for cmd in apply sync; do
  for i in {1..8}; do
    helmfile -f cluster-infra.yaml $cmd && break
    [ $i -eq 8 ] && exit 1
    sleep 15
  done
done

# CHECK FOR NGINX (INGRESS) NOT FOUND PAGE
curl $(hostname -f)
```

</details>

<details><summary>DEPLOY ARGOCD (KIND)</summary>

```bash
# OUTPUT INGRESS DOMAIN
DOMAIN=$(echo $(kubectl get nodes -o json | jq -r '.items[] | select(.metadata.labels."ingress-ready" == "true") | .status.addresses[] | select(.type == "InternalIP") | .address').nip.io)
echo ${DOMAIN}

# GENERATE PASSWORD (CHANGE Test2025! IF YOU LIKE)
sudo apt -y install apache2-utils

# GEN PW HASES
adminPassword=$(htpasswd -nbBC 10 "" 'Test2025!' | tr -d ':\n')
adminPasswordMTime=$(echo $(date +%FT%T%Z))

cat <<EOF > argocd.yaml
---
helmfiles:
  - path: git::https://github.com/stuttgart-things/helm.git@apps/argocd.yaml
    values:
      - namespace: argocd
      - clusterIssuer: selfsigned
      - issuerKind: cluster-issuer
      - hostname: argocd
      - domain: ${DOMAIN}
      - ingressClassName: nginx
      - adminPassword: ${adminPassword}
      - adminPasswordMTime: ${adminPasswordMTime}
      - enableAvp: false
EOF

export KUBECONFIG=~/.kube/kind-argocd
helmfile template -f argocd.yaml # RENDER ONLY
helmfile apply -f argocd.yaml # APPLY HELMFILE
until kubectl wait --for=condition=Ready --all pods -n argocd --timeout=0s >/dev/null 2>&1; do gum spin --title "Waiting for ArgoCD pods..." -- sleep 5; done

kubectl get po -n argocd
kubectl get ing -n argocd

# ADD LOCALHOST ENTRY
echo ADD THIS TO YOUR LAPTOPS HOSTS FILE!
echo $(hostname -I | awk '{print $1}') argocd.${DOMAIN}
```

</details>

<details><summary>CREATE LOCAL TEST CLUSTER (ANOTHER KIND CLUSTER)</summary>

```bash
LOCAL_IP=$(hostname -I | awk '{print $1}')
HOST_PORT=$(echo $(( RANDOM % (36443 - 30000 + 1) + 30000 )))

cat <<EOF > test-cluster.yaml
---
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  apiServerAddress: ${LOCAL_IP}
  disableDefaultCNI: true
  kubeProxyMode: none
nodes:
  - role: control-plane
    image: kindest/node:v1.32.3
    extraPortMappings:
      - containerPort: 6443
        hostPort: ${HOST_PORT}
        protocol: TCP
  - role: worker
    image: kindest/node:v1.32.3
    extraMounts:
      - hostPath: /mnt/data-node1  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
EOF

sudo sysctl fs.inotify.max_user_watches=524288
sudo sysctl fs.inotify.max_user_instances=512
kind create cluster --name maverick --config test-cluster.yaml --kubeconfig ~/.kube/kind-maverick
kubectl get nodes --kubeconfig ~/.kube/kind-maverick
```

</details>

## MANAGE CLUSTERS

<details><summary>ADD TEST CLUSTER w/ CLI</summary>

### LOGIN w/ CLI

```bash
export KUBECONFIG=~/.kube/kind-argocd
DOMAIN=$(echo $(kubectl get nodes -o json | jq -r '.items[] | select(.metadata.labels."ingress-ready" == "true") | .status.addresses[] | select(.type == "InternalIP") | .address').nip.io)
argocd login argocd.${DOMAIN}:443 --insecure
```

### ADD TEST CLUSTER

```bash
export KUBECONFIG=~/.kube/kind-maverick
argocd cluster add $(kubectl config current-context) --name maverick --grpc-web
```

</details>


<details><summary>CREATE APP PROJECTS</summary>

Needed for:
* Team Isolation – Different teams (frontend/backend) have their own projects.
* Security & Compliance – Restrict deployments to certain namespaces/clusters.
* Deployment Scheduling – Block deployments during maintenance windows.
* Multi-Cluster Management – Deploy the same app to different regions.

### PROJECT FOR TEST CLUSTER (ALL PRIVILIDGES)

```bash
# CREATE APP PROJECT FOR TEST CLUSTER

CLUSTER_NAME=MAVERICK
export KUBECONFIG=~/.kube/kind-maverick
SERVER_URL=$(awk '/server:/ {print $2}' ${KUBECONFIG})

cat <<EOF > test-cluster-project.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: ${CLUSTER_NAME}
  namespace: argocd
spec:
  clusterResourceBlacklist:
    - group: ""
      kind: ""
  clusterResourceWhitelist:
    - group: '*'
      kind: '*'
  description: ${CLUSTER_NAME} cluster
  destinations:
    - name: ${CLUSTER_NAME}
      namespace: '*'
      server: ${SERVER_URL}
  namespaceResourceBlacklist:
    - group: ""
      kind: ""
  namespaceResourceWhitelist:
    - group: '*'
      kind: '*'
  sourceRepos:
    - '*'
EOF

# APPLY TO ARGOCD
export KUBECONFIG=~/.kube/kind-argocd
kubectl apply -f test-cluster-project.yaml
```

</details>

<details><summary>CREATE HELM BASED APPLICATION</summary>

```bash
# SET TESTING CLUSTER INFORMATION
CLUSTER_NAME=MAVERICK
export KUBECONFIG=~/.kube/kind-maverick
SERVER_URL=$(awk '/server:/ {print $2}' ${KUBECONFIG})

# CREATE APPLICATION
export KUBECONFIG=~/.kube/kind-argocd
kubectl apply -f - <<EOF
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: vault
  namespace: argocd
spec:
  destination:
    name: ''
    namespace: vault
    server: ${SERVER_URL}
  source:
    path: ''
    repoURL: https://helm.releases.hashicorp.com
    targetRevision: 0.25.0
    chart: vault
    helm:
      values: |
        injector:
          enabled: false
        server:
          enabled: true
        csi:
          enabled: true
  sources: []
  project: ${CLUSTER_NAME}
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
    automated: null
EOF
```

VERIFY-SETPS:
* CHECK ARGOCD GUI FOR APPLICATION STATE AND SYNC APP MANUALY
* CHECK w/ KUBECONFIG APPLICATION STATE ON ARGOCD CLUSTER (kubectl get application -n argocd)
* CHECK w/ KUBECONFIG APPLICATION STATE ON TESTING CLUSTER (kubectl get po -n vault)

FOLLOWOING STEPS-SETPS:
* DELETE APP WITH GUI
* ADD APP WITH GUI (INSERT MANIFEST), UPDATE SYNC POLICY TO AUOTMATIC

</details>



<details><summary>ADD GIT REPOSIORY</summary>

```bash

```

</details>







<details><summary>PROJECTS</summary>

```bash

```

</details>



<details><summary>ADD HELM REPOSIORIES</summary>

```bash

```

</details>

## APPLICATIONS

<details><summary>GIT-SOURCE</summary>

```bash

```

</details>

<details><summary>HELM-REPO-SOURCE</summary>

```bash

```

</details>

<details><summary>KUSTOMIZE</summary>

```bash

```

</details>
