# stuttgart-things/docs/flux

## TROUBLESHOOTING
```
flux get all -A --status-selector ready=false # show all flux objects that are not ready
kubectl get events -n flux-system --field-selector type=Warning # show flux warning events
```


## CREATE SECRET FOR KUSTOMIZATION
```
apiVersion: v1
kind: Secret
metadata:
  name: vault
  namespace: flux-system
type: Opaque
stringData:
  VAULT_ADDR: https://vault-vsphere.tiab.labda.sva.de:8200
  VAULT_TOKEN: ""
  VAULT_ROLE_ID: ""
  VAULT_SECRET_ID: ""
  VAULT_NAMESPACE: root
  VAULT_CA_BUNDLE: ""
  VAULT_PKI_PATH: vault-vsphere.tiab.labda.sva.de
```

## BOOTRSTAP FROM GITHUB
```
flux bootstrap github --owner=stuttgart-things --repository=stuttgart-things --path=clusters/labda/vsphere/u23-test  # EXAMPLE
```

## UNINSTALL FLUX
```
flux uninstall --namespace=flux-system
```

## LIST

### HELM RELEASES
```
kubectl get hr -A  # LIST ALL HRs
flux suspend hr metallb-configuration -n metallb-system  # SUSPEND HR
flux resume hr metallb-configuration -n metallb-system  # RESUME HR
flux delete hr metallb-configuration -n metallb-system  # NOTHING ELSE MATTERS
```

### LIST ALL HELM KUSTOMIZATIONS
```
kubectl get Kustomization -A
```

