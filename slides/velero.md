+++
weight = 20
+++
{{< slide id=velero >}}

## /VELERO
* open-source Kubernetes backup/restore tool maintained by VMWare
* complete application backups, disaster recovery, and Kubernetes migration

---

# BACKUP/RESTORE-EXAMPLE

```
velero backup create demo-backup --include-namespaces demo-ns
```

```
velero restore create demo-restore \
--from-backup demo-backup \
--namespace-mappings demo-ns:new-demo-ns
```

---
