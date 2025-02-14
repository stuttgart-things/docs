# DEV-MACHINE

* the following story assums that you are running against a (probably newly created) vm/machine w/ ansible
* you want to use this machine for development of iac automation / kubernetes based microservice code

## ANSIBLE-REQUIREMENTS

<details><summary><b>COLLECTIONS</b></summary>

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
    version: 4.3.0
  - name: community.vmware
    version: 5.2.0
  - name: awx.awx
    version: 24.6.1
  - name: community.hashi_vault
    version: 6.2.0
  - name: ansible.netcommon
    version: 7.1.0
  - name: https://github.com/stuttgart-things/ansible/releases/download/sthings-container-25.4.716.tar.gz/sthings-container-25.4.716.tar.gz
  - name: https://github.com/stuttgart-things/ansible/releases/download/sthings-baseos-25.4.1257/sthings-baseos-25.4.1257.tar.gz
EOF

ansible-galaxy collection install -r requirements.yaml -f
```

</details>


<details><summary><b>INVENTORY</b></summary>


</details>

## ALL-IN-ONE

<details><summary><b>ANSIBLE-CLI</b></summary>


</details>



<details><summary><b>CROSSPLANE - ANSIBLERUN</b></summary>

Usecase:
  - kubernetes based ansible execution

Requirements:
  - kubernetes cluster
  - crossplane
  - kubernetes provider
  - tekon-pipelines

```bash
kubectl apply -f - <<EOF
---
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: AnsibleRun
metadata:
  name: dev-machine-setup
  namespace: crossplane-system
spec:
  pipelineRunName: dev-machine-setup5
  createInventory: "false"
  varsFile: bmFtZToga29sbGUK # pragma: allowlist secret
  inventoryFile: MTAuMzEuMTAzLjQxCg== # pragma: allowlist secret
  playbooks:
    - "sthings.baseos.prepare_env"
    - "sthings.baseos.golang"
    - "sthings.baseos.binaries"
    - "sthings.container.docker"
    - "sthings.container.tools"
  ansibleVarsFile:
    - golang_version+-1.23.6
    - manage_filesystem+-true
    - update_packages+-true
    - install_requirements+-true
    - install_motd+-true
    - username+-sthings
    - lvm_home_sizing+-'15%'
    - lvm_root_sizing+-'35%'
    - lvm_var_sizing+-'50%'
    - send_to_msteams+-true
    - reboot_all+-false
  gitRepoUrl: https://github.com/stuttgart-things/ansible.git
  gitRevision: main
  providerRef:
    name: in-cluster
  vaultSecretName: vault # pragma: allowlist secret
  pipelineNamespace: tekton-pipelines
  workingImage: ghcr.io/stuttgart-things/sthings-ansible:11.0.0
  roles:
    - "https://github.com/stuttgart-things/install-requirements.git,2024.05.11"
    - "https://github.com/stuttgart-things/install-configure-docker,2024.12.30"
  collections:
    - community.crypto:2.22.3
    - community.general:10.1.0
    - ansible.posix:2.0.0
    - kubernetes.core:5.0.0
    - community.docker:4.1.0
    - community.vmware:5.2.0
    - awx.awx:24.6.1
    - community.hashi_vault:6.2.0
    - ansible.netcommon:7.1.0
    - https://github.com/stuttgart-things/ansible/releases/download/sthings-baseos-25.3.1202.tar.gz/sthings-baseos-25.3.1202.tar.gz
    - https://github.com/stuttgart-things/ansible/releases/download/sthings-container-25.6.1311.tar.gz/sthings-container-25.6.1311.tar.gz
EOF
```

</details>

## BASE

<details><summary><b>BINARIES</b></summary>


</details>

<details><summary><b>ANSIBLE</b></summary>


</details>

## CODING

<details><summary><b>GOLANG</b></summary>


</details>

## CONTAINER

### K3S DEV-CLUSTER

<img src="https://github.com/user-attachments/assets/71d5fd21-f41f-434b-83ce-feb63fd3127e" width="500">

* deploys a single node k3s-cluster for local testing
* ingress-controller address for browser/curl = fqdn
* LoadBalancing config over cilium (cluster setup / cli) configurable
* Certs over cert-manager deployment/integration

<details><summary><b>K3S DEV-CLUSTER DEPLOYMENT</b></summary>

### INVENTORY

```bash
cat <<EOF > k3s.yaml
# Change fqdn/ip to your machine's ip, no special inventory format needed
#10.31.104.110
EOF
```

### CLUSTER-SETUP

```bash
ansible-playbook sthings.container.k3s.yaml -i k3s.yaml -vv
```

### DEPLOY INGRESS-NGINX

```bash
ansible-playbook sthings.container.deploy_to_k8s \
-e profile=ingress-nginx-k3s -i k3s.yaml \
-e state=present \
-e path_to_kubeconfig=/etc/rancher/k3s/k3s.yaml \ # remote path
-e target_host=all \
-vv 
```

### TEST INGRESS-NGINX DEPLOYMENT

```bash
curl https://<fqdn>

# open browser
https://<fqdn>
```

### DEPLOY CERT-MANAGER

```bash
ansible-playbook sthings.container.deploy_to_k8s \
-e profile=cert-manager -i k3s.yaml \
-e state=present \
-e path_to_kubeconfig=/etc/rancher/k3s/k3s.yaml \ # remote path
-e target_host=all \
-vv 
```

### CERT-MANAGER EXAMPLE ISSUER

```bash
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned
spec:
  ca:
    secretName: root-ca
EOF
```

### CERT-MANAGER EXAMPLE CERT

```bash
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-tls
  namespace: default
spec:
  secretName: example-tls-secret
  issuerRef:
    name: selfsigned
    kind: ClusterIssuer
  commonName: <fqdn>
  dnsNames:
    - <fqdn>
  duration: 2160h # 90 days
  renewBefore: 360h # 15 days before expiration
  privateKey:
    algorithm: RSA
    size: 2048
EOF
```

</details>




## MANUAL CONFIGURATION & SNIPPETS

<details><summary><b>GIT-CONFIG</b></summary>


</details>

<details><summary><b>GH-CLI CONFIG</b></summary>


</details>

<details><summary><b>REGISTRY LOGINS</b></summary>


</details>
