# ARGO-CD

## DEPLOYMENT

<details><summary><b>HELM</b></summary>

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm upgrade --install argo-cd argo/argo-cd -n argocd --create-namespace --version 5.46.7
```

</details>

## CONFIGURATION

<details><summary><b>ADD GIT-REPOSITORY</b></summary>

```yaml
---
apiVersion: v1
data:
  password: ""
  project: ZGVmYXVsdA==
  type: Z2l0
  url: aHR0cHM6Ly9naXRodWIuYm9zY2hkZXZjbG91ZC5jb20vSEVQNEJVRS90b29sa2l0LmdpdAo=
  username: ""
kind: Secret
metadata:
  annotations:
    managed-by: argocd.argoproj.io
  labels:
    argocd.argoproj.io/secret-type: repository
  name: repo-tekton
  namespace: argocd
type: Opaque
```

</details>

## CLI

<details><summary><b>LOGIN</b></summary>

```bash
argocd login argo-cd.mgmt.sthings-vsphere.labul.sva.de:443 --insecure
```

</details>

<details><summary><b>ADD CLUSTER</b></summary>

```bash
# download kubeconfig of target cluster local and export KUBECONFIG
argocd cluster add $(kubectl config current-context) --name sthings-app --grpc-web
```

</details>

<details><summary><b>TERMINATE APP</b></summary>

```bash
argocd app terminate-op yacht-application-server
```

</details>

<details><summary><b>ADD OCI REPOSITORY</b></summary>

```bash
argocd repo add <REGISTRY-URL> --type helm --name aks2 --enable-oci --username <USERNAME> --password <PASSWORD>
```

</details>

## APPLICATION

<details><summary><b>FOLDER</b></summary>

```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: demo-cluster-configuration
  namespace: argocd
spec:
  destination:
    name: ''
    namespace: tekton-pipelines
    server: 'https://kubernetes.default.svc'
  source:
    path: clusters/aks
    repoURL: 'https://github.<ent>.com/HEP4BUE/tekton.git'
    targetRevision: HEAD
    directory:
      recurse: true
  sources: []
  project: default
  syncPolicy:
    automated:
      prune: false
      selfHeal: false
```

</details>

<details><summary><b>HELM</b></summary>

```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: vault-deployment
  namespace: argocd
spec:
  destination:
    name: ''
    namespace: vault
    server: 'https://kubernetes.default.svc'
  source:
    path: ''
    repoURL: 'https://helm.releases.hashicorp.com'
    targetRevision: 0.25.0
    chart: vault
    helm:
      values: |
        injector:
          enabled: false
        server:
          enabled: true
        csi:
          enabled: true
  sources: []
  project: default
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
    automated:
      prune: false
      selfHeal: true
```

</details close>

<details open><summary><b>MULTISOURCES HELM + GIT VALUES</b></summary>

```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: tekton-cd-pipelineruns
  namespace: argocd
spec:
  project: app
  sources:
    - repoURL: eu.gcr.io/stuttgart-things
      chart: tekton-resources
      targetRevision: v0.47.31
      helm:
        valueFiles:
        - $values/images/pipelineRuns.yaml
        - $values/charts/pipelineRuns.yaml
    - repoURL: https://github.com/stuttgart-things/stuttgart-things.git
      targetRevision: HEAD
      ref: values
  destination:
    name: dev11
    namespace: tektoncd
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
    automated:
      prune: true
      selfHeal: true
```

</details close>

## APPSET

<details open><summary><b>LIST GENERATOR, BULD ENV VAR + VAULT PLUGIN VALUES</b></summary>

```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: tekton-builds
  namespace: argocd
spec:
  generators:
  - list:
      elements:
        - app: sweatshop-creator
          repoURL: https://github.com/stuttgart-things/sweatShop-creator.git
          targetRevision: main
          appShort: sws-c
          destination: dev11
          kind: tekton
          namespace: tekton-cd
          path: helm/sweatshop-creator
        - app: sweatshop-informer
          repoURL: https://github.com/stuttgart-things/sweatShop-informer.git
          targetRevision: main
          appShort: sws-i
          destination: dev11
          kind: tekton
          namespace: tekton-cd
          path: helm/sweatshop-informer
        - app: machineshop-operator
          repoURL: https://github.com/stuttgart-things/machine-shop-operator.git
          targetRevision: ANSIBLE-CR
          appShort: ms-o
          destination: dev11
          kind: tekton
          namespace: tekton-cd
          path: helm/machine-shop-operator
  template:
    metadata:
      name: '{{ app }}-{{ kind }}-{{ destination }}'
    spec:
      project: app
      source:
        repoURL: '{{ repoURL }}'
        path: '{{ path }}'
        targetRevision: '{{ targetRevision }}'
        helm:
          values: |
            tektonResources:
              enabled: true
          parameters:
            - name: tekton-resources.runs.buildHelmChart.name
              value: '{{ appShort }}-helm-${ARGOCD_APP_REVISION}'
      destination:
        name: '{{ destination }}'
        namespace: '{{ namespace }}'
      syncPolicy:
        syncOptions:
        - CreateNamespace=true
        automated:
          prune: true
          selfHeal: false
```

</details close>

<details open><summary><b>GIT REPO+PATH</b></summary>

```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: machineshop-operator-dev-crs
  namespace: argocd
spec:
  generators:
  - list:
      elements:
      - app: sweatshop-creator
        destination: dev11
        kind: crs
        namespace: machine-shop-operator-system
        targetRevision: ANSIBLE-CR
        path: config/samples
        repoURL: https://github.com/stuttgart-things/machine-shop-operator.git
  template:
    metadata:
      name: '{{ app }}-{{ kind }}-{{ destination }}'
    spec:
      project: app
      source:
        repoURL: '{{ repoURL }}'
        targetRevision:  '{{ targetRevision }}'
        path: '{{ path }}'
      destination:
        name: '{{ destination }}'
        namespace: '{{ namespace }}'
      syncPolicy:
        syncOptions:
        - CreateNamespace=true
        automated:
          prune: true
          selfHeal: false
```
</details close>

<details open><summary><b>PULL REQUEST + LIST GENERATOR MATRIX</b></summary>

```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: tetkon-pr-scaffolder
  namespace: argocd
spec:
  generators:
    - matrix:
        generators:
          - pullRequest:
              github:
                api: https://github.<ent>.com/api/v3/
                owner: HEP4BUE
                repo: scaffolder # application source code repo
                tokenRef:
                  secretName: github-ent
                  key: token
                # labels:
                #   - build # label on PR
              requeueAfterSeconds: 30
          - list:
              elements:
                - repositoryUrl: https://github.<ENTERPRISE>.com/<USERNAME>/scaffolder.git
                  registry: akswkstekton.azurecr.io/scaffolder
  template:
    metadata:
      name: 'tekton-{{ number }}'
    spec:
      project: default
      destination:
        server: 'https://kubernetes.default.svc'
        namespace: tektoncd
      syncPolicy:
        automated:
          prune: true
      source:
        repoURL: https://github.<ENTERPRISE>.com/<USERNAME>/tekton.git
        targetRevision: main
        path: pipelineRuns
        helm:
          values: |
            runs:
              lint-golang:
                name: lint-go-scaffolder-{{ number }}
                addRandomDateToRunName: true #{{head_sha}}
                namespace: tektoncd
                kind: Pipeline
                ref: lint-golang-module
                params:
                  gitRepoUrl: {{ repositoryUrl }}
                  gitRevision: {{ branch }}
                  gitWorkspaceSubdirectory: scaffolder-{{ head_sha }}
                  golintImage: "docker.io/golangci/golangci-lint:v1.54-alpine"
                workspaces:
                  source:
                    workspaceKind: volumeClaimTemplate
                    storageClassName: longhorn
                    accessModes: ReadWriteMany
                    storage: 1Gi
                  secrets:
                    workspaceKind: csi
                    secretProviderDriver: secrets-store.csi.k8s.io
                    secretProviderClass: vault-git-creds
                  basic-auth:
                    workspaceKind: csi
                    secretProviderDriver: secrets-store.csi.k8s.io
                    secretProviderClass: vault-git-creds
              build-kaniko:
                name: build-kaniko-image-scaffolder-{{ number }}
                addRandomDateToRunName: true
                namespace: tektoncd
                kind: Pipeline
                ref: build-kaniko-image
                params:
                  gitRepoUrl: {{ repositoryUrl }}
                  gitRevision: {{ branch }}
                  gitWorkspaceSubdirectory: /kaniko/scaffolder-{{ head_sha }}
                  dockerfile: Dockerfile
                  context: /kaniko/scaffolder-{{ head_sha }}
                  image: {{ registry }}
                  tag: {{ number }}.{{ head_sha }}
                workspaces:
                  shared-workspace:
                    workspaceKind: volumeClaimTemplate
                    storageClassName: longhorn
                    accessModes: ReadWriteMany
                    storage: 2Gi
                  dockerconfig:
                    workspaceKind: csi
                    secretProviderDriver: secrets-store.csi.k8s.io
                    secretProviderClass: vault-kaniko-creds
                  basic-auth:
                    workspaceKind: csi
                    secretProviderDriver: secrets-store.csi.k8s.io
                    secretProviderClass: vault-git-creds
```
