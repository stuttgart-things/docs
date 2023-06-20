# stuttgart-things/docs/argo-cd

## ADD CLUSTER w/ CLI

```
argocd login argo-cd.mgmt.sthings-vsphere.labul.sva.de:443 --insecure

# download kubeconfig of target cluster local and export KUBECONFIG

argocd cluster add $(kubectl config current-context) --name sthings-app --grpc-web
```
