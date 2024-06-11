# /CROSSPLANE
Usecase Kubernetes 👾
--
### /KUBERNETES
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/kübernetz.jpeg" width="525"/>
--
### /K8s + HELM PROVIDER
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/k8s-helm-provider.png" width="2500"/>
--
### /EXAMPLE OBJECT
```
apiVersion: kubernetes.crossplane.io/v1alpha2
kind: Object
metadata:
  name: sample-namespace
spec:
  forProvider:
    manifest:
      apiVersion: v1
      kind: Namespace
      metadata:
        labels:
          example: "true"
  providerConfigRef:
    name: dev-cluster
```
--
### /EXAMPLE RELEASE
```
apiVersion: helm.crossplane.io/v1beta1
kind: Release
metadata:
  name: goldilocks
spec:
  forProvider:
    chart:
      name: goldilocks
      repository: https://charts.fairwinds.com/stable
      version: 8.0.0
    namespace: goldilocks
    values:
      service:
        type: ClusterIP
```
--
### /INFRA EXAMPLE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/trident-composition.png" width="1200"/>
--
### /TRIDENT CLAIM
```
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: Trident
metadata:
  name: labda-demo
  namespace: crossplane-system
spec:
  clusterName: labda-demo
  backendConfig:
    dataLIF: 10.100.112.160
    backendName: ontap-nas-backend
    storageClassName: onptap
```
--
### /APP EXAMPLE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/shared-cluster.png" width="600"/>
--
### /HARBOR CLAIM
```
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: Harbor
metadata:
  name: harbor-demo
  namespace: crossplane-system
spec:
  hostname: test-reg
  projects:
    - app1
    - app2
```
