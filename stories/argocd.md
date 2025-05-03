# HOW TO ARGOCD

Goal: Deploy and manage applications using GitOps principles with ArgoCD on KinD clusters.

```bash
Key Features Demonstrated:
✅ GitOps Workflow (Git as source of truth)
✅ Multi-Cluster Management
✅ Automated Sync + Self-Healing
✅ Secure Secrets Handling (bcrypt, cert-manager)
```

## DEPLOYMENT

argocd cluster (control plane + workers) with:
* Custom networking (CNI disabled)
* Ingress-ready nodes
* Persistent storage mounts
* maverick test cluster (for deployment targets)

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

Helmfile-based:
* Installs Cilium (CNI), Ingress-Nginx, and Cert-Manager
* Automated retry logic (helmfile apply/sync)

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
sleep 30 && curl $(hostname -f)
```

</details>

<details><summary>DEPLOY ARGOCD (KIND)</summary>

Customized Deployment:
* Secure admin password (bcrypt-hashed)
* Ingress configured with Let's Encrypt/cert-manager
* Self-signed certs for local development

```bash
# OUTPUT INGRESS DOMAIN
export KUBECONFIG=~/.kube/kind-argocd

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

# REPLACE IP IN KUBECONFIG
sed -i "s|server: https://0\.0\.0\.0:|server: https://$LOCAL_IP:|g" ~/.kube/kind-maverick
kubectl get nodes --kubeconfig ~/.kube/kind-maverick
```

</details>

## MANAGE CLUSTERS

Adding Clusters:
* Register external clusters (argocd cluster add)
* Projects for RBAC (whitelist/blacklist resources)

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

CLUSTER_NAME=maverick
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

VERIFY-STEPS:
* CHECK ARGOCD GUI FOR PROJECT EXISTENCE

FOLLOW-UP-STEPS:
* ADD A PROJECT w/ THE NAME in-cluster (WITH ALL PRIVILEGES) FOR THE LOCAL/ARGOCD CLUSTER
* ADD IN-CLUSTER AND MAVERICK TO A NEWLY CREATED APP PROJECT (WITH ALL PRIVILEGES) WITH THE NAME all-clusters

</details>

## DEPLOY APPLICATIONS

Methods:
* Helm Charts (from repositories like helm.cilium.io)
* Git Repositories (raw manifests or Helm charts in Git)
* Sync Policies:
  * Automated sync with pruning/self-healing
  * Manual sync for control

<details><summary>CREATE HELM BASED APPLICATION</summary>

### DEPLOY CILIUM

```bash
# SET TESTING CLUSTER INFORMATION
CLUSTER_NAME=maverick
export KUBECONFIG=~/.kube/kind-maverick
SERVER_URL=$(awk '/server:/ {print $2}' ${KUBECONFIG})

# CREATE APPLICATION
export KUBECONFIG=~/.kube/kind-argocd

kubectl apply -f - <<EOF
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cilium
  namespace: argocd
spec:
  destination:
    name: ''
    namespace: kube-system
    server: ${SERVER_URL}
  source:
    path: ''
    repoURL: https://helm.cilium.io
    targetRevision: 1.17.2
    chart: cilium
    helm:
      values: |
        autoDirectNodeRoutes: true
        devices:
        - eth0
        - net0
        externalIPs:
          enabled: true
        ipv4NativeRoutingCIDR: 10.244.0.0/16
        k8sServiceHost: maverick-control-plane
        k8sServicePort: 6443
        kubeProxyReplacement: true
        l2announcements:
          enabled: true
          leaseDuration: 3s
          leaseRenewDeadline: 1s
          leaseRetryPeriod: 500ms
        operator:
          replicas: 1
        routingMode: native
  sources: []
  project: ${CLUSTER_NAME}
  syncPolicy:
    syncOptions:
      - CreateNamespace=false
    automated: null
EOF
```

### DEPLOY CERT-MANAGER

```bash
# SET TESTING CLUSTER INFORMATION
CLUSTER_NAME=maverick
export KUBECONFIG=~/.kube/kind-maverick
SERVER_URL=$(awk '/server:/ {print $2}' ${KUBECONFIG})

# CREATE APPLICATION
export KUBECONFIG=~/.kube/kind-argocd

kubectl apply -f - <<EOF
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cert-manager
  namespace: argocd
spec:
  destination:
    name: ''
    namespace: cert-manager
    server: ${SERVER_URL}
  source:
    path: ''
    repoURL: https://charts.jetstack.io
    targetRevision: v1.17.1
    chart: cert-manager
    helm:
      values: |
        crds:
          enabled: true
  sources: []
  project: ${CLUSTER_NAME}
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
    automated:
      prune: true       # Delete resources when removed from Git
      selfHeal: true   # Automatically revert manual changes
      allowEmpty: false # Prevent sync when manifests are empty
EOF
```

#### DEPLOY CLUSTERISSUER

```bash
export KUBECONFIG=~/.kube/kind-maverick

kubectl apply -f - <<EOF
---
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned
spec:
  selfSigned: {}
EOF
```

### DEPLOY INGRESS-NGINX

```bash
# SET TESTING CLUSTER INFORMATION
CLUSTER_NAME=maverick
export KUBECONFIG=~/.kube/kind-maverick
SERVER_URL=$(awk '/server:/ {print $2}' ${KUBECONFIG})

# CREATE APPLICATION
export KUBECONFIG=~/.kube/kind-argocd

kubectl apply -f - <<EOF
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ingress-nginx
  namespace: argocd
spec:
  destination:
    name: ''
    namespace: ingress-nginx
    server: ${SERVER_URL}
  source:
    repoURL: https://kubernetes.github.io/ingress-nginx
    targetRevision: 4.0.13
    chart: ingress-nginx
    helm:
      values: |
        controller:
          replicaCount: 2
          service:
            type: NodePort
            nodePorts:
              http: 30080
              https: 30443
          ingressClassResource:
            name: nginx
            controllerValue: "k8s.io/ingress-nginx"
  project: ${CLUSTER_NAME}
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
    automated:
      prune: true
      selfHeal: true
EOF
```

VERIFY-STEPS:
* CHECK ARGOCD GUI FOR APPLICATION STATE AND SYNC APP MANUALY
* CHECK w/ KUBECONFIG APPLICATION STATE ON ARGOCD CLUSTER (kubectl get application -n argocd)
* CHECK w/ KUBECONFIG APPLICATION STATE ON TESTING CLUSTER (kubectl get po -n vault)

FOLLOW-UP-STEPS:
* DELETE APP WITH GUI
* ADD APP WITH GUI (INSERT MANIFEST), UPDATE SYNC POLICY TO AUOTMATIC
* DEPLOY APP IN-CLUSTER

</details>

<details><summary>PREPARATION/OPTIONAL: ADD EXAMPLE MANIFESTS TO A GITREPO</summary>

PREPARATION-STEPS:
* CREATE PERSONAL GIT REPO (SCM YOUR CHOICE)
* CLONE REPO TO LOCAL

```bash
cd <REPO-DIR>
mkdir nginx

cat <<EOF > nginx/manifests.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 2
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
          image: nginx:latest
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP  # Change to NodePort or LoadBalancer if needed
EOF
```

FOLLOW-UP-STEPS:
* COMMIT FOLDER TO YOUR REPO/BRANCH

</details>

<details><summary>ADD GIT-REPOSIORY TO ARGOCD</summary>

```bash
# CREATE APPLICATION
export KUBECONFIG=~/.kube/kind-argocd

kubectl apply -f - <<EOF
apiVersion: v1
stringData:
  password: "" # BASIC TOKEN IF REPO NOT PUBLIC
  project: maverick # EXAMPLE - CHANGE TO YOURS
  type: git
  url: https://github.com/stuttgart-things/helm.git # EXAMPLE - CHANGE TO YOURS
  username: "" # USERNAME IF REPO NOT PUBLIC
kind: Secret
metadata:
  annotations:
    managed-by: argocd.argoproj.io
  labels:
    argocd.argoproj.io/secret-type: repository
  name: repo-helm  # EXAMPLE - CHANGE TO YOURS
  namespace: argocd
type: Opaque
EOF
```

FOLLOW-UP-STEPS:
* CHECK ON ARGOCD GUI FOR GIT-REPOSITORY

</details>

<details><summary>CREATE GIT/PATH-BASED APPLICATION</summary>

```bash
# CREATE APPLICATION
export KUBECONFIG=~/.kube/kind-argocd

# PLEASE REPLACE THE DUMMY VALUES w/ YOUR REPO/PATH/PROJECT/NAMESPACE

kubectl apply -f - <<EOF
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: deployment-tekton-pipelines # EXAMPLE - CHANGE TO YOURS
  namespace: argocd
spec:
  destination:
    name: ''
    namespace: tekton-pipelines # EXAMPLE - CHANGE TO YOURS
    server: 'https://kubernetes.default.svc' # EXAMPLE - CHANGE TO YOURS
  source:
    path: apps/tekton # EXAMPLE - CHANGE TO YOURS
    repoURL: 'https://github.com/stuttgart-things/tekton.git' # EXAMPLE - CHANGE TO YOURS
    targetRevision: HEAD # EXAMPLE - CHANGE TO YOURS
    directory:
      recurse: true
  sources: []
  project: default # EXAMPLE - CHANGE TO YOURS
  syncPolicy:
    automated:
      prune: true
      selfHeal: false
EOF
```

VERIFY-STEPS:
* CHECK ARGOCD GUI FOR APPLICATION STATE AND SYNC APP MANUALY
* CHECK w/ KUBECONFIG APPLICATION STATE ON ARGOCD CLUSTER (kubectl get application -n argocd)
* CHECK w/ KUBECONFIG APPLICATION STATE ON TESTING CLUSTER (kubectl get po -n <NAMESPACEXY>)

FOLLOW-UP-STEPS:
* UPDATE APP IN GIT AND SEE WHAT HAPPENS :-)

</details>

<details><summary>CREATE GIT/PATH-BASED APPLICATION w/ APPSET FROM PRIVATE REPO</summary>

#### CREATE PRIVATE REPO - PLEASE REPLACE THE DUMMY VALUES w/ YOUR REPO/PATH/PROJECT/NAMESPACE/CREDENTIALS

```bash
export KUBECONFIG=~/.kube/kind-argocd
kubectl apply -f - <<EOF
---
apiVersion: v1
stringData:
  password: ""
  project: default # EXAMPLE - CHANGE TO YOURS
  type: git
  url: https://github.com/stuttgart-things/stuttgart-things.git
  username: ""
kind: Secret
metadata:
  annotations:
    managed-by: argocd.argoproj.io
  labels:
    argocd.argoproj.io/secret-type: repository
  name: stuttgart-things # EXAMPLE - CHANGE TO YOURS
  namespace: argocd
type: Opaque
EOF
```

#### CREATE APPLICATION FOR APPSET

```bash
export KUBECONFIG=~/.kube/kind-argocd
kubectl apply -f - <<EOF
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: apps-configuration
  namespace: argocd
spec:
  destination:
    name: in-cluster # EXAMPLE - CHANGE TO YOURS
    namespace: argocd
  source:
    path: clusters/kind/machinery/apps # EXAMPLE - CHANGE TO YOURS
    repoURL: 'https://github.com/stuttgart-things/stuttgart-things.git'
    targetRevision: HEAD
    directory:
      recurse: true
  sources: []
  project: in-cluster # EXAMPLE - CHANGE TO YOURS
  syncPolicy:
    automated:
      prune: true
      selfHeal: false
EOF
```

#### CREATE APPSET 

```bash
export KUBECONFIG=~/.kube/kind-argocd

cat <<EOF > apps-appset.yaml
---
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: apps
  namespace: argocd
spec:
  goTemplate: true
  goTemplateOptions: ["missingkey=error"]
  generators:
  - list:
      elements:
        - app: crossplane
          project: in-cluster
          namespace: crossplane-system
          targetRevision: 1.19.0
          repoURL: https://charts.crossplane.io/stable
          destination: in-cluster
          appValues: |
            ---
            args:
              - '--debug'
              - '--enable-usages'
              - '--enable-external-secret-stores'
            provider:
              packages:
                - xpkg.upbound.io/crossplane-contrib/provider-helm:v0.20.4
                - xpkg.upbound.io/crossplane-contrib/provider-kubernetes:v0.17.1
  template:
    metadata:
      name: '{{ .app }}-{{ .destination }}'
    spec:
      project: '{{ .project }}'
      source:
        repoURL: '{{ .repoURL }}'
        chart: '{{ .app }}'
        targetRevision: '{{ .targetRevision }}'
        helm:
          releaseName: '{{ .app }}-{{ .project }}'
          values: |
            {{ .appValues }}
          skipCrds: false
      destination:
        name: '{{ .destination }}'
        namespace: '{{ .namespace }}'
      syncPolicy:
        syncOptions:
          - CreateNamespace=true
        automated:
          prune: true
          selfHeal: true
EOF

# COMMIT TO GIT
```

</details>




<!---
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
-->
