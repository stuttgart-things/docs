# STAGETIME-OPERATOR
--

```yaml
---
apiVersion: stagetime.sthings.tiab.ssc.sva.de/v1beta1
kind: RevisionRun
metadata:
  labels:
    app.kubernetes.io/name: revisionrun
    app.kubernetes.io/managed-by: kustomize
    app.kubernetes.io/created-by: stagetime-operator
  name: revisionrun-simulation
spec:
  repository: stuttgart-things
  revision: ad3121246532123
  technologies:
    - id: test0
      kind: simulation
      resolver: revision=main
      params: scriptTimeout=10s
      canfail: false
    - id: test1
      kind: simulation
      resolver: revision=main
      params: scriptTimeout=25s
      canfail: true
```
--