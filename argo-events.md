# stuttgart-things/docs/argo-events

## TERMINOLOGY

<details><summary><b>TABLE</b></summary>

https://www.atlantbh.com/implementing-ci-cd-pipeline-using-argo-workflows-and-argo-events/
https://github.com/argoproj/argo-events/blob/master/examples/event-sources/resource.yaml
https://siebjee.nl/posts/how-i-manage-elasticsearch/#setting-up-argo-events

</details>

## DEPLOYMENT

<details><summary><b>DEPLOYMENT + VALUES</b></summary>

```bash

```

</details>

## USECASE: TRIGGER MINIO BUCEKT TO WORKFLOW EVENTS

<details><summary>EVENTBUS</summary>

```yaml
apiVersion: argoproj.io/v1alpha1
kind: EventBus
metadata:
  name: minio
  namespace: argo-events
spec:
  nats:
    native:
      replicas: 3
      auth: none
```

</details>

<details><summary>MINIO SECRET</summary>

```yaml
---
kind: Secret
apiVersion: v1
metadata:
  name: artifacts-minio
  namespace: argo-events
stringData:
  accesskey: <ACCESS-KEY>
  secretkey: <SECRET-KEY>
```

</details>

<details><summary>CA CERTIFICATES</summary>

```yaml
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: ca-certificates
  namespace: argo-events
data:
  ca-certificates.crt: |-
    -----BEGIN CERTIFICATE-----
    MIIFijCCA3KgAwIBAgIUYeYPin86X #..
```

</details>

<details><summary>EVENTSOURCE</summary>

```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: EventSource
metadata:
  name: minio
  namespace: argo-events
spec:
  eventBusName: minio
  minio:
    example:
      bucket:
        name: modules
      endpoint: artifacts.automation.sthings-vsphere.labul.sva.de
      events:
        - s3:ObjectCreated:Put
        - s3:ObjectRemoved:Delete
      insecure: false
      accessKey:
        key: accesskey
        name: artifacts-minio
      secretKey:
        key: secretkey
        name: artifacts-minio
  template:
    container:
      env:
        - name: DEBUG_LOG
          value: "true"
      volumeMounts:
        - name: certs-volume
          mountPath: /etc/ssl/certs
    volumes:
      - name: certs-volume
        configMap:
          name: ca-certificates
```

</details>

<details><summary>SERVICE ACCOUNT</summary>

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  namespace: argo-events
  name: operate-workflow-sa
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: operate-workflow
  labels:
    rbac.authorization.k8s.io/aggregate-to-view: "true"
rules:
- apiGroups:
  - argoproj.io
  resources:
  - workflows
  - workflows/finalizers
  - workfloweventbindings
  - workfloweventbindings/finalizers
  - workflowtemplates
  - workflowtemplates/finalizers
  - cronworkflows
  - cronworkflows/finalizers
  - clusterworkflowtemplates
  - clusterworkflowtemplates/finalizers
  - workflowtaskresults
  - workflowtaskresults/finalizers
  verbs:
  - get
  - list
  - watch
  - create
- apiGroups:
    - ""
  resources:
    - pods
  verbs:
    - get
    - watch
    - patch
- apiGroups:
    - ""
  resources:
    - pods/log
  verbs:
    - get
    - watch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: operate-workflow
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: operate-workflow
subjects:
- kind: ServiceAccount
  name: operate-workflow-sa
  namespace: argo-events
```

</details>

<details><summary>SENSOR</summary>

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Sensor
metadata:
  name: minio
  namespace: argo-events
spec:
  eventBusName: minio
  template:
    serviceAccountName: operate-workflow-sa
    container:
      env:
        - name: DEBUG_LOG
          value: "true"
  dependencies:
    - name: test-dep
      eventSourceName: minio
      eventName: example
  triggers:
    - template:
        name: minio-workflow-trigger
        k8s:
          operation: create
          source:
            resource:
              apiVersion: argoproj.io/v1alpha1
              kind: Workflow
              metadata:
                generateName: artifact-workflow-2-
                # namespace: argo-workflows
              spec:
                serviceAccountName: operate-workflow-sa
                entrypoint: whalesay
                arguments:
                  parameters:
                    - name: message
                      # the value will get overridden by event payload from test-dep
                      value: THIS_WILL_BE_REPLACED
                templates:
                  - name: whalesay
                    inputs:
                      parameters:
                        - name: message
                    container:
                      command:
                        - cowsay
                      image: docker/whalesay:latest
                      args: ["{{inputs.parameters.message}}"]
          # The container args from the workflow are overridden by the s3 notification key
          parameters:
            - src:
                dependencyName: test-dep
                dataKey: notification.0.s3.object.key
              dest: spec.arguments.parameters.0.value
      retryStrategy:
        steps: 3
```
</details>



