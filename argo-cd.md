# stuttgart-things/docs/argo-cd

## LOGIN w/ CLI
```
argocd login argo-cd.mgmt.sthings-vsphere.labul.sva.de:443 --insecure
```
## ADD CLUSTER TO ARGO-CD w/ CLI
```
# download kubeconfig of target cluster local and export KUBECONFIG
argocd cluster add $(kubectl config current-context) --name sthings-app --grpc-web
```

## TERMINATE APPLICATION
```
argocd app terminate-op yacht-application-server
```
