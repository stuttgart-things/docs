+++
weight = 10
+++
{{< slide id=backup >}}

## BACK UP

- Stateful application data (e.g., databases using persistent volumes)
- Cluster state (e.g., etcd backup)
- Namespace or resource-level (e.g., using kubectl to export resource definitions)

---

## STACKEHOLDER

- DEV: APPLICATION
- PLATFORM: BACKUP-SW
- INFRASTRUCTURE: STORAGE-SYSTEMS

---

## USE-CASES

- APPLICATION/NAMESPACE
- PVCS
- VOLUMESNAPSHOTS
- (REDIRECTED) RESTORES
- CROSS NAMESPACE/CLUSTER RESTORES (REWRITES)
- SCHEDULES
- CONFIGURATION AS CODE

<br>
