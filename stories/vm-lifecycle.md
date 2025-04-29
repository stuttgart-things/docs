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
# NAMESPACE DEFINTION FOR PROXMOX
apiVersion: v1
kind: Namespace
metadata:
  name: proxmox
---
# NAMESPACE DEFINTION FOR VSPHERE
apiVersion: v1
kind: Namespace
metadata:
  name: vsphere
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
  name: kubernetes-incluster
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
SA=$(kubectl -n crossplane-system get sa -o name | grep provider-kubernetes | sed -e 's|serviceaccount\/|crossplane-system:|g')
kubectl create clusterrolebinding provider-kubernetes-admin-binding --clusterrole cluster-admin --serviceaccount="${SA}"
```

</details>