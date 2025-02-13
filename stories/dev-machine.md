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
  - name: https://github.com/stuttgart-things/ansible/releases/download/sthings-container-25.4.608.tar.gz/sthings-container-25.4.608.tar.gz
  - name: https://github.com/stuttgart-things/ansible/releases/download/sthings-baseos-25.4.1257/sthings-baseos-25.4.1257.tar.gz
EOF

ansible-galaxy collection install -r requirements.yaml -f
```

</details>


<details><summary><b>INVENTORY</b></summary>


</details>

## ALL-IN-ONE

<details><summary><b>INLCUDE PLAYBOOK</b></summary>


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

<<<<<<< HEAD
=======
![Image](https://github.com/user-attachments/assets/71d5fd21-f41f-434b-83ce-feb63fd3127e)

>>>>>>> b5f08597749ae18a9ae7d3f7d073cc76b6d33bee
<details><summary><b>K3S DEV-CLUSTER DEPLOYMENT</b></summary>

### INVENTORY

```bash
cat <<EOF > k3s.yaml
10.31.104.110
EOF
```

### CLUSTER-SETUP

```bash
ansible-playbook sthings.container.k3s.yaml -i k3s.yaml -vv
```

### DEPLOY INGRESS-NGINX

```bash
ansible-playbook sthings.container.deploy_to_k8s 
-e profile=ingress-nginx-k3s -i k3s.yaml \
-e state=present \
-e path_to_kubeconfig=/etc/rancher/k3s/k3s.yaml \
-e target_host=all \
-vv 
```

</details>

## MANUAL CONFIGURATION & SNIPPETS

<details><summary><b>GIT-CONFIG</b></summary>


</details>

<details><summary><b>GH-CLI CONFIG</b></summary>


</details>

<details><summary><b>REGISTRY LOGINS</b></summary>


</details>