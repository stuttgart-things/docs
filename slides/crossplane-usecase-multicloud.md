### /CROSSPLANE USECASE MULTICLOUD
BUNDLE MULTI CLOUD RESOURCES IN ONE COMPOSITION
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
WORKSPACE DEFINITION I

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
WORKSPACE DEFINITION II

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
EXCALIDRAW: CROSSPLANE + GCP PROVIDER + VM IN VSPHERE
---
### /USECASE3: MANIFEST TEKTON
CROSSPLANE + KUBERNETES PROVIDER
--
OBJECT
--
EXCALIDRAW: CROSSPLANE + KUBERNETES + TEKTON ON CLUSTER
---
### /COMPOSITION
### /XRDS
### /CLAIM
