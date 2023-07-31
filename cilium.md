# stuttgart-things/docs/cilium
NOT FINISHED!!!!
Cilium 1.14.0 is compatible with k8s 1.17.x or older

## K8s Cluster
Install cluster w/ kudeadm without kube-proxy:
```
kubeadm init --skip-phases=addon/kube-proxy
```

## Install Cilium /w Helm
```
helm repo add cilium https://helm.cilium.io/
helm install cilium cilium/cilium --version 1.14.0  -f cilium-values.yaml -n kube-system
```
```
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
```
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

## Create loadbalancer pool
Like in metallb we need activate and configure the announcement of the ip pool

This is a basic example and we announce the pool to all network interfaces:
```
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

This is a basic example and we announce the pool only to network interfaces, that match the regex term "^eth[0-9]+":
```
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
  interfaces:
  - ^eth[0-9]+
  externalIPs: true
  loadBalancerIPs: true
```
