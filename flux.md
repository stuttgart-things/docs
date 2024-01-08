# stuttgart-things/docs/flux

## SNIPPETS

<details><summary>BOOTRSTRAP</summary>

```bash
# BOOTRSTRAP GITHUB
export KUBECONFIG=<KUBECONFIG>
export GITHUB_TOKEN=<TOKEN>
flux bootstrap github --owner=stuttgart-things --repository=stuttgart-things --path=clusters/labda/vsphere/u23-test # EXAMPLE
```

```bash
# BOOTRSTRAP GITLAB
export KUBECONFIG=<KUBECONFIG>
export GITLAB_TOKEN=<TOKEN>
flux bootstrap gitlab --token-auth --hostname=<GITHUB-SERVER> --owner=Lab/stuttgart-things --repository=stuttgart-things --branch=master --path=clusters/labul/vsphere/sthings2 # EXAMPLE
```

```bash
# BOOTRSTAP WITHOUT GIT
flux install \
--namespace=flux-system \
--network-policy=false \
--components=source-controller,helm-controller
```

</details>

<details><summary>TROUBLESHOOTING</summary>

```bash
flux get all -A --status-selector ready=false # show all flux objects that are not ready
kubectl get events -n flux-system --field-selector type=Warning # show flux warning events
```

```bash
kubectl get hr -A  # LIST ALL HRs
flux suspend hr metallb-configuration -n metallb-system  # SUSPEND HR
flux resume hr metallb-configuration -n metallb-system  # RESUME HR
flux delete hr metallb-configuration -n metallb-system  # NOTHING ELSE MATTERS
flux reconcile kustomization vault -n flux-system # RECONCILE KUSTOMIZATION
flux reconcile source helm argocd  -n argocd # RECONCILE HELM SOURCE
```

</details>

<details><summary>PATCH VERSION OF HELMRELEASE</summary>

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: tekton-pipelines
  namespace: flux-system
spec:
  interval: 1h
  retryInterval: 1m
  timeout: 5m
  sourceRef:
    kind: GitRepository
    name: stuttgart-things-github
  path: ./apps/tekton
  prune: true
  wait: true
  postBuild:
    substituteFrom:
      - kind: Secret
        name: vault-flux-secrets
  patches:
    - patch: |-
        - op: replace
          path: /spec/chart/spec/version
          value: v0.53.4
      target:
        kind: HelmRelease
        name: tekton-pipelines
        namespace: tekton-pipelines
```

</details>

<details><summary>ADD HEALTH CHECKS TO HELMRELEASE</summary>

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: crossplane
  namespace: flux-system
spec:
  interval: 1h
  retryInterval: 1m
  timeout: 5m
  sourceRef:
    kind: GitRepository
    name: flux-system
  path: ./apps/crossplane
  prune: true
  wait: true
  patches:
    - patch: |-
        - op: replace
          path: /spec/chart/spec/version
          value: 1.14.5
      target:
        kind: HelmRelease
        name: crossplane-deployment
        namespace: crossplane-system
  healthChecks:
    - apiVersion: helm.toolkit.fluxcd.io/v2beta1
      kind: HelmRelease
      name: crossplane-deployment
      namespace: crossplane-system
    - apiVersion: apps/v1
      kind: Deployment
      name: crossplane
      namespace: crossplane-system
```

</details>

<details><summary>CREATE SECRET FOR KUSTOMIZATION</summary>

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

</details>

</details>

<details><summary>UNINSTALL FLUX</summary>

```bash
flux uninstall --namespace=flux-system
```

</details>

<details><summary>ADD GITREPOSITORY AS YAML</summary>

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

</details>

<details><summary>PATCH HELM VALUES</summary>

```yaml
# APP DEFINITION
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
# KUSTOMIZATION
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
</details>

<details><summary>USE AS S3 AS SOURCE</summary>

```bash
# CREATE S3 SECRET
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

# CREATE S3 BUCKET
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

# CREATE S3 KUSTOMIZATION
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

</details>



## USE AGE+SOPS FOR SECRETS
<!-- https://deyan7.de/en/sops-secrets-operations-kubernetes-operator-secure-your-sensitive-data-while-maintaining-ease-of-use/ -->
[age](https://github.com/getsops/sops/releases) - management of gnupg keyrings and PGP keys
[sops](https://github.com/FiloSottile/age/releases) - encrypts file while maintaining the original structure


<details><summary><b>CREATE KEY FOR SOPS W/ AGE</b></summary>

```bash
age-keygen -o sops.key
```

</details>

<details><summary><b>CREATE SOPS CONFIG YAML</b></summary>

```bash
AGE_PUB_KEY=$(cat sops.key | grep 'public key' | awk '{ print $4 }')
cat <<EOF > .sops.yaml
creation_rules:
  - encrypted_regex: '^(data|stringData)$'
    age: ${AGE_PUB_KEY}
EOF
```

</details>

<details><summary><b>EXAMPLE ENCRYPTION</b></summary>

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

</details>

<details><summary><b>DECRYPTION ON SHELL</b></summary>

```bash
export SOPS_AGE_KEY_FILE=${PWD}/sops.key
sops --decrypt sops-secret.yaml
```

</details>

<details><summary><b>DECRYPTION ON FLUX</b></summary>

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

</details>

## MOUNT CUSTOM CERTIFICAT IN SOURCE CONTROLLER

[issue](https://github.com/fluxcd/flux2/issues/3417)

<details><summary><b>CREATE PUB CERT VIA KUBECTL</b></summary>

```bash
kubectl -n <namespace-for-config-map-optional> \
create configmap ca-pemstore -— from-file=labul-pve.crt
```

</details>

<details><summary><b>CREATE PUB CERT VIA MANIFEST</b></summary>

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

</details>

<details><summary><b>PATCH SOURCE-CONTROLLER KUSTOMIZATION</b></summary>

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

</details>

<details><summary><b>PREVIEWING CHANGES FROM KUSTOMIZATION ON CLUSTER</b></summary>

```bash
flux diff kustomization --path=./clusters/labul/pve/bootstrap flux-system
flux build kustomization --path=./clusters/labul/pve/bootstrap flux-system
```

</details>

<details><summary><b>PREVIEW CHANGES FROM KUSTOMIZATION LOCALLY</b></summary>

```bash
flux build kustomization vault --path clusters/labul/pve/bootstrap --kustomization-file clusters/labul/pve/bootstrap/infra.yaml --dry-run > ../flux.yaml
```

</details>
