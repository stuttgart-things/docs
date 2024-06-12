## CROSSPLANE: IAC ON STEROIDS
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/intro.jpeg" width="600"/>
<span style="color:orange">Fachbereichsmeeting Agile IT
& Software Dev 2024</span>
--
<!-- .slide: data-transition="zoom" -->
### /AGENDA
* INTRO <!-- .element: class="fragment fade-up" -->
* GCP + TERRAFORM PROVIDER <!-- .element: class="fragment fade-up" -->
* KUBERNETES PROVIDER <!-- .element: class="fragment fade-up" -->
* IAC COMPOSITIONS <!-- .element: class="fragment fade-up" -->
* HELM PROVIDER <!-- .element: class="fragment fade-up" -->
* KUBERNETES COMPOSITIONS <!-- .element: class="fragment fade-up" -->
--
### /INTRO

<span style="color:orange">#CICD #Automation #Cloud #IAC #Kubernetes #Containerization #PlatformEngineering </span> <br><br>

```
Patrick Hermann
System-Engineer (SVA SüdWest)
patrick.hermann@sva.de
```
---
# /CROSSPLANE - IAC ON STEROIDS

⚡️Provision and manage cloud infrastructure and services using kubectl⚡️
--
### /INTRO
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/00-crossplane-overview.png" width="1200"/>
* overview
--
### /CROSSPLANE
* use Kubernetes to control all of your cloud <!-- .element: class="fragment fade-up" -->
* created by Upbound (released in December 2018) <!-- .element: class="fragment fade-up" -->
* incubating CNCF project by the (2020) <!-- .element: class="fragment fade-up" -->
* managed enterprise/ui control plane (by) upbound <!-- .element: class="fragment fade-up" -->
--
### /CONCEPTS
* Kubernetes basics <!-- .element: class="fragment fade-up" -->
* Operators + cr(d)s <!-- .element: class="fragment fade-up" -->
* GitOps <!-- .element: class="fragment fade-up" -->
* Cloud <!-- .element: class="fragment fade-up" -->
* Platform engineering/IDP <!-- .element: class="fragment fade-up" -->
--
### /CONTROL (X)PLANE
* service that watches:
  * a declared state <!-- .element: class="fragment fade-up" -->
  * actual state reflects that of the declared <!-- .element: class="fragment fade-up" -->
    [<img src="https://www.padok.fr/hubfs/reconciliation_loop_crossplane.webp" width="900"/>](https://www.sva.de/index.html)
    ## <!-- .element: class="fragment fade-up" -->
---
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
* provision vspherevm + gcp bucket
---
### /RESOURCE3: KUBERNETES PROVIDER

Usecase Kubernetes 👾
--
### /KUBERNETES
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/kübernetz.jpeg" width="525"/>
--
### /K8s + HELM PROVIDER
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/k8s-helm-provider.png" width="2500"/>
* infra/app deployment (hub-spoke possible)
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
* example namespace object
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
* example helm release
--
### /INFRA EXAMPLE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/trident-composition.png" width="1200"/>
* Composition for trident
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
* trident claim
--
### /APP EXAMPLE
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/shared-cluster.png" width="600"/>
* developer consume apps/infra via claims
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
--
### /VSPHEREVM + ANSIBLERUN
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/vspherevm-ansiblerun.png" width="2500"/>
* VSPHEREVM-GCP-ANSIBLE
--
### /CLAIM
<img src="https://artifacts.app1.sthings-vsphere.labul.sva.de/images/rke2-miami.yaml.png" width="500"/>
* VSPHEREVM-GCP-ANSIBLE
--
<img src="https://pbs.twimg.com/media/EXfngQCWAAAlQQ6.jpg" width="700"/>
---
### /SUMMARY
* creating and managing shared tools, systems, and processes that other software teams use to build, deploy, and run their applications (Platform Engineering)
* Crossplanes can manage external APIs using K8s
* Read [blog post](https://wiki.sva.de/pages/viewpage.action?pageId=554802017)
--
### /NEXT STEPS
* RANCHER IPI/UPI CLUSTER + PROVISIONING (GITOPS, DNS, INFRA, APPLICATIONS)
* OPTIMIZE XRDS, COMPOSITIONS <!-- .element: class="fragment fade-up" -->
* TESTING COMPOSITION AND CLAIMS W/ KUTTL <!-- .element: class="fragment fade-up" -->
* BUILD (CROSSPLANE BASED) IDP W/ BACKSTAGE <!-- .element: class="fragment fade-up" -->
--
### /THANK YOU & GOODBYE GALAXY
<img src="https://media.licdn.com/dms/image/C4E22AQEd16vto8HKOA/feedshare-shrink_800/0/1671131117163?e=2147483647&v=beta&t=Ac815Z-pKEYJu6Hkve5HCGSi9timgGpEUS4rpSco624" width="500"/>
