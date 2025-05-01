# KUBERNETES BACKUP
--
### KUBERNETES BACKUP
<!-- .slide: data-transition="zoom" -->
---
# /AGENDA
* KUBERNETES BACKUP <!-- .element: class="fragment fade-up" -->
* VELERO <!-- .element: class="fragment fade-up" -->
* KASTEN (K10)<!-- .element: class="fragment fade-up" -->
* COMPARISON <!-- .element: class="fragment fade-up" -->
---
# /BACKUP
[<img src="https://miro.medium.com/v2/resize:fit:934/0*xgCTrk6NbQGdv_qF.jpeg" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
---
# /WHAT TO BACKUP
* Stateful application data (e.g., databases using persistent volumes).
* Cluster state (e.g., etcd backup).
* Namespace or resource-level (e.g., using kubectl to export resource definitions).
---
# /WHAT TO RESTORE


---
# /VELERO
* open-source Kubernetes backup/restore tool maintained by VMWare
* complete application backups, disaster recovery, and Kubernetes migration
--
# /EXECUTION
* On-demand 
* Scheduled 
--
# /BACKUP-EXAMPLE

```
velero backup create demo-backup --include-namespaces demo-ns
```
--
## RESTORE BACKUP (TO DIFFERENT NAMESPACE)

```
velero restore create demo-restore \
--from-backup demo-backup \
--namespace-mappings demo-ns:new-demo-ns
```


---
# /COMPARISON

| Feature                       | Kasten                                                                 | Velero                                                                 |
|-------------------------------|-----------------------------------------------------------------------|-----------------------------------------------------------------------|
| **Pricing & Support**         | Enterprise + 24/7 dedicated support. Free version limits deployment to 5 nodes | Open-source and free to use |
