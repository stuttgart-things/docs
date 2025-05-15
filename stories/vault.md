# VAULT

## DEPLOY VAULT

<details><summary><b>DEPLOY w/ HELMFILE ON KIND</b></summary>

REQUIREMENTS:

✅ Kind CLuster w/ conifgured CNI/Cert-Manager/Ingress Controller
✅ helmfile, kubectl installed


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
