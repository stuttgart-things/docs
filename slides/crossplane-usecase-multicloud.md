### /CROSSPLANE USECASE MULTICLOUD
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/crossplane-composition.png" width="400"/>

🚀 BUNDLE MULTI CLOUD RESOURCES IN ONE COMPOSITION 🚀
--
### /RESOURCE1: GCP BUCKET
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/diagram-crossplane-gcp.png" width="600"/>
--
### /RESOURCE1: GCP BUCKET CLAIM
```
apiVersion: storage.gcp.upbound.io/v1beta1
kind: Bucket
metadata:
  name: example
  labels:
  annotations:
    crossplane.io/external-name: xsthings-demo
spec:
  forProvider:
    location: US
    storageClass: MULTI_REGIONAL
  providerConfigRef:
    name: default
  deletionPolicy: Delete
```
--
### /CREATE BUCKET + SHOW MANAGED RESOURCE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/bucket.gif" width="900"/>
--
### /MANAGE GCP BUCKET LIEFECYCLE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/01-crossplane-gcp-bucket.png" width="900"/>
---
### /RESOURCE2: TERRAFORM VSPHEREVM
<img src="https://www.ambient-it.net/wp-content/uploads/2023/08/terraform-VS-crossplane.png" width="800"/>

TERRAFORM PROVIDER
--
### /terraform provider
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/02-crossplane-terraform.png" width="1200"/>
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
--
### /REMOTE WORKSPACE (TERRAFORM CALL)
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/terraform-module-call.png" width="850"/>
--
### /VM-WORKSPACE DEFINITION
(PART I - EXAMPLE SHORTEND)

```
apiVersion: tf.upbound.io/v1beta1
kind: Workspace
metadata:
  name: tuesday-test1-knqpq-s92xd
spec:
  providerConfigRef:
    name: gcp-tuesday-test1
  deletionPolicy: Delete
  forProvider:
    entrypoint: ""
    module: "git::https://github.com/
    stuttgart-things/vsphere-vm.git?ref=v1.7.5-2.7.0"
    source: Remote
```
--
### /VM-WORKSPACE DEFINITION
(PART II - EXAMPLE SHORTEND)

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
--
### /CORRECT DRIFT
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/drift-meme.png" width="520"/>
--
### /MANAGE TERRAFORM LIEFECYCLE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/02-crossplane-terraform-vm.png"width="900">
--
### /XRD
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/vspherevmgcp.png" width="600">
--
### /COMPOSITION
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/vspheregcp-composition.png" width="1200">
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
--
### /KUBERNETES PROVIDER
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/kubernetes-provider.png"width="600">
--
### /OBJECT EXAMPLE

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
### /TEKTON PIPLINERUN



--
### /TEKTON PIPLINERUN OBJECT

--




### /KUBERNETES PROVIDER
<img src="https://pbs.twimg.com/media/EXfngQCWAAAlQQ6.jpg" width="650"/>



<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/platform-meme.png" width="900"/>
--
CROSSPLANE +
--
OBJECT

EXCALIDRAW: CROSSPLANE + KUBERNETES + TEKTON ON CLUSTER
---
