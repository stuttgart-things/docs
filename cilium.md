# stuttgart-things/docs/cilium

NOT FINISHED!!!!
Cilium 1.14.0 is compatible with k8s 1.17.x or older but not newer

It is important that the cluster does not have a kube-proxy installed

## K8s Cluster

Install cluster /w kudeadm without kube-proxy:

```bash
kubeadm init --skip-phases=addon/kube-proxy
```

Install cluster /w rke2 without kube-proxy:

Configure rke2:

```yaml
# /etc/rancher/rke2/config.yaml
---
disable:
  - rke2-ingress-nginx
cni: cilium
disable-kube-proxy: true
```

Configure cilium rke2 manifest:

```yaml
# /var/lib/rancher/rke2/server/manifests/rke2-cilium-config.yaml
---
apiVersion: helm.cattle.io/v1
kind: HelmChartConfig
metadata:
  name: rke2-cilium
  namespace: kube-system
spec:
  valuesContent: |-
    bgp:
      enabled: false
    hubble:
      enabled: true
      relay:
        enabled: true
      ui:
        enabled: true
    ingressController:
      enabled: true
    k8sServiceHost: 127.0.0.1 # for HA rke2 clusters use k8s HA API hostname
    k8sServicePort: 6443
    kubeProxyReplacement: true
    l2announcements:
      enabled: true
```

## Install Cilium /w Helm only for ! rke2 clusters

```bash
helm repo add cilium https://helm.cilium.io/
helm install cilium cilium/cilium --version 1.14.0  -f cilium-values.yaml -n kube-system
```

```yaml
# cilium-values.yaml
---
kubeProxyReplacement: strict # This setting enable the cilium kube-proxy replacment
k8sServiceHost: 172.28.30.173 # Enter Kube-API Host IP or set it to ""
k8sServicePort: 6443 # Enter Kube-API Host Port number or set it to ""
ingressController:
  enabled: true # This setting enable the cilium ingress controller
hubble:
  enabled: true
  relay:
    enabled: true # This setting enable hubble relay
  ui:
    enabled: true # This setting enable hubble ui
ipam:
  mode: "kubernetes" # This setting prevent cilium to overide the service and pod subnet and use the kubeadm network configuration
l2announcements:
  enabled: true # This setting enable the metallb like arp load balancing
```

## Create loadbalancer pool

Like in metallb we need to create a ip pool for cilium

```yaml
# cilium-mainpool.yaml
---
apiVersion: "cilium.io/v2alpha1"
kind: CiliumLoadBalancerIPPool
metadata:
  name: "main-pool"
spec:
  cidrs:
  - cidr: "10.1.2.0/24"
```

## Configure the L2 Announcement

Like in metallb we need activate and configure the announcement of the ip pool

This is a basic example and we announce the pool to all network interfaces:

```yaml
# cilium-l2policy.yaml
---
apiVersion: "cilium.io/v2alpha1"
kind: CiliumL2AnnouncementPolicy
metadata:
  name: policy1
spec:
  nodeSelector:
    matchExpressions:
      - key: node-role.kubernetes.io/control-plane
        operator: DoesNotExist
  externalIPs: true
  loadBalancerIPs: true
```

Recommend: This is a basic example and we announce the pool only to network interfaces, that match the regex term "^eth[0-9]+" and only announce services with the requestet label "l2=active":

```yaml
# cilium-l2policy.yaml
---
apiVersion: "cilium.io/v2alpha1"
kind: CiliumL2AnnouncementPolicy
metadata:
  name: policy1
spec:
  serviceSelector:
    matchLabels:
      l2: active
  nodeSelector:
    matchExpressions:
      - key: node-role.kubernetes.io/control-plane
        operator: DoesNotExist
  interfaces:
  - ^eth[0-9]+
  externalIPs: true
  loadBalancerIPs: true
```

## Use Cilium for kubernetes services

We can use a annotation to tell cilium, which specific ip should set for the service

```yaml
annotations:
  io.cilium/lb-ipam-ips: 172.28.30.200
```

## Commands for troubleshooting

Check l2 works:

In this example we testing, if cilium is announcing the service correctly over arp. The service is exposed /w cilium over arp via 172.28.30.200

```bash
arping: arping -I <interface> <announced_ip>

[root@linux ~] # arping -I ens192 172.28.30.200
ARPING 172.28.30.200 from 172.28.30.184 ens192
Unicast reply from 172.28.30.200 [00:50:56:89:5E:0A]  0.853ms
Unicast reply from 172.28.30.200 [00:50:56:89:5E:0A]  0.707ms
Unicast reply from 172.28.30.200 [00:50:56:89:5E:0A]  0.741ms
Unicast reply from 172.28.30.200 [00:50:56:89:5E:0A]  0.634ms
Unicast reply from 172.28.30.200 [00:50:56:89:5E:0A]  0.763ms
```

Check IP pool CR:

```bash
kubectl get ippools
```

Check l2 Announcement CR:

```bash
kubectl describe l2announcement
```

Check l2 leases: (look for ressources with pattern l2announce)

```bash
kubectl -n kube-system get lease
```

Also check the logs of cilium pods and operator!!
Relevant log part from cilium pod:

```bash
[...]
level=info msg="Serving cilium health API at unix:///var/run/cilium/health.sock" subsys=health-server
level=info msg="attempting to acquire leader lease kube-system/cilium-l2announce-kube-system-cilium-ingress..." subsys=klog
level=info msg="successfully acquired lease kube-system/cilium-l2announce-kube-system-cilium-ingress" subsys=klog
[...]
```

## Cilium ingress controller (tbd)

## Cilium wildcard default certs (tbd)

## Admission webhooks time out after a reboot (kind + socket LB)

### Symptom

Any admission webhook fails with a 10s timeout, e.g. Tekton:

```bash
failed calling webhook "webhook.pipeline.tekton.dev":
Post "https://tekton-pipelines-webhook.tekton-pipelines.svc:443/defaulting":
context deadline exceeded
```

The webhook pod is Running and has Endpoints, the cert is fine — but every request
from the apiserver runs into the timeout. Affects all webhooks (Crossplane, cert-manager, ...),
not just Tekton.

### Cause

`/run` inside a kind node is a **tmpfs**, so the `/run/cilium/cgroupv2` mount is gone after
every node container (re)start — i.e. after every host reboot or `docker restart`. It is only
recreated by the `mount-cgroup` init container of the cilium pod.

Whether that init container re-runs is not deterministic: if kubelet rebuilds the pod sandbox
it runs, if it only restarts the containers in place it is skipped. Without the mount, cilium's
socket LB (kube-proxy replacement) no longer translates ClusterIPs for processes in the host
netns. The BPF service map is still correct — `cilium-dbg service list` looks fine — but the
translation never happens.

This hurts most on the **control plane**, because the apiserver runs there with hostNetwork:
it can no longer reach a single ClusterIP, so all admission webhooks time out.

### Detect

Fast check — is the network broken, or is it something else?

```bash
docker exec kind1-control-plane sh -c 'timeout 6 curl -sk -o /dev/null \
  -w "%{http_code}\n" https://10.96.0.1:443/ || echo TIMEOUT'
```

`403` means the network is fine, look elsewhere. `TIMEOUT` means it is this problem.

Confirm by checking the mount on every node:

```bash
for n in kind1-control-plane kind1-worker kind1-worker2; do
  printf "%-22s " $n
  docker exec $n sh -c 'grep -q cilium/cgroupv2 /proc/mounts && echo OK || echo MISSING'
done
```

Useful to tell this apart from a real webhook problem: the pod IP works while the ClusterIP
does not.

```bash
# pod IP - works even when broken
docker exec kind1-control-plane sh -c 'timeout 5 curl -sk -o /dev/null \
  -w "%{http_code}\n" https://<webhook-pod-ip>:8443/defaulting'

# ClusterIP - times out
docker exec kind1-control-plane sh -c 'timeout 5 curl -sk -o /dev/null \
  -w "%{http_code}\n" https://<webhook-svc-ip>:443/defaulting'
```

### Fix

Recreate the cilium pod on the affected node so the init containers — and with them
`mount-cgroup` — run again:

```bash
NODE=kind1-control-plane

kubectl -n kube-system delete pod -l k8s-app=cilium \
  --field-selector spec.nodeName=$NODE

kubectl -n kube-system wait --for=condition=Ready pod -l k8s-app=cilium \
  --field-selector spec.nodeName=$NODE --timeout=180s
```

Short network disruption on that node, ~15s.

### Verify

```bash
# mount back?
docker exec $NODE sh -c 'grep cilium/cgroupv2 /proc/mounts'

# ClusterIP reachable? expect 403 in ~10ms instead of a timeout
docker exec $NODE sh -c 'timeout 6 curl -sk -o /dev/null \
  -w "%{http_code} t=%{time_total}\n" https://10.96.0.1:443/'

# webhook path end to end - expect a sub-second answer
kubectl apply --dry-run=server -f <some-pipelinerun>.yaml
```

Also confirm the init container actually re-ran — `mount-cgroup` must show a recent timestamp:

```bash
kubectl -n kube-system get pod <new-cilium-pod> \
  -o jsonpath='{range .status.initContainerStatuses[*]}{.name}{" finished="}{.state.terminated.finishedAt}{"\n"}{end}'
```

Note that `config` is a native sidecar in cilium 1.19 and restarts independently of the other
init containers — a fresh timestamp on `config` alone does not mean `mount-cgroup` ran.
