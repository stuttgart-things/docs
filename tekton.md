# stuttgart-things/docs/tekton

## TEKTON OPERATOR

<details><summary><b>EXAMPLE TEKTON-PIPELINE CR</b></summary>

```yaml
apiVersion: operator.tekton.dev/v1alpha1
kind: TektonPipeline
metadata:
  name: pipeline
spec:
  targetNamespace: tekton-pipelines
  await-sidecar-readiness: true
  coschedule: workspaces
  disable-affinity-assistant: false
  disable-creds-init: false
  disable-inline-spec: "pipeline,pipelinerun,taskrun"
  enable-api-fields: stable
  enable-bundles-resolver: true
  enable-cel-in-whenexpression: false
  enable-cluster-resolver: true
  enable-custom-tasks: false
  enable-git-resolver: true
  enable-hub-resolver: true
  require-git-ssh-secret-known-hosts: false
  running-in-environment-with-injected-sidecars: true
  trusted-resources-verification-no-match-policy: ignore
  performance:
    disable-ha: false
    buckets: 1
    replicas: 1
    threads-per-controller: 2
    kube-api-qps: 5.0
    kube-api-burst: 10
  options:
    disabled: false
    configMaps: {}
    deployments: {}
```

</details>

## TASKS

<details><summary><b>HELLO-TEKTON</b></summary>

```yaml
apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: hello-world
spec:
  params:
    - name: message
      type: string
      description: The message to print
  steps:
    - name: hello
      image: alpine
      script: |
        #!/bin/sh
        echo "$(params.message)"
---
apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: hello-bibi
spec:
  params:
    - name: message
      type: string
      description: The message to print
  steps:
    - name: hello
      image: nginx
      script: |
        #!/bin/sh
        echo "$(params.message)"
---
apiVersion: tekton.dev/v1
kind: Pipeline
metadata:
  name: hello-pipeline
spec:
  params:
    - name: message1
      type: string
    - name: message2
      type: string
  tasks:
    - name: run-hello-world
      taskRef:
        name: hello-world
      params:
        - name: message
          value: $(params.message1)
    - name: run-hello-bibi
      runAfter:
        - run-hello-world
      taskRef:
        name: hello-bibi
      params:
        - name: message
          value: $(params.message2)
---
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  name: hello-pipeline-run2
spec:
  pipelineRef:
    name: hello-pipeline
  params:
    - name: message1
      value: "Goodbye, Mr. Burns!"
    - name: message2
      value: "You, Rock!"
```

</details>

<details><summary><b>PACKAGE-HELM</b></summary>

```yaml
---
apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: package-helm
  labels:
    app.kubernetes.io/version: "0.2"
  annotations:
    tekton.dev/categories: "helm chart Build"
    tekton.dev/pipelines.minVersion: "0.48.0"
    tekton.dev/platforms: "linux/amd64"
    tekton.dev/tags: "helm-chart-build"
spec:
  description: create and publish helm chart to a registry
  workspaces:
    - name: dockerconfig
      description: includes a docker `config.json`
      optional: false
      mountPath: /home/nonroot/.config/helm/registry/
    - name: source
      description: holds helm chart source
      optional: false
  params:
    - name: CHARTNAME
      description: name of helm chart, e.g. "sthings-k8s-operator"
      type: string
      default: ""
    - name: CHARTTAG
      description: tag of helm chart, e.g. "0.1.0"
      type: string
      default: ""
    - name: IMAGE
      description: working image
      type: string
      default: "eu.gcr.io/stuttgart-things/sthings-k8s:1.127.2"
    - name: PATH
      description: directory to helm chart in repo, e.g. "helm"
      type: string
      default: ""
    - name: REGISTRY
      description: registry url, e.g. "scr.tiab.labda.sva.de"
      type: string
      default: ""
    - name: SUBDIRECTORY
      description: subdirectory of workspace
      type: string
      default: ""
  steps:
    - name: publish-helm-chart
      workingDir: $(workspaces.source.path)/$(params.SUBDIRECTORY)
      image: "$(params.IMAGE)"
      securityContext:
        privileged: false
        runAsNonRoot: true
        runAsUser: 65532
      script: |-
        #!/usr/bin/env sh
        set -eu
        helm dependency update $(params.PATH)/$(params.CHARTNAME)
        helm package --version $(params.CHARTTAG)-helm $(params.PATH)/$(params.CHARTNAME)
        helm push $(ls -Art | tail -n 1) oci://$(params.REGISTRY)
```

</details>

## PIPELINE

<details><summary><b>PACKAGE-HELM-CHART</b></summary>

```yaml
---
apiVersion: tekton.dev/v1
kind: Pipeline
metadata:
  name: package-helm-chart
spec:
  workspaces:
    - name: shared-workspace
    - name: sshCredentials
      optional: true
    - name: basic-auth
      optional: true
    - name: dockerconfig
  params:
    - name: gitRepoUrl
      type: string
      default: ""
      description: source git repo
    - name: gitRevision
      type: string
      default: ""
      description: revision of source git repo
    - name: gitWorkspaceSubdirectory
      type: string
      default: ""
      description: subdirectory on workspace
    - name: helmChartName
      type: string
      default: ""
      description: name of helm chart, e.g. "sthings-k8s-operator"
    - name: helmChartPath
      type: string
      default: ""
      description: directory to helm chart in repo, e.g. "helm"
    - name: helmChartTag
      type: string
      default: ""
      description: tag of helm chart, e.g. "0.1.0"
    - name: registry
      type: string
      default: ""
      description: registry url, e.g. "scr.tiab.labda.sva.de"
    - name: workingImage
      type: string
      default: ""
      description: working image
  tasks:
    - name: build-package-helmchart
      runAfter:
        - fetch-repository
      taskRef:
        name: package-helm
      workspaces:
        - name: dockerconfig
          workspace: dockerconfig
        - name: source
          workspace: shared-workspace
      params:
        - name: CHARTNAME
          value: $(params.helmChartName)
        - name: CHARTTAG
          value: $(params.helmChartTag)
        - name: IMAGE
          value: $(params.workingImage)
        - name: PATH
          value: $(params.helmChartPath)
        - name: REGISTRY
          value: $(params.registry)
        - name: SUBDIRECTORY
          value: $(params.gitWorkspaceSubdirectory)
    - name: fetch-repository
      taskRef:
        name: clone-git
      workspaces:
        - name: output
          workspace: shared-workspace
        - name: ssh-directory
          workspace: sshCredentials
        - name: basic-auth
          workspace: basic-auth
      params:
        - name: deleteExisting
          value: 'true'
        - name: revision
          value: $(params.gitRevision)
        - name: subdirectory
          value: $(params.gitWorkspaceSubdirectory)
        - name: url
          value: $(params.gitRepoUrl)
```

</details>

## PIPELINERUN EXAMPLES

<details><summary><b>LINT-GOLANG</b></summary>

```yaml
---
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  name: lint-scaffolder-cli-1
spec:
  pipelineRef:
    name: lint-golang-module
  workspaces:
    - name: source
      volumeClaimTemplate:
        spec:
          storageClassName: longhorn
          accessModes:
            - ReadWriteMany
          resources:
            requests:
              storage: 1Gi
    - name: secrets
      csi:
        driver: 'secrets-store.csi.k8s.io'
        readOnly: true
        volumeAttributes:
          secretProviderClass: vault-git-creds
    - name: basic-auth
      csi:
        driver: 'secrets-store.csi.k8s.io'
        readOnly: true
        volumeAttributes:
          secretProviderClass: vault-git-creds
  params:
    - name: gitRepoUrl
      value: https://github.<ENT>.com/<USERNAME>/scaffolder.git
    - name: gitRevision
      value: main
    - name: gitWorkspaceSubdirectory
      value: scaffolder
    - name: golintImage
      value: docker.io/golangci/golangci-lint:v1.54-alpine
```

</details>

## SECRET MANIFEST TEMPLATES

<details><summary><b>REGISTRY SECRET MANIFEST</b></summary>

```yaml
apiVersion: v1
data:
  config.json: <$(cat .docker/config.json | base64 -w 0)>
kind: Secret
metadata:
  name: acr
type: Opaque
```
</details>


<details><summary><b>VAULT SECRET ACR</b></summary>

```bash
config.json: {"auths": {"<REGISTRY>.azurecr.io": {"auth": "<USERNAME:PASSWORD|BASE64>"}}}
```

</details>


<details><summary><b>BASIC AUTH SECRET MANIFEST</b></summary>

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: basic
type: Opaque
stringData:
  .gitconfig: |
    [url "https://<USERNAME>:<TOKEN>@github.<ENT>.com"]
        insteadOf = https://github.<ENT>.com
    [user]
        name = Patrick Hermann
        email = patrick.hermann@sva.de
  .git-credentials: |
    https://<USERNAME>:<TOKEN>@github.<ENT>.com
```

</details>

<details><summary><b>GITHUB TOKEN SECRET MANIFEST</b></summary>

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: github-token
stringData:
  token: <TOKEN>
```

</details>

## SERVICE-ACCOUNT

<details><summary><b>REFERENCE SERVICE ACCOUNTS IN PIPELINERUN</b></summary>

```yaml
...
kind: PipelineRun
metadata:
  name: watch-tekton-pipelineruns-29
spec:
  taskRunSpecs:
    - pipelineTaskName: watch-tekton
      serviceAccountName: tektoncd
```

</details>

<details><summary><b>SERVICE ACCOUNT FOR TKN TASK</b></summary>

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tektoncd
  namespace: tektoncd
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: tektoncd
  name: tektoncd
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["create", "get", "watch", "list"]
- apiGroups: ["batch"]
  resources: ["jobs"]
  verbs: ["create", "get", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: tektoncd
  namespace: tektoncd
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: tektoncd
subjects:
- kind: ServiceAccount
  name: tektoncd
  namespace: tektoncd
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: list-all-namespaces-and-jobs-tektoncd
rules:
- apiGroups: [""]
  resources: ["namespaces"]
  verbs: ["get", "list"]
- apiGroups: ["batch"]
  resources: ["jobs"]
  verbs: ["create", "get", "patch", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: list-all-namespaces-and-jobs-tektoncd
subjects:
- kind: ServiceAccount
  name: tektoncd
  namespace: tektoncd
roleRef:
  kind: ClusterRole
  name: list-all-namespaces-and-jobs-tektoncd
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: tekton-pipelines-controller-cluster-access-tektoncd
subjects:
- kind: ServiceAccount
  name: tektoncd
  namespace: tektoncd
roleRef:
  kind: ClusterRole
  name: tekton-pipelines-controller-cluster-access
  apiGroup: rbac.authorization.k8s.io
```

</details>
