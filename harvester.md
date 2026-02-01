# HARVESTER

<details>
  <summary>Fetch Harvester Kubeconfig</summary>

```bash
ssh rancher@192.168.1.50 "sudo cat /etc/rancher/rke2/rke2.yaml" > ./harvester.yaml
yq -i '.clusters[].cluster.server = "https://192.168.1.50:6443"' ./harvester.yaml
yq '.clusters[].cluster.server' ./harvester.yaml
kubectl get nodes --kubeconfig ./harvester.yaml
```

</details>


<details>
  <summary>ReplicaSchedulingFailure Single-Node Harvester Cluster</summary>
  
You have a single-node Harvester cluster (sthings)
Longhorn is configured for 3 replicas per volume
Only 1 replica can run because Longhorn's anti-affinity prevents multiple replicas on the same node
Status: ReplicaSchedulingFailure: precheck new replica failed

Why this happens:
Longhorn's default configuration assumes multi-node clusters for data redundancy. With one node, it can't satisfy the "3 replicas on different nodes" requirement.
Solutions:

```bash
For existing volumes
kubectl --kubeconfig ~/.kube/harvester patch volume pvc-2ae20462-92b3-4ce2-93f5-8d90812b03bb \
  -n longhorn-system --type=merge -p '{"spec":{"numberOfReplicas":1}}'

kubectl --kubeconfig ~/.kube/harvester patch volume pvc-5626539c-5b15-4b9c-8bf9-cda3625887a4 \
  -n longhorn-system --type=merge -p '{"spec":{"numberOfReplicas":1}}'

# Set global default for future volumes
kubectl --kubeconfig ~/.kube/harvester patch settings.longhorn.io default-replica-count \
  -n longhorn-system --type=merge -p '{"value":"1"}'
```

</details>



