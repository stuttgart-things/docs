# stuttgart-things/docs/vault

## GENERAL

<details><summary><b>PORT FORWARD TO VAULT INSTANCE</b></summary>

```bash
kubectl -n vault port-forward vault-deployment-0 8200:8200
```

</details>

<details><summary><b>CREATE APPROLE</b></summary>

```bash
# ENABLING APPROLE
APPROLE_NAME="kubeconfigs"

vault secrets enable -path=${APPROLE_NAME} kv-v2
vault auth enable approle

# CREATE A VAULT POLICY
vault policy write ${APPROLE_NAME} - <<EOF
path "${APPROLE_NAME}/data/*" {
  capabilities = ["create", "update", "patch", "read", "delete"]
}

path "${APPROLE_NAME}/metadata/*" {
  capabilities = ["list"]
}
EOF

vault policy list

# DEFINE A ROLE
vault write auth/approle/role/${APPROLE_NAME} policies=${APPROLE_NAME}
vault list auth/approle/role

# GENERATE THE AUTHENTICATION CREDENTIALS
vault read auth/approle/role/${APPROLE_NAME}/role-id
vault write -f auth/approle/role/${APPROLE_NAME}/secret-id

# GET APPROLE ID + SECRET ID
export ROLE_ID=<role_id>
export SECRET_ID=<secret_id>

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

<details><summary><b>CONFIGURE VAULT FOR THE USE OF VAULT SECRETS OPERATOR</b></summary>

```bash
# JUMP INTO VAULT POD AND LOGIN
kubectl -n vault exec -it vault-deployment-0 -- /bin/sh
vault login

# CREATE KV ENGINE + PUT EXAMPLE SECRETS
vault secrets enable -path=tektoncd kv-v2
vault kv put tektoncd/cd43 username="web-user" password=":pa55word:"

# CREATE POLICY
vault policy write tektoncd - <<EOF
path "tektoncd/data/cd43" {
   capabilities = ["read"]
}
path "tektoncd/metadata/cd43" {
   capabilities = ["read"]
}
EOF

# ENABLE AUTH
vault auth enable -path=tektoncd kubernetes

# CREATE CONFIG
vault write auth/tektoncd/config \
token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
disable_issuer_verification=true

# CREATE ROLE
vault write auth/tektoncd/role/tektoncd-role \
bound_service_account_names=default \
bound_service_account_namespaces=tektoncd \
policies=tektoncd \
ttl=24h

# VERIFY
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
  name: vault-static-secret-1
  namespace: tektoncd
spec:
  vaultAuthRef: vault-auth
  mount: tektoncd
  type: kv-v2
  path: cd43
  refreshAfter: 10s
  destination:
    create: true
    name: vso-handled
```

</details>

## VAULT KUBERNTES AUTH (EXTERNAL CLUSTER)

### GET CLIENT CLUSTER DETAILS

```bash
TOKEN_REVIEW_JWT=<VAULT-TOKEN>
KUBE_HOST=$(kubectl config view --raw --minify --flatten --output='jsonpath={.clusters[].cluster.server}')
# KUBE_CA_CERT
kubectl config view --raw --minify --flatten --output='jsonpath={.clusters[].cluster.certificate-authority-data}' | base64 -d

echo KUBE_HOST=${KUBE_HOST}
echo TOKEN_REVIEW_JWT=${TOKEN_REVIEW_JWT}
```

### CREATE KUBERNETES AUTH FOR EXTERNAL CLUSTER

```bash
kubectl -n vault exec -it vault-deployment-0 -- /bin/sh
vault login

# COPY FROM STEP ABOVE
echo KUBE_HOST=${KUBE_HOST}
echo TOKEN_REVIEW_JWT=${TOKEN_REVIEW_JWT}

# COPY FROM STEP ABOVE
vi /tmp/dev51.crt

# ENABLE KUBERNETES AUTH
vault auth enable -path=dev51 kubernetes

# CREATE CONFIG
vault write auth/dev51/config \
token_reviewer_jwt="${TOKEN_REVIEW_JWT}" \
kubernetes_host="${KUBE_HOST}" \
kubernetes_ca_cert=@/tmp/dev51.crt \
disable_issuer_verification=true

vault write auth/dev51/role/tektoncd-role \
bound_service_account_names=default \
bound_service_account_namespaces=tektoncd \
policies=tektoncd \
ttl=24h
```
