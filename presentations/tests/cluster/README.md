# SLIDES DEMO CLUSTER

<details><summary>CREATE CLUSTER (KIND)</summary>

```bash
kind create cluster \
--config slides-cluster.yaml \
--kubeconfig ~/.kube/kind-slides
```

</details>

<details><summary>DEPLOY CLUSTER-INFRA</summary>

```bash
export KUBECONFIG=~/.kube/kind-slides
export HELMFILE_CACHE_HOME=/tmp/helmfile-cache

helmfile init --force

for cmd in apply sync; do
  for i in {1..8}; do
    helmfile -f cluster-infra.yaml $cmd && break
    [ $i -eq 8 ] && exit 1
    sleep 15
  done
done
```

</details>

<details><summary>GET DOMAIN</summary>

```bash
DOMAIN=$(echo $(kubectl get nodes -o json | jq -r '.items[] | select(.metadata.labels."ingress-ready" == "true") | .status.addresses[] | select(.type == "InternalIP") | .address').nip.io)
echo slides.${DOMAIN}
```

</details>
