# stuttgart-things/docs/minio

## SNIPPETS

<details><summary><b>VAULT-KES-MINIO</b></summary>

[DOC](https://blog.min.io/minio-operator-with-kes-backed-by-vault)

#### DEPLOY MINIO OPERATOR

```bash
kubectl apply -k github.com/minio/operator
```

#### VAULT UNSEAL

```bash
helm repo add unseal https://pytoshka.github.io/vault-autounseal

cat << EOF> unseal-values.yaml
vault_label_selector: app.kubernetes.io/component=server
EOF

helm upgrade --install vault-autounseal \
unseal/vault-autounseal \
--set=settings.vault_url=http://vault-server.vault.svc:8200 \
--values unseal-values.yaml \
-n vault
```

#### VAULT CONFIG

```bash
kubectl get po -n vault --show-labels

kubectl -n vault exec -it vault-server-0 -- sh

vault login
vault secrets enable -version=1 kv

vault policy write kes-policy - <<EOF
path "kv/*" {
  capabilities = [ "create", "read", "delete" ]
}
EOF

vault auth enable approle

vault write auth/approle/role/kes-server token_num_uses=0 secret_id_num_uses=0 period=5m
vault write auth/approle/role/kes-server policies=kes-policy

vault read auth/approle/role/kes-server/role-id
vault write -f auth/approle/role/kes-server/secret-id

#id: 986d855b-d315-2939-13c9-8c69f5097772
#secret: 3eb58365-7359-f3ed-f2b2-309a14f8a8b6
```

#### KES CONFIGURATION

```bash
git clone https://github.com/minio/operator.git
code operator/examples/kustomization/tenant-kes-encryption/kes-configuration-secret.yaml
```

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: kes-configuration
  namespace: tenant-kms-encrypted
type: Opaque
stringData:
  server-config.yaml: |-
    version: v1
    address: :7373
    admin:
      identity: _ # Effectively disabled since no root identity necessary.
    tls:
      key: /tmp/kes/server.key   # Path to the TLS private key
      cert: /tmp/kes/server.crt # Path to the TLS certificate
      proxy:
        identities: []
        header:
          cert: X-Tls-Client-Cert
    policy:
      my-policy:
        allow:
        - /v1/api
        - /v1/key/create/*
        - /v1/key/generate/*
        - /v1/key/decrypt/*
        - /v1/key/bulk/decrypt/*
        identities:
        - ${MINIO_KES_IDENTITY}
    cache:
      expiry:
        any: 5m0s
        unused: 20s
    log:
      error: on
      audit: off
    keystore:
      vault:
        endpoint: "http://vault-server.vault.svc.cluster.local:8200"
        namespace: "default"
        prefix: "my-minio"    # An optional K/V prefix. The server will store keys under this prefix.
        approle:
          id: 986d855b-d315-2939-13c9-8c69f5097772
          secret: 3eb58365-7359-f3ed-f2b2-309a14f8a8b6
          retry: 15s
        tls:
          key: ""
          cert: ""
          ca: ""
        status:
          ping: 10s
```

```bash
code examples/kustomization/base/tenant.yaml # change e.g. storageClassName

kubectl apply -k operator/examples/kustomization/tenant-kes-encryption

kubectl get pods -n minio-operator                       
kubectl get pods -n tenant-kms-encrypted
```      

#### TEST KES ENCRYPTION

```bash
kubectl -n tenant-kms-encrypted run -it --rm mc   --image=minio/mc:RELEASE.2025-05-21T01-59-54Z-cpuv1   --restart=Never   --command -- sh

mc alias set minio https://myminio-hl.tenant-kms-encrypted.svc.cluster.local:9000 console console12
3

mc admin kms key create minio encrypted-bucket-key
mc mb minio/encryptedbucket

mc admin kms key status minio encrypted-bucket-key

echo "Hello" >> file1.txt

mc ls minio/encryptedbucket
mc cp file1.txt minio/encryptedbucket

mc cat minio/encryptedbucket/file1.txt

mc stat minio/encryptedbucket/file1.txt
```

</details>

<details><summary><b>INSTALL MINIO-CLI (MC)</b></summary>

```bash
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/
```

</details>


<details><summary><b>USE MINIO PLAY FOR TESTING</b></summary>

```bash
mkdir -p ~/.mc/
cat << EOF> ~/.mc/config.json
{
  "version": "10",
  "aliases": {
    "play": {
      "url": "https://play.min.io",
      "accessKey": "minioadmin",
      "secretKey": "minioadmin",
      "api": "s3v4",
      "path": "auto"
    }
  }
}
EOF
```

```bash
# ZIP A TEST FOLDER (JUST FOR REFERENCE - NOT REQUIRED)
zip -r toolkit.zip toolkit/

# LIST BUCKET
mc ls play

# CREATE A BUCKET
mc mb play/ankit

# COPY TO BUCKET
mc cp toolkit.zip play/ankit

# COPY FROM BUCKET
mc cp play/andreu/xlanguage.png ./bla.png
```

</details>


<details><summary><b>MC CONFIG (EXAMPLE)</b></summary>

```json
cat << EOF> ~/.mc/config.json
{
  "version": "10",
  "aliases": {
    "artifacts-labda": {
      "url": "https://artifacts.app.4sthings.tiab.ssc.sva.de",
      "accessKey": "<REPLACEME>",
      "secretKey": "<REPLACEME>",
      "api": "s3v4",
      "path": "auto"
    },
    "labul-automation": {
      "url": "https://artifacts.automation.sthings-vsphere.labul.sva.de",
      "accessKey": "<REPLACEME>",
      "secretKey": "<REPLACEME>",
      "api": "s3v4",
      "path": "auto"
    }
  }
}
EOF
```

</details>

<details><summary><b>MC COMMAND SNIPPETS</b></summary>

```bash
mc anonymous set public artifacts-labda/roles # SET BUCKET TO PUBLIC
mc ls artifacts-labda # LIST BUCKETS
```

</details>

## RCLONE

<details><summary>RCLONE CONFIG (EXAMPLE)</summary>

```bash
mdkir -p ${HOME}/.config/rclone/
cat <<EOF > ${HOME}/.config/rclone/rclone.conf
[labul-automation]
type = s3
provider = Minio
access_key_id = <REPLACEME>
secret_access_key = <REPLACEME>
endpoint = https://artifacts.automation.sthings-vsphere.labul.sva.de:443
acl = private
region = us-central-1
EOF
```

</details>

<details><summary>RCLONE COMMAND SNIPPETS</summary>

```bash
rclone ls labul-automation:vsphere-vm
rclone sync labul-automation:vsphere-vm . # sync bucket to current (local) dir
```

</details>
