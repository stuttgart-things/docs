# stuttgart-things/docs/flux

## USE AGE+SOPS FOR SECRETS

[age](https://github.com/getsops/sops/releases) - management of gnupg keyrings and PGP keys
[sops](https://github.com/FiloSottile/age/releases) - encrypts file while maintaining the original structure

### CREATE KEY FOR SOPS W/ AGE

```bash
age-keygen -o sops.key
```

### CREATE SOPS CONFIG YAML

```bash
AGE_PUB_KEY=$(cat sops.key | grep 'public key' | awk '{ print $4 }')
cat <<EOF > .sops.yaml
creation_rules:
  - encrypted_regex: '^(data|stringData)$'
    age: ${AGE_PUB_KEY}
EOF
```

### EXAMPLE ENCRYPTION

```bash
cat <<EOF > ./secret.yaml
kind: Secret
apiVersion: v1
metadata:
  name: secret
data:
  password: wHat6ver
EOF

sops -e ./secret.yaml | tee sops-secret.yaml
```

### DECRYPTION ON SHELL

```bash
export SOPS_AGE_KEY_FILE=${PWD}/sops.key
sops --decrypt sops-secret.yaml
```

### DECRYPTION ON FLUX

```bash
kubectl -n flux-system create secret generic sops-age \
--from-file=age.agekey=sops.key
```

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: flux-system
  namespace: flux-system
spec:
  interval: 10m0s
  path: ./clusters/labul/pve/dev43
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
  decryption:
    provider: sops
    secretRef:
      name: sops-age
```

## USE AS S3 AS SOURCE

### CREATE S3 SECRET

```bash
kubectl apply -f - <<EOF
---
apiVersion: v1
kind: Secret
metadata:
  name: artifacts-labul-automation-secret
  namespace: flux-system
type: Opaque
stringData:
  accesskey: flux
  secretkey: <${SECRET}
EOF
```

### CREATE S3 BUCKET

```bash
kubectl apply -f - <<EOF
---
apiVersion: source.toolkit.fluxcd.io/v1beta2
kind: Bucket
metadata:
  name: artifacts-labul-automation
  namespace: flux-system
spec:
  interval: 5m0s
  endpoint: artifacts.automation.sthings-vsphere.labul.sva.de
  insecure: false
  secretRef:
    name: artifacts-labul-automation-secret
  bucketName: vsphere-vm
EOF
```

### CREATE S3 KUSTOMIZATION

```bash
kubectl apply -f - <<EOF
---
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: terraform
  namespace: flux-system
spec:
  interval: 10m0s
  prune: true
  path: ./
  sourceRef:
    kind: Bucket
    name: artifacts-labul-automation
EOF
```

## MOUNT CUSTOM CERTIFICAT IN SOURCE CONTROLLER

### CREATE PUB CERT AS CM

[issue](https://github.com/fluxcd/flux2/issues/3417)

#### VIA KUBECTL

```bash
kubectl -n <namespace-for-config-map-optional> \
create configmap ca-pemstore -— from-file=labul-pve.crt
```

#### VIA MANIFEST

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ca-pemstore
  namespace: flux-system
data:
  labul-pve.crt: |-
    -----BEGIN CERTIFICATE-----
    MIIFeDCCA2CgAwIBAgIUT4jkE73bE/rKLhh9k03K2uJ8EjowDQYJKoZIhvcNAQEL
    #...
    -----END CERTIFICATE-----
```

#### PATCH SOURCE-CONTROLLER KUSTOMIZATION

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- gotk-components.yaml
- gotk-sync.yaml
patches:
  - patch: |
      - op: add
        path: /spec/template/spec/volumes/-
        value:
          name: ca-pemstore
          configMap:
            name: ca-pemstore
      - op: add
        path: /spec/template/spec/containers/0/volumeMounts/-
        value:
          name: ca-pemstore
          mountPath: /etc/ssl/certs/my-cert.pem
          subPath: labul-pve.crt
          readOnly: true
    target:
      kind: Deployment
      name: source-controller
```

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
export KUBECONFIG=<KUBECONFIG>
export GITHUB_TOKEN=<TOKEN>
flux bootstrap github --owner=stuttgart-things --repository=stuttgart-things --path=clusters/labda/vsphere/u23-test # EXAMPLE
```

## BOOTRSTAP FROM PRIVATE GITHUB

```bash
export KUBECONFIG=<KUBECONFIG>
export GITLAB_TOKEN=<TOKEN>
flux bootstrap gitlab --token-auth --hostname=<GITHUB-SERVER> --owner=Lab/stuttgart-things --repository=stuttgart-things --branch=master --path=clusters/labul/vsphere/sthings2 # EXAMPLE
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
flux reconcile kustomization vault -n flux-system # RECONCILE KUSTOMIZATION
flux reconcile source helm argocd  -n argocd # RECONCILE HELM SOURCE
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
          path: /spec/values/ingress/server/enabled
          value: false
      target:
        kind: HelmRelease
        name: vault-deployment
        namespace: vault
```

#### ADD GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: stuttgart-things-github
  namespace: flux-system
spec:
  interval: 1m0s
  ref:
    branch: main
  url: https://github.com/stuttgart-things/stuttgart-things.git
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
