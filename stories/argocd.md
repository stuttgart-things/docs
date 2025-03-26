# ARGOCD

## DEPLOYMENT

<details><summary>DEPLOY w/ HELMFILE</summary>

```bash

```

</details>

<details><summary>CREATE LOCAL TEST CLUSTER</summary>

```bash
LOCAL_IP=$(hostname -I | awk '{print $1}')

cat <<EOF > kind-cluster.yaml
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
        hostPort: 36443
        protocol: TCP
  - role: worker
    image: kindest/node:v1.32.2
    extraMounts:
      - hostPath: /mnt/data-node1  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
EOF

mkdir -p ~/.kube || true
kind create cluster --name maverick --config kind-cluster.yaml --kubeconfig ~/.kube/maverick
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
