# ARGOCD

## DEPLOYMENT

<details><summary>DEPLOY ARGOCD KIND-TESTING CLUSTER (KIND)</summary>

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
    image: kindest/node:{{ .k8sVersion}}
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
    image: kindest/node:{{ .k8sVersion}}
    extraMounts:
      - hostPath: /mnt/data-node1  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
  - role: worker
    image: kindest/node:{{ .k8sVersion}}
    extraMounts:
      - hostPath: /mnt/data-node2  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
  - role: worker
    image: kindest/node:{{ .k8sVersion}}
    extraMounts:
      - hostPath: /mnt/data-node3  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
EOF

mkdir -p ~/.kube || true
kind create cluster --name maverick --config argocd-cluster.yaml --kubeconfig ~/.kube/argocd
```

</details>

<details><summary>CREATE LOCAL TEST CLUSTER</summary>

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
kind create cluster --name maverick --config test-cluster.yaml --kubeconfig ~/.kube/maverick
```

</details>

## MANAGE CLUSTERS

<details><summary>ADD CLUSTER w/ CLI</summary>

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

## APPLICATIONS

<details><summary>GIT-SOURCE</summary>

```bash

```

</details>

<details><summary>HELM-REPO-SOURCE</summary>

```bash

```

</details>
