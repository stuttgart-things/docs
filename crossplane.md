# stuttgart-things/docs/crossplane

##  TERMINOLOGY

<details><summary><b>OVERVIEW</b></summary>

| KIND  | DESCRIPTION                                                          |
|----------|----------------------------------------------------------------------|
| Provider       | enable Crossplane to provision infrastructure on an external service |
| ProviderConfig | each Provider package has its own configuration type |
| Composition | Terraform fanboys might think of a Composition as a Terraform module - the HCL code that describes how to take input variables and use them to create resources in some cloud - Helm fanboys might think of a Composition as a Helm chart's templates; the moustache templated YAML files that describe how to take Helm chart values and render Kubernetes resources |
| CompositeResourceDefinition | There isn't a direct analog to XRDs in the Helm ecosystem, but they're a little bit like the variable blocks in a Terraform module that define which variables exist, whether those variables are strings or integers, whether they're required or optional, etc. |
| Composite Resource Claim  | Claims map to the same concepts as described above under the composite resource heading; i.e. tfvars files and Helm values.yaml files. Imagine that some tfvars files and some values.yaml files were only accessible to the platform team while others were offered to application teams; that's the difference between a composite resource and a claim. |

</details>

##  DEPLOYMENT

<details><summary><b>CLI INSTALLATION</b></summary>

```bash
curl -sL "https://raw.githubusercontent.com/crossplane/crossplane/master/install.sh" | sh
sudo mv crossplane /usr/local/bin
```

</details>

<details><summary><b>DEPLOYMENT W/ HELM</b></summary>

[provider-helm](https://github.com/crossplane-contrib/provider-helm/tree/master)

```bash
kubectl create namespace crossplane-system
helm repo add crossplane-stable https://charts.crossplane.io/stable && helm repo update

helm upgrade --install crossplane --wait \
--namespace crossplane-system \
crossplane-stable/crossplane --version 1.14.5

kubectl api-resources | grep upbound
```

</details>

## HELM PROVIDER

<details><summary><b>HELM PROVIDER INSTALLATION</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-helm
spec:
  package: "crossplanecontrib/provider-helm:master"
EOF
```

</details>

<details><summary><b>IN-CLUSTER PROVIDER CONFIGURATION</b></summary>

```bash
# DEPLOY HELM RELEASES ON THE SAME CLUSTER CROSSPLANE IS RUNNING ON
SA=$(kubectl -n crossplane-system get sa -o name | grep provider-helm | sed -e 's|serviceaccount\/|crossplane-system:|g')
kubectl create clusterrolebinding provider-helm-admin-binding --clusterrole cluster-admin --serviceaccount="${SA}"

kubectl apply -f - <<EOF
apiVersion: helm.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: helm-provider-incluster
spec:
  credentials:
    source: InjectedIdentity
EOF
```

</details>

<details><summary><b>DEPLOY HELM RELEASE</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: helm.crossplane.io/v1beta1
kind: Release
metadata:
  name: goldilocks-example
spec:
  forProvider:
    chart:
      name: goldilocks
      repository: https://charts.fairwinds.com/stable
      version: 8.0.0
#     url: "https://charts.bitnami.com/bitnami/wordpress-9.3.19.tgz"
    namespace: goldilocks
    insecureSkipTLSVerify: true
    skipCreateNamespace: false
    wait: true
    skipCRDs: true
    values:
      service:
        type: ClusterIP
  providerConfigRef:
    name: helm-provider-incluster
EOF
```

</details>

<details><summary><b>VERIFY RELEASE</b></summary>

```bash
kubectl get Release
```

</details>


## TERRAFORM PROVIDER

<details><summary><b>PROVIDER DEPLOYMENT</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-terraform
spec:
  package: xpkg.upbound.io/upbound/provider-terraform:v0.13.0
EOF
```

</details>

<details><summary><b>PROVIDER CONFIG (K8S STATE)</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: tf.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
spec:
  configuration: |
    terraform {
      backend "kubernetes" {
        secret_suffix     = "providerconfig-default"
        namespace         = "crossplane-system"
        in_cluster_config = true
      }
    }
EOF
```
</details>

<details><summary><b>INLINE WORKSPACE EXAMPLE</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: tf.upbound.io/v1beta1
kind: Workspace
metadata:
  name: example-inline
  annotations:
    crossplane.io/external-name: hello
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
EOF
```

</details>

<details><summary><b>CREATE TFVARS AS SECRET</b></summary>

```bash
# CREATE terraform.tfvars
cat <<EOF > terraform.tfvars
vsphere_user = "<USER>"
vsphere_password = "<PASSWORD>"
vm_ssh_user = "<SSH_USER>"
vm_ssh_password = "<SSH_PASSWORD>"
EOF
```

```bash
# CREATE SECRET
kubectl create secret generic vsphere-tfvars --from-file=terraform.tfvars
```

</details>

<details><summary><b>DEFINE INLINE WORKSPACE W/ MODULE CALL</b></summary>

```yaml
apiVersion: tf.upbound.io/v1beta1
kind: Workspace
metadata:
  name: vsphere-vm-labda-1
  annotations:
    crossplane.io/external-name: vsphere-vm-labda-1
spec:
  forProvider:
    source: Inline
    module: |
      module "labda-vm" {
        source = "github.com/stuttgart-things/vsphere-vm"
        vm_count               = 1
        vsphere_vm_name        = "michigan3"
        vm_memory              = 6144
        vm_disk_size           = "64"
        vm_num_cpus            = 6
        firmware               = "bios"
        vsphere_vm_folder_path = "stuttgart-things/testing"
        vsphere_datacenter     = "/NetApp-HCI-Datacenter"
        vsphere_datastore      = "/NetApp-HCI-Datacenter/datastore/DatastoreCluster/NetApp-HCI-Datastore-02"
        vsphere_resource_pool  = "Resources"
        vsphere_network        = "/NetApp-HCI-Datacenter/network/tiab-prod"
        vsphere_vm_template    = "/NetApp-HCI-Datacenter/vm/stuttgart-things/vm-templates/ubuntu23"
        vm_ssh_user            = var.vm_ssh_user
        vm_ssh_password        = var.vm_ssh_password
        bootstrap              = ["echo STUTTGART-THINGS"]
        annotation             = "VSPHERE-VM BUILD w/ TERRAFORM CROSSPLANE PROVIDER FOR STUTTGART-THINGS"
      }

      provider "vsphere" {
        user                 = var.vsphere_user
        password             = var.vsphere_password
        vsphere_server       = var.vsphere_server
        allow_unverified_ssl = true
      }

      variable "vsphere_server" {
        type        = string
        default     = false
        description = "vsphere server"
      }

      variable "vsphere_user" {
        type        = string
        default     = false
        description = "password of vsphere user"
      }

      variable "vsphere_password" {
        type        = string
        default     = false
        description = "password of vsphere user"
      }

      variable "vm_ssh_user" {
        type        = string
        default     = false
        description = "username of ssh user for vm"
      }

      variable "vm_ssh_password" {
        type        = string
        default     = false
        description = "password of ssh user for vm"
      }

    varFiles:
      - source: SecretKey
        secretKeyRef:
          namespace: default
          name: vsphere-tfvars
          key: terraform.tfvars
  writeConnectionSecretToRef:
    namespace: default
    name: terraform-workspace-vsphere-vm-labda-1
```

</details>

<details><summary><b>APPLY/STATUS/DESTORY</b></summary>

```bash
kubectl apply -f <WORKSPACE-DEFINITION>.yaml
kubectl describe workspace <WORKSPACE_NAME> | grep Status -A10
kubectl delete workspace <WORKSPACE_NAME>
```

</details>

<details><summary><b>COMPOSITE-RESOURCE-DEFINITION</b></summary>

```yaml
---
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xvmspherevms.resources.stuttgart-things.com
spec:
  group: resources.stuttgart-things.com
  names:
    kind: XVsphereVM
    plural: xvmspherevms
  claimNames:
    kind: VsphereVM
    plural: vmspherevms
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                vm:
                  type: object
                  properties:
                    count:
                      type: string
                      default: "1"
                    os:
                      type: string
                    name:
                      type: string
                    cpu:
                      type: string
                      default: "8"
                    ram:
                      type: string
                      default: "6144"
                    disk:
                      type: string
                      default: "64"
                    templatepath:
                      type: string
                    network:
                      type: string
                    folder:
                      type: string
                  required:
                    - count
                    - os
                    - name
                    - cpu
                    - ram
                    - disk
                    - templatepath
                    - network
                    - folder
                tfvars:
                  type: object
                  properties:
                    secretName:
                      type: string
                    secretNamespace:
                      type: string
                      default: default
                    secretKey:
                      type: string
                      default: terraform.tfvars
                  required:
                    - secretName
                connectionSecret:
                  type: object
                  properties:
                    name:
                      type: string
                    namespace:
                      type: string
                      default: default
                  required:
                    - name
              required:
                - vm
                - tfvars
                - connectionSecret
```

</details>

<details><summary><b>COMPOSITION</b></summary>

```yaml
---
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: vsphere-vm
  labels:
    crossplane.io/xrd: xvmspherevms.resources.stuttgart-things.com
spec:
  compositeTypeRef:
    apiVersion: resources.stuttgart-things.com/v1alpha1
    kind: XVsphereVM
  resources:
    - name: vsphere-vm
      base:
        kind: Workspace
        apiVersion: tf.upbound.io/v1beta1
        metadata:
          annotations:
            crossplane.io/external-name: vsphere-vm
        spec:
          writeConnectionSecretToRef:
            name: vsphere-vm-test
            namespace: crossplane-system
          forProvider:
            source: Inline
            vars:
              - key: vmcount
                type: integer
              - key: os
                type: string
              - key: name
                type: string
              - key: cpu
                type: integer
              - key: ram
                type: string
              - key: disk
                type: string
              - key: templatepath
                type: string
              - key: network
                type: string
              - key: folder
                type: string
            varFiles:
              - source: SecretKey
                secretKeyRef:
                  namespace: default
                  name: vsphere-tfvars
                  key: terraform.tfvars
            module: |
              module "vsphere-vm" {
                source = "github.com/stuttgart-things/vsphere-vm"
                vm_count               = var.vmcount
                vsphere_vm_name        = var.name
                vm_memory              = var.ram
                vm_num_cpus            = var.cpu
                vm_disk_size           = var.disk
                firmware               = var.firmware
                vsphere_vm_folder_path = var.folder
                vsphere_datacenter     = var.vsphere_datacenter
                vsphere_datastore      = var.vsphere_datastore
                vsphere_resource_pool  = var.vsphere_resource_pool
                vsphere_network        = var.network
                vsphere_vm_template    = "${var.templatepath}/${var.os}"
                vm_ssh_user            = var.ssh_user
                vm_ssh_password        = var.ssh_password
                bootstrap              = var.bootstrapcmd
                annotation             = var.annotation
              }

              variable "os" {
                description = "Name/version of vm template"
                type        = string
                default     = false
              }

              variable "templatepath" {
                description = "Path to vm-template"
                type        = string
                default     = false
              }

              variable "network" {
                description = "Bootstrap os"
                type        = string
                default     = false
              }

              variable "bootstrapcmd" {
                description = "Bootstrap os"
                type        = list(string)
                default     = ["whoami", "hostname"]
              }

              variable "annotation" {
                description = "Bootstrap os"
                type        = string
                default     = "VSPHERE-VM BUILD w/ TERRAFORM CROSSPLANE PROVIDER FOR STUTTGART-THINGS"
              }

              variable "folder" {
                default     = false
                type        = string
                description = "target (vm) folder path of vsphere virtual machine"
              }

              variable "firmware" {
                default     = "bios"
                type        = string
                description = "The firmware interface to use on the virtual machine. Can be one of bios or EFI. Default: bios"
              }

              provider "vsphere" {
                user                 = var.vsphere_user
                password             = var.vsphere_password
                vsphere_server       = var.vsphere_server
                allow_unverified_ssl = true
              }

              variable "name" {
                type        = string
                default     = false
                description = "vm name"
              }

              variable "vmcount" {
                default     = 1
                type        = number
                description = "amount of vms"
              }

              variable "vsphere_server" {
                type        = string
                default     = false
                description = "vsphere server"
              }

              variable "vsphere_datacenter" {
                default     = false
                type        = string
                description = "name of datacenter"
              }

              variable "vsphere_datastore" {
                default     = false
                type        = string
                description = "name of vsphere datastore"
              }

              variable "vsphere_resource_pool" {
                default     = false
                type        = string
                description = "name of resource_pool"
              }

              variable "vsphere_user" {
                type        = string
                default     = false
                description = "password of vsphere user"
              }

              variable "vsphere_password" {
                type        = string
                default     = false
                description = "password of vsphere user"
              }

              variable "ssh_user" {
                type        = string
                default     = false
                description = "username of ssh user for vm"
              }

              variable "ssh_password" {
                type        =  string
                default     = false
                description = "password of ssh user for vm"
              }

              variable "ram" {
                default     = 4096
                type        = number
                description = "amount of memory of the vm"
              }

              variable "disk" {
                default     = "32"
                type        = string
                description = "size of disk"
              }

              variable "cpu" {
                default     = 4
                type        = number
                description = "amount of cpus from the vm"
              }
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.tfvars.secretName
          toFieldPath: spec.forProvider.varFiles[0].secretKeyRef.name
        - type: FromCompositeFieldPath
          fromFieldPath: spec.tfvars.secretNamespace
          toFieldPath: spec.forProvider.varFiles[0].secretKeyRef.namespace
        - type: FromCompositeFieldPath
          fromFieldPath: spec.tfvars.secretKey
          toFieldPath: spec.forProvider.varFiles[0].secretKeyRef.key
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.count
          toFieldPath: spec.forProvider.vars[0].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.os
          toFieldPath: spec.forProvider.vars[1].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.name
          toFieldPath: spec.forProvider.vars[2].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.cpu
          toFieldPath: spec.forProvider.vars[3].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.ram
          toFieldPath: spec.forProvider.vars[4].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.disk
          toFieldPath: spec.forProvider.vars[5].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.templatepath
          toFieldPath: spec.forProvider.vars[6].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.network
          toFieldPath: spec.forProvider.vars[7].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.folder
          toFieldPath: spec.forProvider.vars[8].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.connectionSecret.name
          toFieldPath: spec.writeConnectionSecretToRef.name
        - type: FromCompositeFieldPath
          fromFieldPath: spec.connectionSecret.namespace
          toFieldPath: spec.writeConnectionSecretToRef.namespace
```

</details>

<details><summary><b>CLAIM</b></summary>

```yaml
---
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: VsphereVM
metadata:
  name: vsphere-vm-claim-11
spec:
  vm:
    count: "1"
    os: ubuntu23
    name: michigan15
    cpu: "4"
    ram: "4096"
    disk: "96"
    templatepath: "/NetApp-HCI-Datacenter/vm/stuttgart-things/vm-templates"
    network: "/NetApp-HCI-Datacenter/network/tiab-prod"
    folder: "stuttgart-things/testing"
  tfvars:
    secretName: vsphere-tfvars
    secretNamespace: default
    secretKey: terraform.tfvars
  connectionSecret:
    name: michigan15-vm
    namespace: default
  compositionRef:
    name: vsphere-vm
```

</details>


<details><summary><b>CREATE CLUSTER ROLE FOR TERRAFORM SERVICE ACCOUNT</b></summary>

```bash
TERRAFORM_SERVICE_ACCOUNT=$(kubectl -n crossplane-system get sa -ojson | jq -r '.items | map(.metadata.name | select(startswith("provider-terraform"))) | .[0]')

kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: crossplane:provider:provider-terraform
rules:
- apiGroups:
  - ""
  - "apps"
  - "extensions"
  - "networking.k8s.io"
  resources:
  - "namespaces"
  - "ingresses"
  - "services"
  - "deployments"
  verbs:
  - "*"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: crossplane:provider:provider-terraform
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: crossplane:provider:provider-terraform
subjects:
- kind: ServiceAccount
  name: ${TERRAFORM_SERVICE_ACCOUNT}
  namespace: crossplane-system
EOF
```

</details>

<details><summary><b>CREATE COMPOSITE-RESOURCE-DEFINITION</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xnginxapps.examples.stuttgart-things.com
spec:
  group: examples.stuttgart-things.com
  names:
    kind: XNginxApp
    plural: xnginxapps
  claimNames:
    kind: NginxApp
    plural: nginxapps
  versions:
  - name: v1alpha1
    served: true
    referenceable: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              env:
                type: string
EOF
```

</details>

<details><summary><b>CREATE SAMPLE COMPOSITION</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: nginx-app
  labels:
    crossplane.io/xrd: xnginxapps.examples.stuttgart-things.com
spec:
  compositeTypeRef:
    apiVersion: examples.stuttgart-things.com/v1alpha1
    kind: XNginxApp
  resources:
  - name: nginx-app
    base:
      kind: Workspace
      apiVersion: tf.upbound.io/v1beta1
      metadata:
        annotations:
          crossplane.io/external-name: default
      spec:
        providerConfigRef:
          name: terraform-default
        forProvider:
          source: Remote
          module: git::https://github.com/stuttgart-things/stuttgart-things.git//terraform/nginx-k8s-app?ref=main
          vars:
          - key: environment
    patches:
    - type: FromCompositeFieldPath
      fromFieldPath: spec.env
      toFieldPath: spec.forProvider.vars[0].value
EOF
```

</details>

<details><summary><b>CREATE SAMPLE CLAIM</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: examples.stuttgart-things.com/v1alpha1
kind: NginxApp
metadata:
  name: nginx-app-staging
spec:
  env: stag1
  compositionRef:
    name: nginx-app
EOF
```

</details>

<details><summary><b>VERIFY CLAIM</b></summary>

```bash
kubectl get NginxApp
```

</details>
