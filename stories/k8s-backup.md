# HOW TO BACKUP ON KUBERNETES

```bash
Key Features:
✅ Deploy + Configure State of the Art backup tools
✅ Multi-Cluster Backup-Management
```

## VELERO

<details><summary>(OPTIONAL) DEPLOY MINIO (KIND)</summary>

## DEPLOY MINIO

this step assumes you have a kind cluster running with enabled cni, ingress-controller and cert-manager. 
The example could be also used on a different kind of kubernetes cluster with configured cert-manager and ingress-controller.

```bash
# USE FOR KIND - NIP.IO
INGRESS_DOMAIN=$(kubectl get nodes -l node-role.kubernetes.io/control-plane -o jsonpath='{.items[0].status.addresses[?(@.type=="InternalIP")].address}').nip.io

cat <<EOF > minio.yaml
---
helmfiles:
  - path: git::https://github.com/stuttgart-things/helm.git@apps/minio.yaml
    values:
      - namespace: minio
      - clusterIssuer: selfsigned
      - issuerKind: cluster-issuer
      - domain: \${INGRESS_DOMAIN}
      - ingressClassName: nginx
      - rootUser: adminadmin
      - rootPassword: adminadmin
      - hostnameConsole: artifacts-console
      - hostnameApi: artifacts
      - storageClass: standard
EOF

# REPLACE
sed -i "s|\\\${INGRESS_DOMAIN}|${INGRESS_DOMAIN}|g" minio.yaml

helmfile apply -f minio.yaml
```

## CREATE A BUCKET FOR VELERO

```bash
kubectl get ingress -A | grep console
# USE WITH BROWSER AND CREATE BUCKET: VELERO
```

</details>

<details><summary>INSTALL VELERO CLI</summary>

```bash

```

</details>

<details><summary>DEPLOY VELERO (KIND)</summary>

```bash
# OPTIONAL: GET MINIO CERT (IF YOU DEPLOYED YOU'RE MINIO SELF-SIGNED)
kubectl get secret artifacts.172.18.0.10.nip.io-tls -n minio -o jsonpath='{.data.ca\.crt}' | base64 --decode > minio-ca.crt
PUB_CA=$(cat minio-ca.crt | base64 -w 0)

cat <<EOF > velero.yaml
---
helmfiles:
  - path: git::https://github.com/stuttgart-things/helm.git@infra/velero.yaml
    values:
      - namespace: velero
      - backupsEnabled: true
      - snapshotsEnabled: true
      - deployNodeAgent: true
      - s3StorageLocation: default
      - awsAccessKeyID: adminadmin
      - awsSecretAccessKey: adminadmin
      - s3Bucket: velero
      - s3CaCert: \${PUB_CA}
      - s3Location: artifacts.172.18.0.10.nip.io
      - imageAwsVeleroPlugin: velero/velero-plugin-for-aws:v1.11.1
EOF

# REPLACE
sed -i "s|\\\${PUB_CA}|${PUB_CA}|g" velero.yaml

# DEPLOY VELERO
helmfile sync -f velero.yaml

# CHECK STORAGE LOCATION
kubectl get Backupstoragelocations default -n velero
```

</details>

<details><summary>CREATE BACKUPS w/ VELERO</summary>

## CREATE TEST DATA
 
```bash
kubectl apply -f - <<EOF
---
apiVersion: v1
kind: Namespace
metadata:
  name: demo-ns
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: demo-ns
data:
  app.properties: |
    server.port=8080
    logging.level=INFO
  db.url: jdbc:postgresql://db:5432/app
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: env-config
  namespace: demo-ns
data:
  ENV: production
  API_KEY: "abc123"
EOF
```

## CREATE BACKUP

```bash
velero backup create demo-backup --include-namespaces demo-ns
```

## RESTORE BACKUP (TO DIFFERENT NAMESPACE)

```bash
velero restore create demo-restore \
--from-backup demo-backup \
--namespace-mappings demo-ns:new-demo-ns
```

</details>

## KASTEN(K10)

<details><summary>INSTALL CSI-SNAPSHOTTER </summary>

```bash
kubectl apply -k https://github.com/kubernetes-csi/external-snapshotter/client/config/crd
```

</details>

<details><summary>INSTALL CSI HOST-PATH DRIVER</summary>

```bash
git clone https://github.com/kubernetes-csi/csi-driver-host-path.git
bash csi-driver-host-path/deploy/kubernetes-1.31/deploy.sh 
kubectl apply -f csi-driver-host-path/examples/csi-storageclass.yaml
```

</details>

<details><summary>DEPLOY KASTEN (CLUSTER)</summary>

[htpasswd-generato](https://hostingcanada.org/htpasswd-generator/)

```bash
cat <<EOF > k10.yaml
---
ingress:
  create: true
  enabled: true
  class: nginx
  host: k10.automation.example.com
  tls:
    enabled: true
    secretName: k10-tls

auth:
  basicAuth:
    enabled: true
    htpasswd: sthings:$apr#...
EOF
```

```bash
helm repo add kasten https://charts.kasten.io/
helm upgrade --install k10 \
kasten/k10 \
--version 7.5.10 \
--values k10.yaml \
--namespace k10 \
--create-namespace
```

</details>

https://documentation.suse.com/trd/veeam/html/gs_rancher_veeam-kasten/index.html#id-installing-kasten-k10
https://patriciocerda.com/?p=1561
