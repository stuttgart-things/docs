# stuttgart-things/docs/velero

https://picluster.ricsanfre.com/docs/backup/

## VOLUMESNAPSHOTS

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/master/client/config/crd/snapshot.storage.k8s.io_volumesnapshotclasses.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/master/client/config/crd/snapshot.storage.k8s.io_volumesnapshotcontents.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes-csi/external-snapshotter/master/client/config/crd/snapshot.storage.k8s.io_volumesnapshots.yaml
```

```yaml
kind: VolumeSnapshotClass
apiVersion: snapshot.storage.k8s.io/v1
metadata:
  name: longhorn-snapshot-vsc
  labels:
    velero.io/csi-volumesnapshot-class: "true"
driver: driver.longhorn.io
deletionPolicy: Delete
parameters:
  type: bak
```


## CMD/CLI SNIPPETS

```bash
kubectl get volumesnapshotlocations.velero.io -A
velero backup-location get
velero backup create metricbeat --include-namespaces metricbeat
velero restore create nginx --from-backup nginx-backup5
kubectl delete volumesnapshotlocation artifacts -n velero
```

## BACKUP/RESTORE PostgresDB

### DEPLOY PostgresDB

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

cat <<EOF > postgres-velero.yaml
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
    post.hook.restore.velero.io/command: '["/bin/bash", "-c", "sleep 1m && PGPASSWORD=$POSTGRES_PASSWORD \
        pg_restore -U postgres -d postgres --clean < /scratch/backup.psql"]'
    pre.hook.backup.velero.io/command: '["/bin/bash", "-c", "export PGPASSWORD=$POSTGRES_PASSWORD \
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
velero backup create pgb18-restic --include-namespaces postgres
```

### RESTORE BACKUP

```bash
velero restore create pgb18 --from-backup pgb18-restic --namespace-mappings postgres:new5

export POSTGRES_PASSWORD=$(kubectl get secret --namespace new5 postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)

kubectl run postgresql-client --rm --tty -i --restart='Never' --namespace new5 --image docker.io/bitnami/postgresql:16.2.0-debian-12-r5 --env="PGPASSWORD=$POSTGRES_PASSWORD" --command -- psql --host postgresql -U postgres -d postgres -p 5432

SELECT * FROM phonebook ORDER BY lastname;
````


## LINKS

```
https://www.ntchosting.com/encyclopedia/databases/postgresql/
https://velero.io/docs/v1.10/backup-hooks/
https://github.com/vmware-tanzu/velero/blob/main/examples/nginx-app/with-pv.yaml
```
