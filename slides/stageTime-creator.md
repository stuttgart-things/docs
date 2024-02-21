# /STAGETIME-CREATOR
--
## SERVICE
* POLLS REDIS FOR TASKS/RESOURCES TO CREATE (STREAMS) <!-- .element: class="fragment fade-up" -->
* READS PIPELINERUNS FROM REDIS (JSON) <!-- .element: class="fragment fade-up" -->
* CREATES PIPELINERUNS ON CLUSTER <!-- .element: class="fragment fade-up" -->
--
## /REDIS-STREAMS


--
## /REDIS-STREAMS

--
# HELM
* Helm is a package manager for Kubernetes applications that includes templating and lifecycle management functionality <!-- .element: class="fragment fade-up" -->
* A chart is just a template for creating and deploying applications on Kubernetes using Helm <!-- .element: class="fragment fade-up" -->
--
https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F415d986e-939a-4773-a022-e7d42296e1eb_380x222.png

https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6cf41a23-e1cb-41cb-b53a-0e706baf9a76_562x212.png


```
apiVersion: v2
name: stagetime-creator
description: Helm chart for Kubernetes
type: application
version: v0.1.100
appVersion: v0.1.100
dependencies:
  - name: sthings-helm-toolkit
    version: 2.4.58
    repository: oci://eu.gcr.io/stuttgart-things
```

```
{{- $envVar := . -}}
{{ include "sthings-helm-toolkit.deployment" (list $envVar) }}
```

```
deployment:
  name: stagetime-creator
  volumes:
    manifest-templates:
      volumeKind: configMap
  labels:
    app: stagetime-creator
  selectorLabels:
    app: stagetime-creator
  allowPrivilegeEscalation: "false"
  privileged: "false"
  runAsNonRoot: "false"
```