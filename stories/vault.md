# VAULT

## DEPLOY VAULT

<details><summary><b>DEPLOY w/ HELMFILE ON KIND</b></summary>

```bash
REQUIREMENTS:
✅ Kind Cluster w/ conifgured CNI/Cert-Manager/Ingress Controller
✅ helmfile, kubectl installed
```

```bash
cat <<EOF > vault.yaml
---
helmfiles:
  - path: git::https://github.com/stuttgart-things/helm.git@apps/vault.yaml
    values:
      - namespace: vault
      - injectorEnabled: true
      - clusterIssuer: <CHANGE> # e.g. selfsigned
      - issuerKind: <CHANGE> # e.g. cluster-issuer
      - hostname: vault
      - domain: <CHANGE> # e.g. 172.18.0.4.nip.io
      - ingressClassName: nginx
EOF
```

```bash
# INIT HELMFILE
helmfile init --force

# APPLY HELMFILE
helmfile apply -f vault.yaml 
```

</details>

<details><summary><b>DEPLOY w/ ARGOCD</b></summary>

```bash
REQUIREMENTS:
✅ ArgoCD up & running
✅ Project + Target Cluster configured
✅ kubectl installed
```


```bash
export KUBECONFIG=~/.kube/<kubeconfig> # EXAMPLE - CHANGE TO YOURS
export CLUSTER_NAME=default  # EXAMPLE - CHANGE TO YOURS
export DOMAIN=$(kubectl get nodes -o json | jq -r '.items[] | select(.metadata.labels."ingress-ready" == "true") | .status.addresses[] | select(.type == "InternalIP") | .address').nip.io
export HOSTNAME=vault
export ISSUERKIND=$(kubectl get clusterissuer -o json | jq -r '.items[].metadata.name')
export SERVER_URL=$(awk '/server:/ {print $2}' ${KUBECONFIG})

kubectl apply -f - <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: vault
  namespace: argocd
spec:
  destination:
    name: ''
    namespace: vault
    server: https://kubernetes.default.svc
  source:
    path: ''
    repoURL: registry-1.docker.io
    targetRevision: 1.7.0
    chart: bitnamicharts/vault
    helm:
      values: |
        server:
          ingress:
            enabled: true
            ingressClassName: nginx # EXAMPLE - CHANGE TO YOURS
            annotations:
              cert-manager.io/${ISSUERKIND}: "selfsigned" # EXAMPLE - CHANGE TO YOURS
            hostname: ${HOSTNAME}.${DOMAIN}
            tls: true
        injector:
          enabled: true
          serviceAccount:
            automountServiceAccountToken: true
  sources: []
  project: ${CLUSTER_NAME}
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
    automated: null
EOF
```

</details>



## UNSEAL VAULT

<details><summary><b>UNSEAL w/ KUBECTL</b></summary>

```bash
# LOG FULL OUTPUT TO FILE
LOG_FILE="vault-init-dev.log"

# RUN INIT AND CAPTURE OUTPUT
INIT_OUTPUT=$(kubectl -n vault exec vault-server-0 -- vault operator init -key-shares=5 -key-threshold=3)
echo "${INIT_OUTPUT}" > "${LOG_FILE}"

# EXTRACT UNSEAL KEYS
UNSEAL_KEYS=($(echo "${INIT_OUTPUT}" | grep "Unseal Key" | awk '{print $NF}'))

# EXTRACT INITIAL ROOT TOKEN (OPTIONAL)
ROOT_TOKEN=$(echo "${INIT_OUTPUT}" | grep "Initial Root Token" | awk '{print $NF}')

# LOG PARSED VALUES
{
  echo ""
  echo "PARSED UNSEAL KEYS:"
  for key in "${UNSEAL_KEYS[@]}"; do
    echo "$key"
  done

  echo ""
  echo "INITIAL ROOT TOKEN:"
  echo "$ROOT_TOKEN"
} >> "$LOG_FILE"

# OUTPUT PATH TO LOG
echo "Vault init details logged to: $LOG_FILE"

# UNSEAL VAULT WITH THE FIRST 3 KEYS
for i in {0..2}; do
  echo "Unsealing with key ${i}..."
  kubectl -n vault exec vault-server-0 -- vault operator unseal "${UNSEAL_KEYS[$i]}"
done
```

</details>

## APPLY VAULT CONFIGURATION

```bash
REQUIREMENTS:
✅ Kind Cluster w/ conifgured CNI/Cert-Manager/Ingress Controller
✅ Vault deployed + unsealed + token
✅ terrafom installed
```

<details><summary><b>CREATE/EDIT TERRAFORM FILES</b></summary>

```bash
cat <<EOF > vault-setup.tf
module "vault-secrets-setup" {
  source                   = "github.com/stuttgart-things/vault-base-setup"
  kubeconfig_path          = var.kubeconfig_path
  context                  = var.context
  vault_addr               = var.vault_addr
  cluster_name             = var.cluster_name
  createDefaultAdminPolicy = true
  csi_enabled              = false
  vso_enabled              = false
  enableApproleAuth        = true
  skip_tls_verify          = true
  approle_roles            = var.approle_roles
  secret_engines           = var.secret_engines
  kv_policies              = var.kv_policies
}

  output "role_ids" {
    description = "Role IDs from the vault approle module"
    value       = module.vault-secrets-setup.role_id
  }

  output "secret_ids" {
    description = "Secret IDs from the vault approle module"
    value       = module.vault-secrets-setup.secret_id
    sensitive   = true
  }

  variable "kubeconfig_path" {
    type        = string
    description = "Path to the kubeconfig file"
  }

  variable "context" {
    type        = string
    description = "Kubernetes context to use"
  }

  variable "vault_addr" {
    type        = string
    description = "Address of the Vault server"
  }

  variable "cluster_name" {
    type        = string
    description = "Name of the Kubernetes cluster"
  }

  variable "approle_roles" {
    type = list(object({
      name           = string
      token_policies = list(string)
    }))
  }

  variable "secret_engines" {
    type = list(object({
      path        = string
      name        = string
      description = string
      data_json   = string
    }))
  }

  variable "kv_policies" {
    type = list(object({
      name         = string
      capabilities = string
    }))
  }
EOF
```

```bash
cat <<EOF > terraform.tfvars.json
{
  "approle_roles": [
    {
      "name": "test",
      "token_policies": ["cloud"]
    }
  ],
  "secret_engines": [
    {
      "path": "cloud",
      "name": "test",
      "description": "test app secrets",
      "data_json": "{\"username\": \"andre\", \"password\": \"test123\"}"
    }
  ],
  "kv_policies": [
    {
      "name": "cloud",
      "capabilities": "path \"cloud/data/test\" {\n  capabilities = [\"create\", \"read\", \"update\", \"patch\", \"list\"]\n}"
    }
  ]
}
EOF
```

</details>

<details><summary><b>OPTIONAL: INSTALL VAULT PUCB CERT ON OS</b></summary>

```bash
# UBUNTU24

# GET/EXTRACT SECRET FROM CLUSTER
kubectl -n vault get secret vault.172.18.0.5.nip.io-tls -o json | jq -r '.data["ca.crt"]' | base64 --decode > /tmp/vault.172.18.0.5.nip.io.crt

# INSTALL CERT
sudo cp vault.172.18.0.5.nip.io.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# CHECK
ls /etc/ssl/certs/ | grep vault.172.18.0.5.nip.io # -> expected to find vault.172.18.0.5.nip.io.pem file
```

</details>

<details><summary><b>EXECUTE TERRAFORM</b></summary>

```bash
export KUBECONFIG=~/.kube/vault-cluster-config # aDD PATH TO KUBECONFIG VAULT IS DEPLYOED ON
LOG_FILE="vault-init-dev.log" # MUST EXIST (FROM UNSEAL)

CONTEXT=$(kubectl config current-context)
NAME=$(kubectl config view -o json | jq -r ".contexts[] | select(.name==\"$CONTEXT\") | .name")
CLUSTER=$(kubectl config view -o json | jq -r ".contexts[] | select(.name==\"$CONTEXT\") | .context.cluster")
DOMAIN=$(echo $(kubectl get nodes -o json | jq -r '.items[] | select(.metadata.labels."ingress-ready" == "true") | .status.addresses[] | select(.type == "InternalIP") | .address').nip.io)

export TF_VAR_kubeconfig_path=${KUBECONFIG}
export TF_VAR_context=${NAME}
export TF_VAR_vault_addr=https://vault.${DOMAIN}
export TF_VAR_cluster_name=${CLUSTER}
export VAULT_TOKEN=$(grep -oE '\bhvs\.[A-Za-z0-9_-]{24,}\b' ${LOG_FILE} | head -n 1)

terraform init

terraform apply --auto-approve
terraform output -json >> ${LOG_FILE}
cat ${LOG_FILE}
```

</details>

</details>

## VAULT USAGE

<details><summary><b>LOOKUP SECRETS w/ ANSIBLE</b></summary>

### APPROLE

```yaml
# VAULT EXPORTS 
export VAULT_AUTH_METHOD=approle
export VAULT_ADDR=https://vault.example.com
export VAULT_SECRET_ID=<secretID>
export VAULT_ROLE_ID=<roleID>

cat <<EOF > test-vault-lookup-approle.yaml
---
- hosts: localhost
  become: true

  environment:
    REQUESTS_CA_BUNDLE: ""

  vars:
    vault_approle_id: "{{ lookup('env', 'VAULT_ROLE_ID') }}"
    vault_approle_secret: "{{ lookup('env', 'VAULT_SECRET_ID') }}"
    vault_url: "{{ lookup('env', 'VAULT_ADDR') }}"
    vault_auth_method: "{{ lookup('env', 'VAULT_AUTH_METHOD') }}"
    test_username: "{{ lookup('community.hashi_vault.hashi_vault', 'secret=cloud/data/test:username validate_certs=false auth_method={{ vault_auth_method }} role_id={{ vault_approle_id }} secret_id={{ vault_approle_secret }} url={{ vault_url }}') }}"
    test_password: "{{ lookup('community.hashi_vault.hashi_vault', 'secret=cloud/data/test:password validate_certs=false auth_method={{ vault_auth_method }} role_id={{ vault_approle_id }} secret_id={{ vault_approle_secret }} url={{ vault_url }}') }}"

  tasks:
    - name: Show vault secret user
      debug:
        var: test_username
    - name: Show vault secret pw
      debug:
        var: test_password
EOF
```

```bash
ansible-playbook test-vault-lookup-approle.yaml -vv
```

### TOKEN

```yaml
# VAULT EXPORTS 
export VAULT_TOKEN=<TOKEN>
export VAULT_AUTH_METHOD=token
export VAULT_ADDR=https://vault.example.com

cat <<EOF > test-vault-lookup-token.yaml
---
- hosts: localhost
  become: true

  environment:
    REQUESTS_CA_BUNDLE: ""

  vars:
    vault_token: "{{ lookup('env', 'VAULT_TOKEN') }}"
    vault_url: "{{ lookup('env', 'VAULT_ADDR') }}"
    vault_auth_method: "{{ lookup('env', 'VAULT_AUTH_METHOD') }}"
    test_username: "{{ lookup('community.hashi_vault.hashi_vault', 'secret=cloud/data/test:username validate_certs=false token={{ vault_token }} auth_method={{ vault_auth_method }} url={{ vault_url }}') }}"
    test_password: "{{ lookup('community.hashi_vault.hashi_vault', 'secret=cloud/data/test:password validate_certs=false token={{ vault_token }} auth_method={{ vault_auth_method }} url={{ vault_url }}') }}"

  tasks:
    - name: Show vault secret user
      debug:
        var: test_username
    - name: Show vault secret pw
      debug:
        var: test_password
EOF
```

```bash
ansible-playbook test-vault-lookup-token.yaml -vv
```

</details>

<details><summary><b>ARGOCD VAULT PLUGIN</b></summary>

</details>

