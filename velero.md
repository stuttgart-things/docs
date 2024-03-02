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

<details><summary><b>BACKUP/RESTORE PostgresDB</b></summary>
  
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
````
</details>

<details><summary><b>BACKUP/RESTORE filebased</b></summary>

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

## LINKS

```
https://www.ntchosting.com/encyclopedia/databases/postgresql/
https://velero.io/docs/v1.10/backup-hooks/
https://github.com/vmware-tanzu/velero/blob/main/examples/nginx-app/with-pv.yaml
```
