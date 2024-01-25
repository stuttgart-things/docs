# stuttgart-things/docs/argocd

## IN-CLUSTER APP PROJECT

<details><summary><b>In-cluster app project</b></summary>

```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: in-cluster
  namespace: argocd
spec:
  clusterResourceBlacklist:
    - group: ""
      kind: ""
  clusterResourceWhitelist:
    - group: '*'
      kind: '*'
  description: in-cluster
  destinations:
    - name: in-cluster
      namespace: '*'
      server: https://kubernetes.default.svc
  namespaceResourceBlacklist:
    - group: ""
      kind: ""
  namespaceResourceWhitelist:
    - group: '*'
      kind: '*'
  sourceRepos:
    - '*'
```

 </details>

## ARGOCD-VAULT-PLUGIN

<details><summary><b>AVP SECRET-MANIFEST</b></summary>

```bash
export AVP_VAULT_ADDR=https://vault.cd43.sthings-pve.labul.sva.de
export AVP_TYPE=vault
export AVP_AUTH_TYPE=approle
export AVP_SECRET_ID=<SECRET-ID>
export AVP_ROLE_ID=<APPROLE-ID>

cat <<EOF > secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: example-secret
  namespace: default
stringData:
  password: <path:stagetime/data/redis#password>
type: Opaque
EOF

argocd-vault-plugin generate ./secret.yaml
```

</details>

<details><summary><b>AVP APPLICATION</b></summary>

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: test2
  namespace: argocd
spec:
  project: pve-dev51
  source:
    repoURL: 'https://github.com/stuttgart-things/stuttgart-things.git'
    path: machineShop/argo-cd/avp-manifest
    targetRevision: HEAD
  destination:
    server: 'https://10.31.103.122:6443'
    namespace: default
```

</details>

<details><summary><b>AVP HELM-CHART</b></summary>

```bash
export AVP_VAULT_ADDR=https://vault.cd43.sthings-pve.labul.sva.de
export AVP_TYPE=vault
export AVP_AUTH_TYPE=approle
export AVP_SECRET_ID=<SECRET-ID>
export AVP_ROLE_ID=<APPROLE-ID>

cat <<EOF > ./values.yaml
sentinel:
  enabled: true
master:
  service:
    type: ClusterIP
  persistence:
    enabled: false
    medium: ""
replica:
  replicaCount: 1
  persistence:
    enabled: false
    medium: ""
auth:
  password: <path:stagetime/data/redis#password>
EOF

argocd-vault-plugin generate ./values.yaml
```

</details>

<details><summary><b>AVP DOCKERFILE</b></summary>

```bash
ARG REGISTRY=eu.gcr.io
ARG REPOSITORY=stuttgart-things
ARG IMAGE=sthings-alpine
ARG TAG=3.12.0-alpine3.18

FROM ${REGISTRY}/${REPOSITORY}/${IMAGE}:${TAG}
# Switch to root for the ability to perform install

LABEL version=1.17.0
LABEL maintainer="Patrick Hermann patrick.hermann@sva.de"

ENV AWSCDK_VERSION=2.99.0
ENV GLIBC_VER=2.34-r0
ENV AVP_VERSION=1.17.0
ENV BIN=argocd-vault-plugin
# Install tools needed for your repo-server to retrieve & decrypt secrets, render manifests
# (e.g. curl, awscli, gpg, sops)

RUN apk update && apk upgrade -i -a --update-cache && apk --no-cache add \
        binutils \
        curl \
    && curl -sL https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub -o /etc/apk/keys/sgerrand.rsa.pub \
    && curl -sLO https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VER}/glibc-${GLIBC_VER}.apk \
    && curl -sLO https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VER}/glibc-bin-${GLIBC_VER}.apk \
    && apk add --force-overwrite --no-cache \
        glibc-${GLIBC_VER}.apk \
        glibc-bin-${GLIBC_VER}.apk \
    && curl -sL https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o awscliv2.zip \
    && unzip awscliv2.zip \
    && aws/install \
    && rm -rf \
        awscliv2.zip \
        aws \
        /usr/local/aws-cli/v2/*/dist/aws_completer \
        /usr/local/aws-cli/v2/*/dist/awscli/data/ac.index \
        /usr/local/aws-cli/v2/*/dist/awscli/examples \
    && apk --no-cache del \
        binutils \
        curl \
    && rm glibc-${GLIBC_VER}.apk \
    && rm glibc-bin-${GLIBC_VER}.apk \
    && rm -rf /var/cache/apk/*

# Install the AVP plugin (as root so we can copy to /usr/local/bin)
RUN wget https://github.com/argoproj-labs/argocd-vault-plugin/releases/download/v${AVP_VERSION}/argocd-vault-plugin_${AVP_VERSION}_linux_amd64
RUN chmod +x ${BIN}*
RUN mv ${BIN}* /usr/local/bin/${BIN}

# Switch back to non-root user
USER 65532
```

</details>

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

</details>

<details><summary><b>MULTISOURCES HELM + GIT VALUES</b></summary>

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

</details>

## APPSET

<details><summary><b>LIST GENERATOR, BULD ENV VAR + VAULT PLUGIN VALUES</b></summary>

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

</details>

<details><summary><b>GIT REPO+PATH</b></summary>

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

<details><summary><b>PULL REQUEST + LIST GENERATOR MATRIX</b></summary>

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
