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

### CREATE W/ TERRAFORM

#### TF CODE FOR CREATING K8S FOR NAMESPACE/CLUSTER

<details><summary><b>k8s-auth.tf</b></summary>

```hcl
# FIX TF CODE OR CREATE SECRET PRIOR TF RUN w/ KUBECTL
# apiVersion: v1
# kind: Secret
# metadata:
#   name: vault
#   namespace: kube-system
#   annotations:
#     kubernetes.io/service-account.name: vault
#     kubernetes.io/service-account.namespace: kube-system
# type: kubernetes.io/service-account-token

# data "kubernetes_secret" "vault" {
#   metadata {
#     name      = "vault"
#     namespace = "kube-system"
#   }
# }

resource "kubernetes_manifest" "service_account" {
  manifest = {
    "apiVersion" = "v1"
    "kind"       = "ServiceAccount"
    "metadata" = {
      "namespace" = "kube-system"
      "name"      = "vault"
    }

    "automountServiceAccountToken" = true
  }

}

resource "kubernetes_cluster_role_binding" "vault" {
  metadata {
    name = "vault-auth"
  }
  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "system:auth-delegator"
  }
  subject {
    kind      = "ServiceAccount"
    name      = "vault"
    namespace = "kube-system"
  }

  depends_on = [
    kubernetes_manifest.service_account
  ]

}


resource "vault_auth_backend" "kubernetes" {
  type = "kubernetes"
  path = "all"
}

resource "vault_kubernetes_auth_backend_config" "kubernetes" {
  backend            = vault_auth_backend.kubernetes.path
  kubernetes_host    = "https://10.100.136.143:6443"
  kubernetes_ca_cert = "-----BEGIN CERTIFICATE-----\n ... \n-----END CERTIFICATE-----"
  token_reviewer_jwt = "ey ... wA"
  disable_iss_validation = "true"
  disable_local_ca_jwt   = "true"
}

resource "vault_policy" "secrets" {
  name = "secrets-access"

  policy = <<EOT
path "env/*" {
  capabilities = ["read","list","update","create","delete"]
}
EOT
}

resource "vault_kubernetes_auth_backend_role" "default" {
  backend                          = vault_auth_backend.kubernetes.path
  role_name                        = "allow-all"
  bound_service_account_names      = ["*"]
  bound_service_account_namespaces = ["*"]
  token_ttl                        = 7200
  token_policies                   = ["default", vault_policy.secrets.name]
}

provider "vault" {
  address = "https://vault.dev11.4sthings.tiab.ssc.sva.de"
  token   = "<REPLACE-ME"
}

provider "kubernetes" {
  config_context = "default"
  config_path    = "~/.kube/labda-app"
}
```

</details>


<details><summary><b>static-secret.yaml</b></summary>

```yaml
---
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultConnection
metadata:
  name: vault-connection
  namespace: kube-system
spec:
  address: https://vault.dev11.4sthings.tiab.ssc.sva.de
  skipTLSVerify: true
---
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultAuth
metadata:
  name: vault-auth11
  namespace: kube-system
spec:
  vaultConnectionRef: vault-connection
  method: kubernetes
  mount: all
  kubernetes:
    role: allow-all
    serviceAccount: vault
---
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: vault-static-secret11
  namespace: kube-system
spec:
  vaultAuthRef: vault-auth11
  mount: env
  type: kv-v2
  path: labul
  refreshAfter: 10s
  destination:
    create: true
    name: vso-handled-new
```

</details>

## OPENBAO

### Deploy via Compose

<details><summary><b>docker-compose.yml</b></summary>

```yaml
name: openbao

services:
  openbao:
    image: openbao/openbao:2.5.1
    container_name: openbao
    restart: unless-stopped

    cap_add:
      - IPC_LOCK

    command: server

    environment:
      BAO_ADDR: http://0.0.0.0:8200

    volumes:
      - ./config:/openbao/config
      - ./data:/openbao/file
      - ./logs:/openbao/logs

    expose:
      - "8201"   # internal cluster port (raft)

    networks:
      - web
      - openbao-internal

    labels:
      - "traefik.enable=true"

      # HTTP → HTTPS redirect
      - "traefik.http.routers.openbao-http.rule=Host(`YOUR_VAULT_URL`)"
      - "traefik.http.routers.openbao-http.entrypoints=web"
      - "traefik.http.routers.openbao-http.middlewares=openbao-https-redirect"
      - "traefik.http.routers.openbao-http.service=openbao"

      # HTTPS router
      - "traefik.http.routers.openbao.rule=Host(`YOUR_VAULT_URL`)"
      - "traefik.http.routers.openbao.entrypoints=websecure"
      - "traefik.http.routers.openbao.tls=true"
      - "traefik.http.routers.openbao.service=openbao"

      # Backend port
      - "traefik.http.services.openbao.loadbalancer.server.port=8200"

      # Redirect middleware
      - "traefik.http.middlewares.openbao-https-redirect.redirectscheme.scheme=https"
      - "traefik.http.middlewares.openbao-https-redirect.redirectscheme.permanent=true"

      # Proper proxy header handling
      - "traefik.http.middlewares.openbao-headers.headers.sslProxyHeaders.X-Forwarded-Proto=https"
      - "traefik.http.routers.openbao.middlewares=openbao-headers"

      # Important: must match your traefik docker network
      - "traefik.docker.network=web"

networks:
  web:
    external: true
  openbao-internal:
    driver: bridge
```

</details>


<details><summary><b>config/openbao.hcl</b></summary>

```
ui = true

storage "raft" {
  path = "/openbao/file"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1
}

api_addr     = "https://YOUR_BAO_ADDR"
cluster_addr = "http://openbao:8201"
```

</details>


### Vault Terraform Configuration

Manages [OpenBao](https://openbao.org/) (Vault-compatible) infrastructure using a reusable Terraform module.

#### Example Structure (with keycloak-specific vault configuration)

```
terraform/
├── modules/
│   └── vault/          # Reusable module: KV secrets, policies, AppRole
└── environments/
    └── keycloak/       # Keycloak-specific Vault configuration
```

#### Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.5
- Access to the OpenBao instance at `https://YOUR_VAULT_URL`
- A Vault token with sufficient permissions (root token for initial bootstrap only)

#### Quick Start

```bash
cd terraform/environments/keycloak
terraform init
terraform apply -var="vault_token=$VAULT_TOKEN"
```

#### Adding a New Service

1. Create a new environment directory:

```bash
mkdir -p environments/<service-name>
```

2. Add `main.tf` that calls the module:

<details><summary><b>main.tf</b></summary>
  
```hcl
module "vault" {
 source = "../../modules/vault"

 enable_kv = false  # KV mount already exists after first apply

 secrets = {
   <service-name> = {
     USERNAME = "..."
     PASSWORD = "..."
   }
 }

 policies = {
   <service-name>-read = <<-EOT
     path "secret/data/<service-name>" {
       capabilities = ["read"]
     }
     path "secret/metadata/<service-name>" {
       capabilities = ["read"]
     }
   EOT
 }

 approle_roles = {
   <service-name> = {
     token_policies = ["<service-name>-read"]
   }
 }
}
```

</details>

3. Add `variables.tf`, `terraform.tfvars`, and apply.

> **Note:** Set `enable_kv = false` and `enable_approle = false` if the KV mount or AppRole backend was already created by another environment. Alternatively, use `terraform import` to adopt existing resources.


### Example Keycloak Vault Environment

Provisions Vault secrets and AppRole access for the Keycloak service.

#### Setup

1. **Initialize:**

```bash
cd terraform/environments/keycloak
terraform init
```

2. **Configure main.tf**:

<details><summary><b>main.tf</b></summary>
  
```
terraform {
  required_providers {
    vault = {
      source  = "hashicorp/vault"
      version = "~> 4.0"
    }
  }
}

provider "vault" {
  address = var.vault_addr
  token   = var.vault_token
}

module "vault" {
  source = "../../modules/vault"

  # KV-v2
  kv_mount_path = "secret"

  # Secrets
  secrets = {
    keycloak = {
      DB_USER     = var.keycloak_db_user
      DB_PW       = var.keycloak_db_pw
      KC_ADMIN    = var.keycloak_admin
      KC_ADMIN_PW = var.keycloak_admin_pw
      DB_LOCATION = var.keycloak_db_location
    }
  }

  # Policies
  policies = {
    keycloak-read = <<-EOT
      path "secret/data/keycloak" {
        capabilities = ["read"]
      }
      path "secret/metadata/keycloak" {
        capabilities = ["read"]
      }
    EOT
  }

  # AppRole
  approle_roles = {
    keycloak = {
      token_policies = ["keycloak-read"]
      token_ttl      = 1800
      token_max_ttl  = 3600
    }
  }
}

output "role_id" {
  value = module.vault.approle_role_ids["keycloak"]
}

output "secret_id" {
  value     = module.vault.approle_secret_ids["keycloak"]
  sensitive = true
}

```

</details>


3. **Configure secrets** in `terraform.tfvars`:

```hcl
keycloak_db_pw    = "your-db-password"
keycloak_admin_pw = "your-admin-password"
```

4. **Configure Vars** in `variables.tf`:

#### Variables

| Name | Default | Description |
|------|---------|-------------|
| `vault_addr` | `https://YOUR_VAULT_URL` | Vault API address |
| `vault_token` | — | Token for Terraform provider auth |
| `keycloak_db_user` | `keycloak` | Database username |
| `keycloak_db_pw` | — | Database password |
| `keycloak_admin` | `admin` | Keycloak admin username |
| `keycloak_admin_pw` | — | Keycloak admin password |
| `keycloak_db_location` | `./keycloak-database` | Database volume path |

<details><summary><b>variables.tf</b></summary>

```
variable "vault_addr" {
  type    = string
  default = "https://YOUR_VAULT_URL
}

variable "vault_token" {
  type      = string
  sensitive = true
}

variable "keycloak_db_user" {
  type    = string
  default = "keycloak"
}

variable "keycloak_db_pw" {
  type      = string
  sensitive = true
}

variable "keycloak_admin" {
  type    = string
  default = "admin"
}

variable "keycloak_admin_pw" {
  type      = string
  sensitive = true
}

variable "keycloak_db_location" {
  type    = string
  default = "./keycloak-database"
}

```

</details>

5. **Apply:**

```bash
export VAULT_TOKEN=<root-or-admin-token>
terraform apply -var="vault_token=$VAULT_TOKEN"
```

6. **Retrieve AppRole credentials:**

```bash
terraform output role_id
terraform output -raw secret_id
```


### Using the Secret in Your Keycloak Setup

Replace the static `.env` file with a Vault lookup using the AppRole credentials:

<details><summary><b>fetch-secrets.sh</b></summary>

```bash
#!/usr/bin/env bash
set -euo pipefail

# =========================
# Konfiguration
# =========================
VAULT_ADDR=""   # Your OpenBao/Vault FQDN
ROLE_ID=""                                # Aus AppRole
SECRET_ID=""                            # Aus AppRole
SECRET_PATH="secret/keycloak"                         # KVv2 Mount "secret", Pfad "keycloak"
ENV_FILE=".env"                                    # Ziel-Datei
TMP_FILE="$(mktemp)"
CURL_OPTS=(--fail -sS)                             # keine -k! (TLS verifizieren)

# Falls du eine eigene CA nutzt:
# CURL_OPTS+=( --cacert /pfad/zum/ca.pem )
# Oder System-Truststore verwenden (Default).
# Falls du wirklich testweise TLS-Verify AUS schalten willst (nicht empfohlen):
CURL_OPTS+=( -k )

# Optional: Namespace (falls verwendet)
# VAULT_NAMESPACE="my-namespace"
# HEADER_NAMESPACE=( -H "X-Vault-Namespace: $VAULT_NAMESPACE" )
HEADER_NAMESPACE=()

cleanup() { rm -f "$TMP_FILE"; }
trap cleanup EXIT

# =========================
# Login via AppRole
# =========================
echo "→ AppRole Login…"
LOGIN_PAYLOAD=$(jq -n --arg rid "$ROLE_ID" --arg sid "$SECRET_ID" '{role_id:$rid, secret_id:$sid}')

TOKEN=$(
  curl "${CURL_OPTS[@]}" -X POST \
    -H "Content-Type: application/json" \
    "${HEADER_NAMESPACE[@]}" \
    -d "$LOGIN_PAYLOAD" \
    "$VAULT_ADDR/v1/auth/approle/login" \
  | jq -er '.auth.client_token'
)

if [[ -z "$TOKEN" ]]; then
  echo "✗ Konnte kein Token erhalten." >&2
  exit 1
fi

# =========================
# KV v2 Secret abrufen
#   WICHTIG: bei KV v2 ist der Data-Endpunkt /v1/<mount>/data/<pfad>
# =========================
MOUNT="${SECRET_PATH%%/*}"         # "secret"
SUBPATH="${SECRET_PATH#*/}"        # "keycloak"

DATA_ENDPOINT="$VAULT_ADDR/v1/$MOUNT/data/$SUBPATH"

echo "→ Secrets von $SECRET_PATH lesen…"
curl "${CURL_OPTS[@]}" \
  -H "X-Vault-Token: $TOKEN" \
  "${HEADER_NAMESPACE[@]}" \
  "$DATA_ENDPOINT" \
| jq -er '.data.data | to_entries[] | "\(.key)=\(.value)"' \
> "$TMP_FILE"

# =========================
# Idempotent schreiben
# =========================
if [[ ! -f "$ENV_FILE" ]] || ! diff -q "$TMP_FILE" "$ENV_FILE" >/dev/null 2>&1; then
  mv "$TMP_FILE" "$ENV_FILE"
  echo "✓ $ENV_FILE aktualisiert."
else
  echo "✓ $ENV_FILE unverändert."
fi

```
</details>

#### keycloak docker-compose snippet

```
services:
  keycloak:
    env_file:
      - ./.env
```

#### Fetch Secrets and start keycloak compose setup
```
chmod +x fetch-secrets.sh
./fetch-secrets.sh
docker compose up -d
```

</details>


#### Debugging 

Check if Vault is sealed

```bash
docker exec -it openbao bao status
```

Unseal Vault (you need your unseal keys (execute 3 times))
```bash
docker exec -it openbao bao operator unseal
```


