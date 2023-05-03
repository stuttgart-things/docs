# FLUX

## LIST

### HELM RELEASES

```
kubectl get hr -A  # LIST ALL HRs
flux suspend hr metallb-configuration -n metallb-system # SUSPEND HR
flux resume hr metallb-configuration -n metallb-system # RESUME HR
```

### LIST ALL HELM KUSTOMIZATIONS

```
kubectl get Kustomization -A
```

