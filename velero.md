# stuttgart-things/docs/velero

<details><summary><b>CLI SNIPPETS</b></summary>

```bash
velero backup-location get
velero backup create metricbeat --include-namespaces metricbeat
velero restore create nginx --from-backup nginx-backup5
kubectl get volumesnapshotlocations.velero.io -A
kubectl delete volumesnapshotlocation artifacts -n velero
```

</details>

<details><summary><b>VELERO DEPLOYMENT</b></summary>

```bash
helm repo add tanzu https://vmware-tanzu.github.io/helm-charts
helm repo update
````

```bash
INGRESS_HOSTNAME_MINIO: artifacts
INGRESS_DOMAIN_MINIO: texas.sthings-vsphere.labul.sva.de
MINIO_ADMIN_USER=sthings
MINIO_ADMIN_PASSWORD=<SECRET>
CA_BUNDLE=<CA_BUNDLE>

cat <<EOF > velero.yaml
deployNodeAgent: true
credentials:
  useSecret: true
  name: minio
  secretContents:
    cloud: |
      [default]
      aws_access_key_id=${MINIO_ADMIN_USER}
      aws_secret_access_key=${MINIO_ADMIN_PASSWORD}
configuration:
  features: EnableCSI
  backupStorageLocation:
    - name: default
      provider: aws
      bucket: velero
      default: true
      caCert: ${CA_BUNDLE}
      config:
        region: minio
        s3ForcePathStyle: true
        s3Url: https://${INGRESS_HOSTNAME_MINIO}.${INGRESS_DOMAIN_MINIO}
        publicUrl: https://${INGRESS_HOSTNAME_MINIO}.${INGRESS_DOMAIN_MINIO}
  volumeSnapshotLocation:
    - name: artifacts
      provider: aws
      bucket: velero
      default: true
      caCert: ${CA_BUNDLE}
      config:
        region: minio
        s3ForcePathStyle: true
        s3Url: https://${INGRESS_HOSTNAME_MINIO}.${INGRESS_DOMAIN_MINIO}
        publicUrl: https://${INGRESS_HOSTNAME_MINIO}.${INGRESS_DOMAIN_MINIO}
initContainers:
  - name: velero-plugin-for-aws
    image: velero/velero-plugin-for-aws:v1.9.0
    volumeMounts:
      - mountPath: /target
        name: plugins
EOF
```

```bash
helm upgrade --install velero tanzu/velero --version 5.4.1 --values velero.yaml -n velero --create-namespace
```

</details>

<details><summary><b>VELERO SCHEDULES</b></summary>

### Create scheduled backup /w velero every day at 4am retention for 72h

`velero schedule create pgsched --schedule="0 4 * * *" --include-namespaces postgres --ttl 72h`

```bash
velero schedule get
NAME      STATUS    CREATED                         SCHEDULE    BACKUP TTL   LAST BACKUP   SELECTOR   PAUSED
pgsched   Enabled   2024-03-05 10:35:06 +0100 CET   0 4 * * *   72h0m0s      n/a           <none>     false
```

### Create Ad Hoc backup from schedule

`velero backup create --from-schedule pgsched`

### Check backups

```bash
velero backup get
NAME                     STATUS      ERRORS   WARNINGS   CREATED                         EXPIRES   STORAGE LOCATION   SELECTOR
pgsched-20240305093755   Completed   0        0          2024-03-05 10:37:55 +0100 CET   2d        default            <none>
```

### finding, after test backups were created every 5min and thus the expired backups start to stack
#### https://velero.io/docs/v1.9/how-velero-works/
The effects of expiration are not applied immediately, they are applied when the gc-controller runs its reconciliation loop every hour.

</details>

<details><summary><b>BACKUP/RESTORE: POSTGRESDB</b></summary>

### DEPLOY PostgresDB

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

cat <<EOF > postgres-velero.yaml

POSTGRES_PASSWORD=<SECRET>

primary:
  extraVolumes:
  - name: backup
    emptyDir: {}
  extraVolumeMounts:
  - name: backup
    mountPath: /scratch
  persistence:
    storageClass: 56-nfs-sc

  podAnnotations:
    backup.velero.io/backup-volumes: backup
    pre.hook.backup.velero.io/timeout: 5m
    pre.hook.restore.velero.io/timeout: 5m
    post.hook.restore.velero.io/command: '["/bin/bash", "-c", "sleep 1m && PGPASSWORD=${POSTGRES_PASSWORD} \
        pg_restore -U postgres -d postgres --clean < /scratch/backup.psql"]'
    pre.hook.backup.velero.io/command: '["/bin/bash", "-c", "export PGPASSWORD=${POSTGRES_PASSWORD} \
        && sleep 1m && pg_dump -U postgres -d postgres -F c -f /scratch/backup.psql"]'
EOF

helm upgrade --install postgresql bitnami/postgresql -n postgres --values postgres-velero.yaml --version 14.2.3
```

### CREATE TESTDATA ON PostgresDB

```bash
# GET THE POSTGRES PASSWORD ON YOUR LOCAL ENV
export POSTGRES_PASSWORD=$(kubectl get secret --namespace postgres postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)

# RUN A POSTGRES CLIENT IN THE NAMESPACE
kubectl run postgresql-client --rm --tty -i --restart='Never' \
--namespace postgres --image docker.io/bitnami/postgresql:16.2.0-debian-12-r5 \
--env="PGPASSWORD=$POSTGRES_PASSWORD" --command \
-- psql --host postgresql postgres -d postgres -p 5432

# CREATE A TABLE
CREATE TABLE phonebook(phone VARCHAR(32), firstname VARCHAR(32), lastname VARCHAR(32), address VARCHAR(64));

# List the databases
\l, \l+

# List tables in the current database
\dt, \dt+

# INSERT TEST DATA
INSERT INTO phonebook(phone, firstname, lastname, address) VALUES('+1 123 456 7890', 'John', 'Doe', 'North America');

# TEST QUERY
SELECT * FROM phonebook ORDER BY lastname;
```

### CREATE BACKUP

```bash
velero backup create pgb18-restic --include-namespaces postgres --wait
```

### SIMULATE DISASTER

```bash
kubectl delete ns postgres
```

### RESTORE BACKUP

```bash
velero restore create pgb18 --from-backup pgb18-restic --namespace-mappings postgres:new5

export POSTGRES_PASSWORD=$(kubectl get secret --namespace new5 postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)

kubectl run postgresql-client --rm --tty -i --restart='Never' --namespace new5 --image docker.io/bitnami/postgresql:16.2.0-debian-12-r5 --env="PGPASSWORD=$POSTGRES_PASSWORD" --command -- psql --host postgresql -U postgres -d postgres -p 5432

SELECT * FROM phonebook ORDER BY lastname;
```

</details>

<details><summary><b>BACKUP/RESTORE: FILE ON PV</b></summary>

### CREATE POD /W VOLUME
```bash
---
apiVersion: v1
kind: Namespace
metadata:
  name: csi-app
---
kind: Pod
apiVersion: v1
metadata:
  namespace: csi-app
  name: csi-nginx
spec:
  nodeSelector:
    kubernetes.io/os: linux
  containers:
    - image: nginx
      name: nginx
      command: [ "sleep", "1000000" ]
      volumeMounts:
        - name: nfsdisk01
          mountPath: "/mnt/nfsdisk"
  volumes:
    - name: nfsdisk01
      persistentVolumeClaim:
        claimName: pvc-nfsdisk
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  namespace: csi-app
  name: pvc-nfsdisk
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Mi
  storageClassName: 56-nfs-sc
```

### CREATE TESTDATA ON VOLUME

```bash
kubectl -n csi-app exec -ti csi-nginx -- bash -c 'echo -n "Hello from Velero!" >> /mnt/nfsdisk/hello'
```

### CREATE BACKUP

```bash
velero backup create csi-backup --include-namespaces csi-app --wait
```

### SIMULATE DISASTER

```bash
kubectl delete ns csi-app
```

### RESTORE BACKUP

```bash
velero restore create csi-restore --from-backup csi-backup
kubectl -n csi-app exec -ti csi-nginx -- bash -c 'cat /mnt/nfsdisk/hello'
```

</details>

<details><summary><b>LINKS</b></summary>

[raspi-longhorn-velero](https://picluster.ricsanfre.com/docs/backup)
[postgresql-velero](https://www.ntchosting.com/encyclopedia/databases/postgresql)
[velero-backup-hooks](https://velero.io/docs/v1.10/backup-hooks)
[tanzu-nginx-app](https://github.com/vmware-tanzu/velero/blob/main/examples/nginx-app/with-pv.yaml)

</details>
