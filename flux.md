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

### OVERWRITE HELM VALUES (EXAMPLE)

#### APP DEFINITION 

```yaml
# /infra/vault/release.yaml
apiVersion: helm.toolkit.fluxcd.io/v2beta1
kind: HelmRelease
metadata:
  name: vault-deployment
  namespace: vault
spec:
  interval: 30m
  dependsOn:
    - name: vault-certificate-configuration
      namespace: vault
  chart:
    spec:
      chart: vault
      version: 0.25.0
      sourceRef:
        kind: HelmRepository
        name: hashicorp
        namespace: vault
      interval: 12h
  values:
    injector:
      enabled: false
    server:
      enabled: true
      dataStorage:
        enabled: true
        storageClass: ${VAULT_STORAGE_CLASS}
        size: ${VAULT_STORAGE_SIZE}
      ingress:
        enabled: true
        hosts:
          - host: ${VAULT_INGRESS_HOSTNAME}.${VAULT_INGRESS_DOMAIN}
        tls:
          - hosts:
            - ${VAULT_INGRESS_HOSTNAME}.${VAULT_INGRESS_DOMAIN}
            secretName: ${VAULT_INGRESS_HOSTNAME}-ingress-tls
        ingressClassName: nginx
    csi:
      enabled: true
```

```yaml
# /clusters/cluster1/infra.yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: vault
  namespace: flux-system
spec:
  interval: 1h
  retryInterval: 1m
  timeout: 5m
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./infra/vault
  prune: true
  wait: true
  patches:
    - patch: |-
        - op: replace
          path: /spec/values
          value: {}
      target:
        kind: HelmRelease
        name: vault-certificate-configuration
        namespace: vault
    - patch: |-
        - op: replace
          path: /spec/values/ingress/enabled
          value: false
      target:
        kind: HelmRelease
        name: vault-deployment
        namespace: vault
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
