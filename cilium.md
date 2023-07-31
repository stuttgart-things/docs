# stuttgart-things/docs/cilium
NOT FINISHED!!!!
Cilium 1.14.0 is compatible with k8s 1.17.x or older

## K8s Cluster
Install cluster w/ kudeadm:
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
  mode: "kubernetes" # This setting prevent cilium to overide the service and pod subnet
l2announcements:
  enabled: true # This setting enable the metallb like arp load balancing
```
