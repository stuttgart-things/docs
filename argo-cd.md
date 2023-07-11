# stuttgart-things/docs/argo-cd

## LOGIN w/ CLI
```
argocd login argo-cd.mgmt.sthings-vsphere.labul.sva.de:443 --insecure
```
## ADD CLUSTER TO ARGO-CD w/ CLI
```
# download kubeconfig of target cluster local and export KUBECONFIG
argocd cluster add $(kubectl config current-context) --name sthings-app --grpc-web
```

## TERMINATE APPLICATION
```
argocd app terminate-op yacht-application-server
```

## APPSET 

<details open><summary>BULD ENV VAR + VAULT PLUGIN VALUES</summary>

```
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

<details open><summary>GIT REPO+PATH</summary>

```
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
        revision: ANSIBLE-CR
        path: config/samples
        repoURL: https://github.com/stuttgart-things/machine-shop-operator.git
  template:
    metadata:
      name: '{{ app }}-{{ kind }}-{{ destination }}'
    spec:
      project: app
      source:
        repoURL: '{{ repoURL }}'
        targetRevision: HEAD
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
