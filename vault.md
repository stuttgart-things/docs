# VAULT

## USE VAULT W/ SECRETS CSI DRIVER

<details><summary><b>DEPLOY VAULT W/ CSI DRIVER ENABLED</b></summary>

```bash
helm repo add hashicorp https://helm.releases.hashicorp.com
helm repo update

cat <<EOF > vaul-values.yaml
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
