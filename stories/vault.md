# VAULT

## DEPLOY VAULT
<details><summary><b>DEPLOY w/ ARGOCD</b></summary>

```bash
export KUBECONFIG=~/.kube/<kubeconfig> # EXAMPLE - CHANGE TO YOURS

CLUSTER_NAME=TEST_CLUSTER  # EXAMPLE - CHANGE TO YOURS

DOMAIN=$(echo $(kubectl get nodes -o json | jq -r '.items[] | select(.metadata.labels."ingress-ready" == "true") | .status.addresses[] | select(.type == "InternalIP") | .address').nip.io)
echo ${DOMAIN}

HOSTNAME=$(kubectl get nodes -o json | jq -r '.items[].metadata.labels."kubernetes.io/hostname"')
echo ${HOSTNAME}

ISSUERKIND=$(kubectl get clusterissuer -o json | jq -r '.items[].metadata.name')
echo $ISSUERKIND

SERVER_URL=$(awk '/server:/ {print $2}' ${KUBECONFIG})
echo ${SERVER_URL}
```

```yaml
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
    server: ${SERVER_URL}
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
              cert-manager.io/${ISSUERKIND}$: "ca-issuer" # EXAMPLE - CHANGE TO YOURS
            hostname: ${HOSTNAME}.${DOMAIN}
            tls: true

        injector:
          enabled: true
          serviceAccount:
            automountServiceAccountToken: true
  sources: []
  project: ${CLUSTER_NAME}$
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
    automated: null
EOF
```

</details>

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
