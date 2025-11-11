# /Helmfile
--
### /OVERVIEW
Helmfile is a declarative spec for deploying helm charts. It lets you... <!-- .element: class="fragment fade-up" -->
    * Keep a directory of chart value files and maintain changes in version control <!-- .element: class="fragment fade-up" -->
    * Apply CI/CD to configuration changes <!-- .element: class="fragment fade-up" -->
    * Periodically sync to avoid skew in environments <!-- .element: class="fragment fade-up" -->
--
### /OVERVIEW
*  Declarative: Write, version-control, apply the desired state file for visibility and reproducibility <!-- .element: class="fragment fade-up" -->
* Modules: Modularize common patterns of your infrastructure, distribute it via Git, S3, etc. to be reused across the entire company <!-- .element: class="fragment fade-up" -->
* Versatility: Manage your cluster consisting of charts, kustomizations, and directories of Kubernetes resources, turning everything to Helm releases <!-- .element: class="fragment fade-up" -->
--
### /EXAMPLE
```
repositories:
- name: prometheus-community
  url: https://prometheus-community.github.io/helm-charts

releases:
- name: prom-norbac-ubuntu
  namespace: prometheus
  chart: prometheus-community/prometheus
  set:
  - name: rbac.create
    value: false
```
--
### /ENVIRONMENTS
```
environments:
  labda-vsphere:
    values:
      - environments/vm.yaml
      - environments/defaults.yaml
      - environments/{{ .Environment.Name }}.yaml
```
--
### /DEFAULTS
```
helmDefaults:
  verify: false
  wait: false
  timeout: 600
  recreatePods: false
  force: true
```
