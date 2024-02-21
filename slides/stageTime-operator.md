# STAGETIME-OPERATOR
--
## USAGE
* WATCHES KIND REVISIONRUN <!-- .element: class="fragment fade-up"
* READS KIND REPO + PIPELINERUNTEMPLATE <!-- .element: class="fragment fade-up"
* TRIGGERS STAGETIME SERVER <!-- .element: class="fragment fade-up"
* STATUS FOR REVISIONRUN <!-- .element: class="fragment fade-up"
--
## REVISIONRUN-CR

```yaml
apiVersion: stagetime.sthings.tiab.ssc.sva.de/v1beta1
kind: RevisionRun
metadata:
  labels:
    app.kubernetes.io/name: revisionrun
  name: revisionrun-simulation
spec:
  repository: stuttgart-things
  #revision: ad3121246532123
  technologies:
    - id: image-build
      kind: docker
      resolver: revision=main
      params: scriptTimeout=10s
      canfail: false
```
--
## OPERTOR-FRAMWORK
*  <!-- .element: class="fragment fade-up"
*  <!-- .element: class="fragment fade-up"
*  <!-- .element: class="fragment fade-up"
*  <!-- .element: class="fragment fade-up"
--
## OPERTOR-FRAMWORK