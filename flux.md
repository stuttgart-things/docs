# FLUX

## BOOTRSTAP FROM GITHUB
```
flux bootstrap github --owner=stuttgart-things --repository=stuttgart-things --path=clusters/labda/vsphere/u23-test  # EXAMPLE
```

## LIST

### HELM RELEASES
```
kubectl get hr -A  # LIST ALL HRs
flux suspend hr metallb-configuration -n metallb-system  # SUSPEND HR
flux resume hr metallb-configuration -n metallb-system  # RESUME HR
```

### LIST ALL HELM KUSTOMIZATIONS
```
kubectl get Kustomization -A
```

