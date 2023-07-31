# stuttgart-things/docs/cilium
NOT FINISHED!!!!

## Install Cilium /w Helm
```
helm repo add cilium https://helm.cilium.io/
helm install cilium cilium/cilium --version 1.14.0  -f cilium-values.yaml -n kube-system
```
```
# cilium-values.yaml
---
kubeProxyReplacement: strict
k8sServiceHost: 172.28.30.173
k8sServicePort: 6443
ingressController:
  enabled: true
hubble:
  enabled: true
  relay:
    enabled: true
  ui:
    enabled: true
ipam:
  mode: "kubernetes"
l2announcements:
  enabled: true
```
