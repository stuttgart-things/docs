# VM LIFECYCLE

## CROSSPLANE + TEKTON

<details><summary>DEPLOYMENT OPENEBS, CROSSPLANE + TEKTON</summary>

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


<details><summary>CONFIGURATION CROSSPLANE</summary>



</details>