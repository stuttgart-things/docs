### /CROSSPLANE USECASE MULTICLOUD
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/crossplane-composition.png" width="400"/>

🚀 BUNDLE MULTI CLOUD RESOURCES IN ONE COMPOSITION 🚀
--
### /RESOURCE1: GCP BUCKET
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/diagram-crossplane-gcp.png" width="600"/>
* Deployment crossplane + gcp provider
--
### /RESOURCE1: GCP BUCKET CLAIM
```
apiVersion: storage.gcp.upbound.io/v1beta1
kind: Bucket
metadata:
  name: xsthings-demo
  labels:
  annotations:
    crossplane.io/external-name: xsthings-demo
spec:
  forProvider:
    location: GER
  providerConfigRef:
    name: default
  deletionPolicy: Delete
```
* create gcp bucket via claim
--
### /CREATE BUCKET
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/bucket.gif" width="900"/>
* creation of bucket + show managed resources

--
### /MANAGED (GCP BUCKET) RESOURCE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/01-crossplane-gcp-bucket.png" width="900"/>
* gcp resources managed on k8s
---
### /RESOURCE2: TERRAFORM VSPHEREVM
<img src="https://www.ambient-it.net/wp-content/uploads/2023/08/terraform-VS-crossplane.png" width="800"/>

TERRAFORM PROVIDER
--
### /terraform provider
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/02-crossplane-terraform.png" width="1200"/>
* crossplane + terraform provider
--
### /terraform provider
<img src="https://media.licdn.com/dms/image/C4E22AQG9YBkzVlWYJA/feedshare-shrink_2048_1536/0/1650457090015?e=2147483647&v=beta&t=aQO1JSO2Xer_ylMNFyfH1Qn6bIZJBLpjW5nvdKHu7tA" width="450"/>
--
### /INLINE WORKSPACE EXAMPLE

```
apiVersion: tf.upbound.io/v1beta1
kind: Workspace
metadata:
  name: example-inline
spec:
  forProvider:
    source: Inline
    module: |
      output "hello_world" {
        value = "Hello, World!"
      }
  writeConnectionSecretToRef:
    namespace: default
    name: terraform-workspace-example-inline
```
* inline hcl code definition
--
### /REMOTE WORKSPACE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/terraform-module-call.png" width="850"/>
* TERRAFORM MODULE CALL (GIT)

--
### /VM-WORKSPACE DEFINITION

```
apiVersion: tf.upbound.io/v1beta1
kind: Workspace
metadata:
  name: vsphere-vm
spec:
  providerConfigRef:
    name: gcp
  deletionPolicy: Delete
  forProvider:
    entrypoint: ""
    module: "git::https://github.com/
    stuttgart-things/vsphere-vm.git?ref=v1.7.5-2.7.0"
    source: Remote
```
* PART I - EXAMPLE SHORTEND
--
### /VM-WORKSPACE DEFINITION
```
varFiles:
- format: HCL
  secretKeyRef:
    key: terraform.tfvars
    name: vsphere-tfvars
    namespace: crossplane-system
  source: SecretKey
vars:
- key: vm_count
  value: "1"
- key: vm_memory
  value: "4096"
writeConnectionSecretToRef:
  name: tuesday-test1
```
* PART II - EXAMPLE SHORTEND
--
### /MANAGED RESOURCE ON CLUSTER
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/crossplane-vsphere.gif" width="1050"/>
* View synced resource
--
### /CORRECT DRIFT
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/drift-meme.png" width="520"/>
--
### /MANAGE TERRAFORM LIEFECYCLE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/02-crossplane-terraform-vm.png"width="900">
* CROSSPLANE SYNCS W/ CLOUD
--
### /XRDS, COMPOSITIONS & CLAIMS
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/xrd-compostion.png" width="1200">
* scope (+personas) of cluster/namespaced resources
--
### /XRD
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/crossplane-crds.png" width="1200">
* custom API specification
--
### /COMPOSITION
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/vspheregcp-composition.png" width="1200">
* composes individual managed resources together into a larger, reusable, solution.
--
### /CLAIM
(EXAMPLE SHORTEND)
```
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: VsphereVMGCP
metadata:
  name: demo-vm
spec:
  providerRef:
    name: gcp-tf
  bucket:
    name: demo-vm
  vm:
    ram: "4096"
    disk: "64"
  tfvars:
    secretName: vsphere-tfvars
```
---
### /RESOURCE3: KUBERNETES PROVIDER
<img src="https://anthonyspiteri.net/wp-content/uploads/2019/07/k8severywhere.jpg" width="700"/>

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
    storageClassName: ontap
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
