# stuttgart-things/docs/flux

## TROUBLESHOOTING

```bash
flux get all -A --status-selector ready=false # show all flux objects that are not ready
kubectl get events -n flux-system --field-selector type=Warning # show flux warning events
```

## CREATE SECRET FOR KUSTOMIZATION

```yaml
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

```bash
flux bootstrap github --owner=stuttgart-things --repository=stuttgart-things --path=clusters/labda/vsphere/u23-test  # EXAMPLE
```

## UNINSTALL FLUX

```bash
flux uninstall --namespace=flux-system
```

## LIST

### HELM RELEASES

```bash
kubectl get hr -A  # LIST ALL HRs
flux suspend hr metallb-configuration -n metallb-system  # SUSPEND HR
flux resume hr metallb-configuration -n metallb-system  # RESUME HR
flux delete hr metallb-configuration -n metallb-system  # NOTHING ELSE MATTERS
flux reconcile kustomization vault -n flux-system # RECREATE HR
```

### LIST ALL HELM KUSTOMIZATIONS

```bash
kubectl get Kustomization -A
```

### PREVIEWING CHANGES FROM KUSTOMIZATION

#### ON CLUSTER

```bash
flux diff kustomization --path=./clusters/labul/pve/bootstrap flux-system
flux build kustomization --path=./clusters/labul/pve/bootstrap flux-system
```

#### LOCAL

```bash
flux build kustomization vault --path clusters/labul/pve/bootstrap --kustomization-file clusters/labul/pve/bootstrap/infra.yaml --dry-run > ../flux.yaml
```
