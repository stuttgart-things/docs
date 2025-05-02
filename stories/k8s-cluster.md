# CLUSTER LIFECYCLE

## TESTING (LOCAL) CLUSTER

### OVERVIEW

Usecase:
  - create a local testing cluster

requirements:
  - ✅ 1-x machines/vms (base-setup for updates/partitioning already provisioned)

### CREATE KIND CLUSTER

<details><summary>KIND CLUSTER w/ INGRESS CONTROLLER</summary>

```bash
cat <<EOF > dev-cluster.yaml
---
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
networking:
  disableDefaultCNI: true
  kubeProxyMode: none
nodes:
  - role: control-plane
    image: kindest/node:v1.33.0
    kubeadmConfigPatches:
      - |
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
    extraPortMappings:
      - containerPort: 80
        hostPort: 80
        protocol: TCP
      - containerPort: 443
        hostPort: 443
        protocol: TCP
  - role: worker
    image: kindest/node:v1.33.0
    extraMounts:
      - hostPath: /mnt/data-node1  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
  - role: worker
    image: kindest/node:v1.33.0
    extraMounts:
      - hostPath: /mnt/data-node2  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
  - role: worker
    image: kindest/node:v1.33.0
    extraMounts:
      - hostPath: /mnt/data-node3  # Host directory to mount
        containerPath: /data       # Mount path inside the KinD node
EOF

sudo systemctl restart containerd
mkdir -p ~/.kube || true
kind create cluster --name dev --config dev-cluster.yaml --kubeconfig ~/.kube/kind-dev
```

</details>

<details><summary>DEPLOY CLUSTER-INFRA</summary>

Helmfile-based:
* Installs Cilium (CNI), Ingress-Nginx, and Cert-Manager
* Automated retry logic (helmfile apply/sync)

```bash
cat <<EOF > cluster-infra.yaml
---
helmDefaults:
  verify: false
  wait: true
  timeout: 600
  recreatePods: false
  force: true

helmfiles:
  - path: git::https://github.com/stuttgart-things/helm.git@infra/cilium.yaml
    values:
      - config: kind
      - configureLB: true
      - ipRangeStart: 172.18.250.0
      - ipRangeEnd: 172.18.250.50
      - clusterName: dev

  - path: git::https://github.com/stuttgart-things/helm.git@infra/ingress-nginx.yaml
    values:
      - enableHostPort: true

  - path: git::https://github.com/stuttgart-things/helm.git@infra/cert-manager.yaml
    values:
      - config: selfsigned
EOF

export KUBECONFIG=~/.kube/kind-dev
export HELMFILE_CACHE_HOME=/tmp/helm-cache/kind-dev

helmfile init --force

for cmd in apply sync; do
  for i in {1..8}; do
    helmfile -f cluster-infra.yaml $cmd && break
    [ $i -eq 8 ] && exit 1
    sleep 15
  done
done
```

</details>

### SHARED (LAB) CLUSTER

#### OVERVIEW

Usecase:
  - create a shared used rke2 cluster (lab based)
  - networking/dns/storage/certificate handling will be deployed after k8s-cluster was created

requirements:
  - ✅ 1-x machines/vms (base-setup for updates/partitioning already provisioned)

### INSTALL REQUIREMENTS 

<details><summary>ANSIBLE (CLI - FROM LOCAL)</summary>

```bash
cat <<EOF > requirements.yaml
---
collections:
  - name: community.crypto
    version: 2.25.0
  - name: community.general
    version: 10.3.1
  - name: ansible.posix
    version: 2.0.0
  - name: kubernetes.core
    version: 5.0.0
  - name: community.docker
    version: 4.4.0
  - name: community.vmware
    version: 5.4.0
  - name: awx.awx
    version: 24.6.1
  - name: community.hashi_vault
    version: 6.2.0
  - name: ansible.netcommon
    version: 7.1.0
  - name: https://github.com/stuttgart-things/ansible/releases/download/sthings-container-25.5.499/sthings-container-25.5.499.tar.gz
  - name: https://github.com/stuttgart-things/ansible/releases/download/sthings-baseos-25.1.682.tar.gz/sthings-baseos-25.1.682.tar.gz
  - name: https://github.com/stuttgart-things/ansible/releases/download/sthings-rke-25.5.532.tar.gz/sthings-rke-25.5.532.tar.gz
EOF

ansible-galaxy collection install -r requirements.yaml -f

pip3 install jmespath kubernetes
```

</details>

### EXECUTE BASE RKE2-SETUP 

<details><summary>ANSIBLE (CLI - FROM LOCAL)</summary>

### CREATE

```bash
# INSTALL COLLECTION
ansible-galaxy collection install https://github.com/stuttgart-things/ansible/releases/download/sthings-rke-25.1.475.tar.gz/sthings-rke-25.1.475.tar.gz -f 

# CREATE INVENTORY
cat <<EOF > rke2
[initial_master_node]
10.100.136.151
[additional_master_nodes]
10.100.136.152
10.100.136.153

[defaults]
host_key_checking = False
EOF

# CREATE CLUSTER
CLUSTER_NAME=dev-cluster
mkdir -p /home/sthings/.kube/

# CHECK FOR RKE2 RELEASES: https://github.com/rancher/rke2/releases

export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook sthings.rke.rke2 \
-i rke2 \
-e rke2_fetched_kubeconfig_path=/home/sthings/.kube/${CLUSTER_NAME} \
-e 1.32.1 \
-e rke2_release_kind=rke2r1 \
-vv

# TEST CLUSTER CONNECTION
export KUBECONFIG=/home/sthings/.kube/${CLUSTER_NAME}
kubectl get nodes

# ADD SOME USEFUL CLIS ON THE CLUSTER NODES
# IF YOU ARE PLANING FOR DOING SOME DEPLOYMENT/DEBUGGING ON THE NODES DIRECTLY (SSH)
ansible-playbook sthings.container.tools -i rke2 -vv
```

### DESTROY

```bash
# INSTALL COLLECTION
ansible-galaxy collection install https://github.com/stuttgart-things/ansible/releases/download/sthings-rke-25.1.475.tar.gz/sthings-rke-25.1.475.tar.gz -f 

# CREATE INVENTORY
cat <<EOF > rke2
[initial_master_node]
10.100.136.151
[additional_master_nodes]
10.100.136.152
10.100.136.153
EOF

ansible-playbook sthings.rke.rke2 \
-i rke2 \
-e rke_state=absent \
-e prepare_rancher_ha_nodes=false \
-vv
```

</details>

</details>

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

### INFRA DEPLOYMENT

<details><summary>GET AND ASSIGN IP (CLUSTERBOOK) VIA MACHINESHOP</summary>

requirements:
  - ✅ machineshop installed
  - ✅ know clusterbook address
  - ✅ cluster up & running - need ip net e.g. 10.31.103 (kubectl get node -> xx.xx.xxx(cut the rest))
  - ✅ clustername for assignment

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

<details><summary>APPLY MULTIPLE INFRA SERVICES AT ONCE w/ HELMFILE</summary>

requirements:
  - ✅ kubeconfig
  - ✅ helmfile

```bash
# IF YOU CONNECTED ON THE CLUSTER (SSH)
sudo chmod 777 /etc/rancher/rke2/rke2.yaml
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml

CLUSTER_NAME=dev-cluster
mkdir ${CLUSTER_NAME}
cat <<EOF > ${CLUSTER_NAME}/infra.yaml
---
helmfiles:
  - path: git::https://github.com/stuttgart-things/helm.git@metallb.yaml?ref=v1.0.0
    values:
      - ipRange: 10.31.103.4-10.31.103.4
  - path: git::https://github.com/stuttgart-things/helm.git@nfs-csi.yaml?ref=v1.0.0
    values:
      - nfsServerFQDN: 10.31.101.26
      - nfsSharePath: /data/col1/sthings
      - clusterName: k3d-my-cluster
      - nfsSharePath: /data/col1/sthings
  - path: git::https://github.com/stuttgart-things/helm.git@cert-manager.yaml?ref=v1.0.0
    values:
      - pkiServer: https://vault-vsphere.labul.sva.de:8200
      - pkiPath: pki/sign/sthings-vsphere.labul.sva.de
      - issuer: cluster-issuer-approle
      - approleSecret: ref+vault://apps/vault/secretID
      - approleID: ref+vault://apps/vault/roleID
      - pkiCA: ref+vault://apps/vault/vaultCA
  - path: git::https://github.com/stuttgart-things/helm.git@ingress-nginx.yaml?ref=v1.0.0
missingFileHandler: Error

helmDefaults:
  diffArgs:
    - "--suppress-secrets"
  skipSchemaValidation: true
  force: true
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

# INIT HELMFILE
helmfile init

# CHECK IF CHARTS CAN BE DOWNLOADED/RENDRED
helmfile template -f ${CLUSTER_NAME}/infra.yaml 

# DEPLOY RELEASES
helmfile sync -f ${CLUSTER_NAME}/infra.yaml
```

</details>

<details><summary>ADD LOADBALANCER IP (INGRESS-CONTROLLER) TO POWERDNS</summary>

requirements:
  - ✅ loadbalancing deployed (e.g metallb or cilium lb)
  - ✅ ingress-controller deployed + assigned loadbalancer ip

```bash
# INSTALL COLLECTION (IF NOT INSTALLED)
ansible-galaxy collection install https://github.com/stuttgart-things/ansible/releases/download/sthings-baseos-25.0.1178.tar.gz/sthings-baseos-25.0.1178.tar.gz -f

# INSTALL JMESPATH (IF NOT INSTALLED)
pip3 install jmespath

# SET VAULT ENV VARS
export VAULT_AUTH_METHOD=approle
export VAULT_ADDR=""
export VAULT_SECRET_ID=""
export VAULT_ROLE_ID=""
export VAULT_NAMESPACE=""

# CURL LOADBALANCER IP
curl 10.31.103.4 # EXAMPLE IP

#  ✅ IF NGINX IS REPLYING
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx</center>
</body>
</html>

# SET VARS
ENTRY_ZONE=sthings-vsphere.example.com. # PLEASE MIND THE . AT THE END!
IP=10.31.103.4 
HOSTNAME=homerun-int2
PDNS_URL=https://pdns-vsphere.example.com:8443
DOMAIN=sthings-vsphere.example.com

# RUN PLAY
ansible-playbook sthings.baseos.pdns \
-e pdns_url=${PDNS_URL} \
-e entry_zone=${ENTRY_ZONE} \
-e ip_address=${IP} \
-e hostname=${HOSTNAME} \
-vv

# TEST AGAINST WILDCARD URL (*.CLUSTER-DOMAIN)
curl test.${HOSTNAME}.${DOMAIN}

# ✅ IF NGINX (INGRESS CONTROLLER) IS REPLYING
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx</center>
</body>
</html>
```

</details>

<details><summary>TEST CREATE INGRESS-CERTIFICATE</summary>

requirements:
  - ✅ kubeconfig + kubectl
  - ✅ cert manager deployed
  - ✅ (cluster-)Issuer configured

```bash
# THIS IS JUST A EXAMPLE - YOU DON'T NEED TO DEPLOY KEYCLOAK :-)
kubectl create ns keycloak
# EXAMPLE CERT
kubectl apply -f - <<EOF
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: keycloak
  namespace: keycloak
spec:
  commonName: keycloak.fluxdev-3.sthings-vsphere.example.com
  dnsNames:
    - keycloak.fluxdev-3.sthings-vsphere.example.com
  issuerRef:
    kind: ClusterIssuer
    name: cluster-issuer-approle
  secretName: keycloak.fluxdev-3.sthings-vsphere.example.com-tls
EOF

# CHECK FOR READY=TRUE STATUS
kubectl get Certificate -n keycloak

# CHECK FOR EXISTENCE OF TLS_SECRET 
kubectl get secret -n keycloak | grep keycloak.fluxdev-3.sthings-vsphere.example.com-tls
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
