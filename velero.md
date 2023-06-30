# stuttgart-things/docs/velero

## CMD/CLI SNIPPETS
```
kubectl get volumesnapshotlocations.velero.io -A
velero backup-location get
velero backup create metricbeat --include-namespaces metricbeat
velero restore create nginx --from-backup nginx-backup5
kubectl delete volumesnapshotlocation artifacts -n velero
```

## BACKUP/RESTORE PostgresDB

### DEPLOY PostgresDB

```
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

  podAnnotations:
    backup.velero.io/backup-volumes: backup
    pre.hook.backup.velero.io/timeout: 5m
    pre.hook.restore.velero.io/timeout: 5m
    post.hook.restore.velero.io/command: '["/bin/bash", "-c", "sleep 1m && PGPASSWORD=Ue1Fsc5Lgd
        pg_restore -U postgres -d postgres --clean < /scratch/backup.psql"]'
    pre.hook.backup.velero.io/command: '["/bin/bash", "-c", "export PGPASSWORD=Ue1Fsc5Lgd
        && sleep 1m && pg_dump -U postgres -d postgres -F c -f /scratch/backup.psql"]'
EOF

helm upgrade --install postgresql bitnami/postgresql -n postgres --values postgres-velero.yaml
```

### CREATE TESTDATA ON PostgresDB

```
export POSTGRES_PASSWORD=$(kubectl get secret --namespace postgres postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)

kubectl run postgresql-client --rm --tty -i --restart='Never' --namespace postgres --image docker.io/bitnami/postgresql:15.2.0-debian-11-r14 --env="PGPASSWORD=$POSTGRES_PASSWORD" --command -- psql --host postgresql -U postgres -d postgres -p 5432

CREATE TABLE phonebook(phone VARCHAR(32), firstname VARCHAR(32), lastname VARCHAR(32), address VARCHAR(64));

INSERT INTO phonebook(phone, firstname, lastname, address) VALUES('+1 123 456 7890', 'John', 'Doe', 'North America'); 
SELECT * FROM phonebook ORDER BY lastname;

```

### CREATE BACKUP 

```
velero backup create pgb18-restic --include-namespaces postgres
```

### RESTORE BACKUP 

```
velero restore create pgb18 --from-backup pgb18-restic --namespace-mappings postgres:new5

export POSTGRES_PASSWORD=$(kubectl get secret --namespace new5 postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)

kubectl run postgresql-client --rm --tty -i --restart='Never' --namespace new5 --image docker.io/bitnami/postgresql:15.2.0-debian-11-r14 --env="PGPASSWORD=$POSTGRES_PASSWORD" --command -- psql --host postgresql -U postgres -d postgres -p 5432

SELECT * FROM phonebook ORDER BY lastname;
````


## LINKS
```
https://www.ntchosting.com/encyclopedia/databases/postgresql/
https://velero.io/docs/v1.10/backup-hooks/
https://github.com/vmware-tanzu/velero/blob/main/examples/nginx-app/with-pv.yaml
```
