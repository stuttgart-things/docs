# VM LIFECYCLE

## CROSSPLANE + TEKTON

<details><summary>OPENEBS, CROSSPLANE + TEKTON DEPLOYMENT</summary>

```bash
cat <<EOF > crossplane-tekton.yaml
---
helmfiles:
  - path: git::https://github.com/stuttgart-things/helm.git@infra/openebs.yaml
    values:
      - namespace: openebs-system
      - profile: localpv
      - openebs_volumesnapshots_enabled: false
      - openebs_csi_node_init_containers_enabled: false
      - openebs_local_lvm_enabled: false
      - openebs_local_zfs_enabled: false
      - openebs_replicated_mayastor_enabled: false
  - path: git::https://github.com/stuttgart-things/helm.git@cicd/tekton.yaml
    values:
      - namespace: tekton-pipelines
  - path: git::https://github.com/stuttgart-things/helm.git@cicd/crossplane.yaml
    values:
      - namespace: crossplane-system
      - providers:
          - xpkg.upbound.io/crossplane-contrib/provider-helm:v0.20.4
          - xpkg.upbound.io/crossplane-contrib/provider-kubernetes:v0.17.1
      - terraform:
          configName: tf-provider
          image: ghcr.io/stuttgart-things/images/sthings-cptf:1.11.2
          package: xpkg.upbound.io/upbound/provider-terraform
          version: v0.20.0
          poll: 10m
          reconcileRate: 10
          s3SecretName: s3
      - secrets:
          s3:
            namespace: crossplane-system
            kvs:
              AWS_ACCESS_KEY_ID: "" # CHANGE
              AWS_SECRET_ACCESS_KEY: "" # CHANGE
EOF

helmfile template -f crossplane-tekton.yaml # RENDER ONLY
helmfile sync -f crossplane-tekton.yaml # APPLY HELMFILE # APPLY HELMFILE
```

</details>

<details><summary>CROSSPLANE CONFIGURATION</summary>

```bash
kubectl apply -f - <<EOF
---
apiVersion: v1
kind: Namespace
metadata:
  name: proxmox
---
apiVersion: v1
kind: Namespace
metadata:
  name: vsphere
---
apiVersion: pkg.crossplane.io/v1
kind: Configuration
metadata:
  name: vspherevm-ansible-run
spec:
  package: ghcr.io/stuttgart-things/crossplane/vsphere-vm-ansible:v0.1.0
---
apiVersion: pkg.crossplane.io/v1
kind: Configuration
metadata:
  name: proxmox-vm
spec:
  package: ghcr.io/stuttgart-things/crossplane/proxmox-vm:v0.3.0
---
apiVersion: pkg.crossplane.io/v1
kind: Configuration
metadata:
  name: ansible-run
spec:
  package: ghcr.io/stuttgart-things/crossplane/ansible-run:v0.3.0
---
apiVersion: pkg.crossplane.io/v1
kind: Configuration
metadata:
  name: proxmox-vm-ansible
spec:
  package: ghcr.io/stuttgart-things/crossplane/proxmox-vm-ansible:v0.1.0
---
apiVersion: pkg.crossplane.io/v1
kind: Configuration
metadata:
  name: vsphere-vm
spec:
  package: ghcr.io/stuttgart-things/crossplane/vsphere-vm:v0.1.0
---
apiVersion: tf.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: vsphere-vm
spec:
  configuration: |
    terraform {
      backend "kubernetes" {
        secret_suffix     = "vsphere-vm-tfstate" # pragma: allowlist secret
        namespace         = "crossplane-system"
        in_cluster_config = true
      }
    }
---
apiVersion: tf.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: proxmox-vm
spec:
  configuration: |
    terraform {
      backend "kubernetes" {
        secret_suffix     = "proxmox-vm-tfstate" # pragma: allowlist secret
        namespace         = "crossplane-system"
        in_cluster_config = true
      }
    }
---
apiVersion: tf.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
spec:
  configuration: |
    terraform {
      backend "kubernetes" {
        secret_suffix     = "default" # pragma: allowlist secret
        namespace         = "crossplane-system"
        in_cluster_config = true
      }
    }
  pluginCache: true
---
apiVersion: kubernetes.crossplane.io/v1alpha1
kind: ProviderConfig
metadata:
  name: in-cluster
spec:
  credentials:
    source: InjectedIdentity
---
apiVersion: helm.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: in-cluster
spec:
  credentials:
    source: InjectedIdentity
---
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-go-templating
spec:
  package: xpkg.upbound.io/crossplane-contrib/function-go-templating:v0.9.2
---
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-patch-and-transform
spec:
  package: xpkg.upbound.io/crossplane-contrib/function-patch-and-transform:v0.8.2
EOF
```

```bash
# KUBERNETES IN-CLUSTER
SA=$(kubectl -n crossplane-system get sa -o name | grep provider-kubernetes | sed -e 's|serviceaccount\/|crossplane-system:|g')
kubectl create clusterrolebinding provider-kubernetes-admin-binding --clusterrole cluster-admin --serviceaccount="${SA}"

# HELM IN-CLUSTER
SA=$(kubectl -n crossplane-system get sa -o name | grep provider-helm | sed -e 's|serviceaccount\/|crossplane-system:|g')
kubectl create clusterrolebinding provider-helm-admin-binding --clusterrole cluster-admin --serviceaccount="${SA}"
```

</details>

<details><summary>CROSSPLANE SECRETS</summary>

#### VSPHERE

```bash
kubectl apply -f - <<EOF
apiVersion: v1
data:
  terraform.tfvars: $(cat <<EOVARS | base64 -w0
vsphere_user = ""
vsphere_password = ""
vm_ssh_user = ""
vm_ssh_password = ""
vsphere_server = ""
EOVARS
)
kind: Secret
metadata:
  name: vsphere-tfvars
  namespace: crossplane-system
type: Opaque
EOF
```

#### PROXMOX

```bash
kubectl apply -f - <<EOF
apiVersion: v1
data:
  terraform.tfvars: $(cat <<EOVARS | base64 -w0
pve_api_url = ""
pve_api_user = ""
pve_api_password = ""
vm_ssh_user = ""
vm_ssh_password = ""
EOVARS
)
kind: Secret
metadata:
  name: proxmox-tfvars
  namespace: crossplane-system
type: Opaque
EOF
```

#### VAULT

```bash
kubectl apply -f - <<EOF
apiVersion: v1
data:
  VAULT_ADDR: ""
  VAULT_NAMESPACE: cm9vdA==
  VAULT_ROLE_ID: ""
  VAULT_SECRET_ID: ""
kind: Secret
metadata:
  name: vault
  namespace: tekton-pipelines
type: Opaque
EOF
```

</details>

<details><summary>OPTIONAL: ADD EXTERAL CLUSTER BY KUBECONFIG</summary>

```bash
# KUBECONFIG MUST EXIST ON DISK
kubectl -n crossplane-system \
create secret generic fluxdev3 \
--from-file=kubeconfig=/home/sthings/.kube/fluxdev3

kubectl apply -f - <<EOF
---
apiVersion: kubernetes.crossplane.io/v1alpha1
kind: ProviderConfig
metadata:
  name: fluxdev3
spec:
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: fluxdev3
      key: kubeconfig
EOF
```

</details>
