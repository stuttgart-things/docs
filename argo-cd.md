# stuttgart-things/docs/argo-cd

## ADD CLUSTER w/ CLI

```
argocd login argo-cd.mgmt.sthings-vsphere.labul.sva.de:443 --insecure

# download kubeconfig of target cluster local and export KUBECONFIG
# get context kubectl w/ config current-context

argocd cluster add default --name sthings-app --grpc-web
```
