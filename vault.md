# stuttgart-things/docs/vault

## GENERAL

</details>

<details><summary><b>PORT FORWARD TO VAULT INSTANCE</b></summary>

```bash
kubectl -n vault port-forward vault-deployment-0 8200:8200
```

</details>

<details><summary><b>CREATE APPROLE</b></summary>

```bash
# Enabling AppRole
vault secrets enable -path=kubeconfigs kv-v2
vault auth enable approle

# Create a Vault Policy
vault policy write kubeconfigs - <<EOF
path "kubeconfigs/data/*" {
  capabilities = ["create", "update", "patch", "read", "delete"]
}

path "kubeconfigs/metadata/*" {
  capabilities = ["list"]
}
EOF
vault policy list

# Define a Role
vault write auth/approle/role/kubeconfigs policies=kubeconfigs
vault list auth/approle/role

# Generate the Authentication Credentials
vault read auth/approle/role/kubeconfigs/role-id
vault write -f auth/approle/role/kubeconfigs/secret-id

# Use Credentials To Login Using AppRole
vault write auth/approle/login \
role_id=${ROLE_ID} \
secret_id=${SECRET_ID} 
```

</details>

## USE VAULT W/ SECRETS CSI DRIVER

<details><summary><b>DEPLOY VAULT W/ CSI DRIVER ENABLED</b></summary>

```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

cat <<EOF > vaul-values.yaml
csi:
  enabled: true
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
    annotations:
      kubernetes.io/ingress.class: nginx
      kubernetes.io/tls-acme: "true"
    hosts:
      - host: ${VAULT_INGRESS_HOSTNAME}.${VAULT_INGRESS_DOMAIN}
    tls:
      - hosts:
        - ${VAULT_INGRESS_HOSTNAME}.${VAULT_INGRESS_DOMAIN}
        secretName: ${VAULT_INGRESS_HOSTNAME}-ingress-tls
EOF

helm upgrade --install vault hashicorp/vault -n vault --create-namespace --version 0.25.0 --values vaul-values.yaml
```

</details>

<details><summary><b>DEPLOY SECRETS STORE CSI DRIVER</b></summary>

```bash
helm repo add secrets-store-csi-driver https://kubernetes-sigs.github.io/secrets-store-csi-driver/charts
helm repo update
helm upgrade --install vault-deployment secrets-store-csi-driver/secrets-store-csi-driver -n vault --version 1.3.4
```

</details>

<details><summary><b>CONFIGURE VAULT</b></summary>

```bash
kubectl -n vault exec -it vault-deployment-0 -- /bin/sh

vault login root  # or w/ ingress vault login -address=https://vault.dev11.4sthings.tiab.ssc.sva.de -tls-skip-verify
vault secrets enable -version=1 kv
vault auth enable kubernetes
vault write auth/kubernetes/config token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

vault policy write kv_policy - <<EOF
path "kv/*" {
  capabilities = ["read"]
}
EOF

vault write auth/kubernetes/role/csi-kv \
bound_service_account_names=csi-sa \
bound_service_account_namespaces=default \
policies=kv_policy \
ttl=20m

## Put some Sample data
vault kv put kv/db password=password
vault kv put kv/app user=admin
```

</details>


<details><summary><b>EXAMPLE: SECRET-PROVIDER-CLASS</b></summary>


```yaml
---
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: vault-git-creds
  namespace: tektoncd
spec:
  provider: vault
  parameters:
    roleName: csi-kv
    vaultAddress: 'http://vault-deployment.vault.svc.cluster.local:8200'
    objects: |
      - objectName: "token"
        secretPath: "kv/git"
        secretKey: "token"
      - objectName: ".git-credentials"
        secretPath: "kv/git"
        secretKey: ".git-credentials"
      - objectName: ".gitconfig"
        secretPath: "kv/git"
        secretKey: ".gitconfig"
---
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: vault-kaniko-creds
  namespace: tektoncd
spec:
  provider: vault
  parameters:
    roleName: csi-kv
    vaultAddress: 'http://vault-deployment.vault.svc.cluster.local:8200'
    objects: |
      - objectName: "config.json"
        secretPath: "kv/acr"
        secretKey: "config.json"
```

</details>

<details><summary><b>EXAMPLE: MOUNT SECRETS AS FILES</b></summary>

```bash
apiVersion: secrets-store.csi.x-k8s.io/v1alpha1
kind: SecretProviderClass
metadata:
  name: vault-user-creds
spec:
  provider: vault
  parameters:
    roleName: 'csi-kv'
    vaultAddress: 'http://vault-deployment:8200'
    objects: |
      - objectName: "user"
        secretPath: "kv/app"
        secretKey: "user"
      - objectName: "password"
        secretPath: "kv/db"
        secretKey: "password"
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: csi-sa
  namespace: default
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: demo
spec:
  selector:
    matchLabels:
      app: demo
  replicas: 1
  template:
    metadata:
      labels:
        app: demo
    spec:
      serviceAccountName: csi-sa
      containers:
        - name: app
          image: nginx
          volumeMounts:
            - name: 'vault-user-creds'
              mountPath: '/mnt/secrets-store'
              readOnly: true
      volumes:
        - name: vault-user-creds
          csi:
            driver: 'secrets-store.csi.k8s.io'
            readOnly: true
            volumeAttributes:
              secretProviderClass: 'vault-user-creds'
```

</details>

<details><summary><b>KVDB V2 SECRET ENGINE/PATH</b></summary>

```
# EXAMPLE SECRET FOR V2 VAULT KVDB
apiVersion: secrets-store.csi.x-k8s.io/v1
kind: SecretProviderClass
metadata:
  name: vault-creds
  namespace: tektoncd
spec:
  provider: vault
  parameters:
    roleName: csi-kv
    vaultAddress: 'http://vault-deployment.vault.svc.cluster.local:8200'
    objects: |
      - objectName: "VAULT_ADDR"
        secretPath: "kv/data/vault-pve"
        secretKey: "VAULT_ADDR"
```

</details>

## VAULT SECRETS OPERATOR

<details><summary><b>CONFIGURE VAULT SECRETS OPERATOR</b></summary>

```bash
#jump into vault pod and login
kubectl -n vault exec -it vault-deployment-0 -- /bin/sh
vault login

#create kv engine + put example secrets
vault secrets enable -path=tektoncd kv-v2
vault kv put kvv2/tektoncd username="web-user" password=":pa55word:"

#create policy
vault policy write tektoncd - <<EOF
path "tektoncd/data/tektoncd" {
   capabilities = ["read"]
}
path "kvv2/metadata/tektoncd" {
   capabilities = ["read"]
}
EOF

#enable auth
vault auth enable -path=tektoncd kubernetes

#create config
vault write auth/tektoncd/config \
token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
disable_issuer_verification=true

#create role
vault write auth/tektoncd/role/tektoncd-role \
bound_service_account_names=default \
bound_service_account_namespaces=tektoncd \
policies=tektoncd \
ttl=24h

#verify
vault list auth/tektoncd/role
vault read auth/tektoncd/role/tektoncd-role
```

</details>


<details><summary><b>CONFIGURE VAULT SECRETS OPERATOR SERVICE ACCOUNT</b></summary>

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: vault-auth
  namespace: tektoncd
---
apiVersion: v1
kind: Secret
metadata:
  name: vault-auth
  namespace: tektoncd
  annotations:
    kubernetes.io/service-account.name: vault-auth
type: kubernetes.io/service-account-token
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: role-tokenreview-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects:
  - kind: ServiceAccount
    name: vault-auth
    namespace: tektoncd
```

</details>

<details><summary><b>DEPLOY VAULT SECRETS OPERATOR</b></summary>

```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update
helm upgrade --install vault-secrets-operator hashicorp/vault-secrets-operator --version 0.3.4
```

</details>

<details><summary><b>CREATE VSO CONNECTION + STATIC SECRET</b></summary>

```yaml
---
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultConnection
metadata:
  name: vault-connection
  namespace: tektoncd
spec:
  # address to the Vault server.
  address: http://vault-deployment.vault.svc.cluster.local:8200
  skipTLSVerify: true
---
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultAuth
metadata:
  name: vault-auth
  namespace: tektoncd
spec:
  vaultConnectionRef: vault-connection
  method: kubernetes
  mount: tektoncd
  kubernetes:
    role: tektoncd-role
    serviceAccount: default
---
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: vault-static-secret
  namespace: tektoncd
spec:
  vaultAuthRef: vault-auth
  mount: kvv2
  type: kv-v2
  path: tektoncd
  refreshAfter: 10s
  destination:
    create: true
    name: vso-handled
```

</details>

