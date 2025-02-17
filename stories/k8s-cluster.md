# CLUSTER LIFECYCLE

## LAB CLUSTER

### OVERVIEW


### REQUIREMENTS

### EXECUTE BASE RKE2-SETUP 

<details><summary>CROSSPLANE - ANSIBLERUN</summary>

```yaml
Usecase:
  - kubernetes based ansible execution

Requirements:
  - kubernetes cluster
  - crossplane
  - kubernetes provider
  - tekon-pipelines
```

```bash
# SET INVENTORY AS B64
cat <<EOF | base64 -w 0
[initial_master_node]
192.168.0.1

[additional_master_nodes]
192.168.0.2
192.168.0.3
EOF

# SET VARS (ALL COMPLEX OR MULTILINE)
cat <<EOF | base64 -w 0
values_cilium: |
  ---
  kubeProxyReplacement: true
  k8sServiceHost: 127.0.0.1
  k8sServicePort: 6443
  cni:
    chainingMode: "none"
EOF
```

### CREATE
```bash
kubectl apply -f - <<EOF
---
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: AnsibleRun
metadata:
  name: rke2-cluster-setup-homerun-int2
  namespace: crossplane-system
spec:
  pipelineRunName: rke2-setup-homerun-int2-2
  createInventory: "false"
  inventoryFile: W2luaXRpYWxfbWFzdGVyX25vZGVdCmhvbWVydW4taW50Mi5sYWJ1bC5zdmEuZGUKClthZGRpdGlvbmFsX21hc3Rlcl9ub2Rlc10KaG9tZXJ1bi1pbnQyLTIubGFidWwuc3ZhLmRlCmhvbWVydW4taW50Mi0zLmxhYnVsLnN2YS5kZQ== # pragma: allowlist secret
  playbooks:
    - "sthings.baseos.prepare_env"
    - "sthings.rke.rke2_workflow"
  ansibleVarsFile:
    - rke_state+-present
    - rke_version+-2
    - rke2_k8s_version+-1.30.4
    - rke2_airgapped_installation+-true
    - rke2_release_kind+-rke2r1 # rke2r2
    - rke2_cni+-cilium
  varsFile: ZGlzYWJsZV9ya2UyX2NvbXBvbmVudHM6CiAgLSBya2UyLWluZ3Jlc3MtbmdpbngKICAtIHJrZS1zbmFwc2hvdC1jb250cm9sbGVyCmNsdXN0ZXJfc2V0dXA6IG11bHRpbm9kZSAjc2luZ2xlbm9kZQpya2UyX2NuaTogY2lsaXVtCnZhbHVlc19jaWxpdW06IHwKICAtLS0KICBrdWJlUHJveHlSZXBsYWNlbWVudDogdHJ1ZQogIGs4c1NlcnZpY2VIb3N0OiAxMjcuMC4wLjEKICBrOHNTZXJ2aWNlUG9ydDogNjQ0MwogIGNuaToKICAgIGNoYWluaW5nTW9kZTogIm5vbmUiCgpoZWxtQ2hhcnRDb25maWc6CiAgY2lsaXVtOgogICAgbmFtZTogcmtlMi1jaWxpdW0KICAgIG5hbWVzcGFjZToga3ViZS1zeXN0ZW0KICAgIHJlbGVhc2VfdmFsdWVzOiAie3sgdmFsdWVzX2NpbGl1bSB9fSI= # pragma: allowlist secret
  gitRepoUrl: https://github.com/stuttgart-things/ansible.git
  gitRevision: main
  providerRef:
    name: in-cluster
  vaultSecretName: vault # pragma: allowlist secret
  pipelineNamespace: tekton-pipelines
  workingImage: ghcr.io/stuttgart-things/sthings-ansible:11.0.0
  roles:
    - "https://github.com/stuttgart-things/install-requirements.git,2024.05.11"
  collections:
    - https://github.com/stuttgart-things/ansible/releases/download/sthings-baseos-25.3.1202.tar.gz/sthings-baseos-25.3.1202.tar.gz
    - https://github.com/stuttgart-things/ansible/releases/download/sthings-container-25.6.1311.tar.gz/sthings-container-25.6.1311.tar.gz
    - https://github.com/stuttgart-things/ansible/releases/download/sthings-rke-25.5.532.tar.gz/sthings-rke-25.5.532.tar.gz
    - community.crypto:2.22.3
    - community.general:10.1.0
    - ansible.posix:2.0.0
    - kubernetes.core:5.0.0
    - community.docker:4.1.0
    - community.vmware:5.2.0
    - awx.awx:24.6.1
    - community.hashi_vault:6.2.0
    - ansible.netcommon:7.1.0
EOF
```

### DESTROY
```bash
kubectl apply -f - <<EOF
---
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: AnsibleRun
metadata:
  name: rke2-cluster-setup-homerun-int2
  namespace: crossplane-system
spec:
  pipelineRunName: rke2-destroy
  createInventory: "false"
  inventoryFile: W2luaXRpYWxfbWFzdGVyX25vZGVdCmhvbWVydW4taW50Mi5sYWJ1bC5zdmEuZGUKClthZGRpdGlvbmFsX21hc3Rlcl9ub2Rlc10KaG9tZXJ1bi1pbnQyLTIubGFidWwuc3ZhLmRlCmhvbWVydW4taW50Mi0zLmxhYnVsLnN2YS5kZQ== # pragma: allowlist secret
  playbooks:
    - "sthings.baseos.prepare_env"
    - "sthings.rke.rke2_workflow"
  ansibleVarsFile:
    - rke_state+-absent #present
    - rke_version+-2
    - prepare_rancher_ha_nodes+-false
  gitRepoUrl: https://github.com/stuttgart-things/ansible.git
  gitRevision: main
  providerRef:
    name: in-cluster
  vaultSecretName: vault # pragma: allowlist secret
  pipelineNamespace: tekton-pipelines
  workingImage: ghcr.io/stuttgart-things/sthings-ansible:11.0.0
  roles:
    - "https://github.com/stuttgart-things/install-requirements.git,2024.05.11"
  collections:
    - https://github.com/stuttgart-things/ansible/releases/download/sthings-baseos-25.3.1202.tar.gz/sthings-baseos-25.3.1202.tar.gz
    - https://github.com/stuttgart-things/ansible/releases/download/sthings-container-25.6.1311.tar.gz/sthings-container-25.6.1311.tar.gz
    - https://github.com/stuttgart-things/ansible/releases/download/sthings-rke-25.5.532.tar.gz/sthings-rke-25.5.532.tar.gz
    - community.crypto:2.22.3
    - community.general:10.1.0
EOF
```

</details>

### INFRA DEPLOYMENT (HELMFILE)

<details><summary>GET AND ASSIGN IP (CLUSTERBOOK) VIA MACHINESHOP</summary>

```bash
machineshop get \
--system=ips \
--destination=clusterbook.fluxdev-3.sthings-vsphere.labul.sva.de:443 \
--path=10.31.103 \
--output=1

machineshop push \
--target=ips \
--destination=clusterbook.fluxdev-3.sthings-vsphere.labul.sva.de:443 \
--artifacts="10.31.103.4" \
--assignee=homerun-int2
```

</details>

<details><summary>APPLY w/ HELMFILE</summary>

```bash
CLUSTER_NAME=k3d-my-cluster
mkdir ${CLUSTER_NAME}
cat <<EOF > ${CLUSTER_NAME}/infra.yaml
---
helmfiles:
  - path: git::https://github.com/stuttgart-things/flux.git@helmfiles/metallb.yaml?ref=feature/add-nfs-chart
    values:
      - ipRange: 10.31.103.4-10.31.103.4
  - path: git::https://github.com/stuttgart-things/flux.git@helmfiles/nfs-csi.yaml?ref=feature/add-nfs-chart
    values:
      - nfsServerFQDN: 10.31.101.26
      - nfsSharePath: /data/col1/sthings
      - clusterName: k3d-my-cluster
      - nfsSharePath: /data/col1/sthings
  - path: git::https://github.com/stuttgart-things/flux.git@helmfiles/cert-manager.yaml?ref=feature/add-nfs-chart
    values:
      - pkiServer: https://vault-vsphere.labul.sva.de:8200
      - pkiPath: pki/sign/sthings-vsphere.labul.sva.de
      - issuer: cluster-issuer-approle
      - approleSecret: ref+vault://apps/vault/secretID
      - approleID: ref+vault://apps/vault/roleID
      - pkiCA: ref+vault://apps/vault/vaultCA
  - path: git::https://github.com/stuttgart-things/flux.git@helmfiles/ingress-nginx.yaml?ref=feature/add-nfs-chart
missingFileHandler: Error

helmDefaults:
  diffArgs:
    - "--suppress-secrets"
  skipSchemaValidation: true
  force: false
  verify: false
EOF

export VAULT_AUTH_METHOD=approle
export VAULT_ADDR=https://<VAULT-URL>:8200
export VAULT_SECRET_ID=623c991f-d.. #example value
export VAULT_ROLE_ID=1d42d7e7-8.. #example value
export VAULT_NAMESPACE=root

HELMFILE_CACHE_HOME=$(pwd)/${CLUSTER_NAME}/helm_cache
mkdir -p ${HELMFILE_CACHE_HOME} && 
export HELMFILE_CACHE_HOME=${HELMFILE_CACHE_HOME}

helmfile init ${CLUSTER_NAME}
helmfile deps -f ${CLUSTER_NAME}/infra.yaml
helmfile sync -f ${CLUSTER_NAME}/infra.yaml
```

</details>


### EXECUTE BASE K3S-SETUP 

#### OPTION1: ANSIBLE-CLI

#### OPTION2: TEKTON-PIPELINERUN


### CLUSTER BASE-CONFIGURATION

#### OPTION1 LOADBALANCING: METALLB

#### OPTION2 LOADBALANCING: CILIUM

#### INGRESS-CONTROLLER: INGRESS-NGINX


#### POWERDNS ENTRY
