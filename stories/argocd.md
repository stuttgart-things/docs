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
kind create cluster --name argocd --config argocd-cluster.yaml --kubeconfig ~/.kube/argocd


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
      - version: 1.17.1
      - config: kind
      - ipRangeStart: 172.18.250.0
      - ipRangeEnd: 172.18.250.50
      - clusterName: {{ .clusterName }}

  - path: git::https://github.com/stuttgart-things/helm.git@infra/ingress-nginx.yaml
    values:
      - enableHostPort: true
      - version: 4.12.0

  - path: git::https://github.com/stuttgart-things/helm.git@infra/cert-manager.yaml
    values:
      - version: v1.17.1
      - config: selfsigned
EOF

helmfile apply -f cluster-infra.yaml || true
helmfile sync -f cluster-infra.yaml
```

</details>

<details><summary>DEPLOY ARGOCD (KIND)</summary>

```bash
# OUTPUT INGRESS DOMAIN
DOMAIN=$(echo *.$(kubectl get nodes -o json | jq -r '.items[] | select(.metadata.labels."ingress-ready" == "true") | .status.addresses[] | select(.type == "InternalIP") | .address').nip.io)

# GENERATE PASSWORD (CHANGE Test2025! IF YOU LIKE)
sudo apt -y install apache2-utils
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

helmfile template -f argocd.yaml # RENDER ONLY
helmfile apply -f argocd.yaml # APPLY HELMFILE
```

</details>

<details><summary>CREATE LOCAL TEST CLUSTER (ANOTHER KIND CLUSTER)</summary>

```bash
LOCAL_IP=$(hostname -I | awk '{print $1}')
HOST_PORT=$(echo $(( RANDOM % (36443 - 30000 + 1) + 30000 )))

cat <<EOF > /tmp/test-cluster.yaml
---
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  apiServerAddress: ${LOCAL_IP}
  disableDefaultCNI: true
  kubeProxyMode: none
nodes:
  - role: control-plane
    image: kindest/node:v1.32.2
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - containerPort: 6443
        hostPort: ${HOST_PORT}
        protocol: TCP
  - role: worker
    image: kindest/node:v1.32.2
    extraMounts:
      - hostPath: /mnt/data-node1  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
EOF

mkdir -p ~/.kube || true
kind create cluster --name maverick --config /tmp/test-cluster.yaml --kubeconfig ~/.kube/kind-maverick
```

</details>

## MANAGE CLUSTERS

<details><summary>ADD CLUSTER w/ CLI</summary>

```bash

```

</details>


<details><summary>CREATE PROJECTS</summary>

Needed for:
* Team Isolation – Different teams (frontend/backend) have their own projects.
* Security & Compliance – Restrict deployments to certain namespaces/clusters.
* Deployment Scheduling – Block deployments during maintenance windows.
* Multi-Cluster Management – Deploy the same app to different regions.

```bash

```

</details>








<details><summary>ADD CLUSTER w/ MANIFEST</summary>

```bash

```

</details>

<details><summary>PROJECTS</summary>

```bash

```

</details>

<details><summary>ADD GIT REPOSIORIES</summary>

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
