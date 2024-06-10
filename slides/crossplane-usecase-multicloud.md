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
### /MANAGE GCP BUCKET LIEFECYCLE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/01-crossplane-gcp-bucket.png" width="900"/>
--
* k9S + GOOLGE CLOUD SREENSHOT
---
### /RESOURCE2: TERRAFORM VSPHEREVM
CROSSPLANE + TERRAFORM PROVIDER
--
### /terraform provider
<img src="https://media.licdn.com/dms/image/C4E22AQG9YBkzVlWYJA/feedshare-shrink_2048_1536/0/1650457090015?e=2147483647&v=beta&t=aQO1JSO2Xer_ylMNFyfH1Qn6bIZJBLpjW5nvdKHu7tA" width="450"/>
--
### /terraform provider
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/02-crossplane-terraform.png" width="700"/>
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
### /VM-WORKSPACE DEFINITION I

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
### /VM-WORKSPACE DEFINITION II

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
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/drift-meme.png" width="450"/>
--
### /MANAGE TERRAFORM LIEFECYCLE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/02-crossplane-terraform-vm.png"width="900">
--
EXCALIDRAW: CROSSPLANE + GCP PROVIDER + VM IN VSPHERE
---
### /RESOURCE3: KUBERNETES PROVIDER
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/platform-meme.png" width="900"/>
--
CROSSPLANE +
--
OBJECT
--
### /RESOURCE3: KUBERNETES PROVIDER
<img src="https://pbs.twimg.com/media/EXfngQCWAAAlQQ6.jpg" width="650"/>
--
EXCALIDRAW: CROSSPLANE + KUBERNETES + TEKTON ON CLUSTER
---
