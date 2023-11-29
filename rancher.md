# stuttgart-things/docs/rancher

## REQURIEMENTS
<details><summary>INVENTORY FILE</summary>

```bash
cat << EOF > inventory
[initial_master_node]
hostname.<domain>
[additional_master_nodes]
# leave emptyfor singlenode cluster

[all:vars]
ansible_user=<USERNAME>
EOF
```
</details>

<details><summary>INSTALL REQUIREMENTS</summary>
  
```bash
cat << EOF > requirements.yaml
roles:
- src: https://github.com/stuttgart-things/deploy-configure-rke.git
  scm: git
- src: https://github.com/stuttgart-things/configure-rke-node.git
  scm: git
- src: https://github.com/stuttgart-things/install-requirements.git
  scm: git
- src: https://github.com/stuttgart-things/install-configure-docker.git
  scm: git
- src: https://github.com/stuttgart-things/create-os-user.git
  scm: git
- src: https://github.com/stuttgart-things/download-install-binary.git
  scm: git

collections: 
- name: community.crypto 
  version: 2.15.1 
- name: community.general 
  version: 7.3.0 
- name: ansible.posix 
  version: 1.5.2 
- name: kubernetes.core
  version: 2.4.0
EOF

ansible-galaxy install -r requirements.yaml -vv
```
</details>

## Deploy RKE2 w/ playbook

<details><summary>Deploy RKE2 w/ playbook</summary>

```bash
cat << EOF > deployRKE2.yaml
- hosts: all
  become: true

  pre_tasks:
    - name: Include vars
      ansible.builtin.include_vars: "{{ path_to_vars_file }}.yaml"
      when: path_to_vars_file is defined

  vars:
    rke_version: 2
    rke2_k8s_version: 1.26.9 # or less
    rke2_release_kind: rke2r1
    rke2_airgapped_installation: true
    disable_rke2_components:
      - rke2-ingress-nginx
      - rke-snapshot-controller
    cluster_setup: multinode #singlenode
    deploy_helm_charts: false

  roles:
    - role: deploy-configure-rke
EOF

ansible-playbook -i inventory deployRKE2.yaml
```

</details>

## Install MetalLB /w Helm

<details><summary> Install MetalLB /w Helm</summary>

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm upgrade --install metallb -n metallb-system --create-namespace bitnami/metallb
```

</details>

### create IPAddressPool

<details><summary>create IPAddressPool</summary>

```bash
kubectl apply -f - << EOF
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
    name: ip-pool
    namespace: metallb-system
spec:
    addresses:
    - <ip-range-begin>-<ip-range-end>
EOF
```

</details>

### create L2Advertisement

<details><summary>create L2Advertisement</summary>

```bash
kubectl apply -f - << EOF
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
    name: pool-advertisement
    namespace: metallb-system
spec:
    ipAddressPools:
    - ip-pool
EOF
```

</details>

## Install IngressNginx /w Helm

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm upgrade --install ingress-nginx -n ingress-nginx --create-namespace ingress-nginx/ingress-nginx
```

### create DNS entry for ip address
depending on the infrastructure, you need to create an A-record for the Ingress IP-Address

### create selfsigned-certs

## REQURIEMENTS

<details><summary>INSTALL REQUIREMENTS</summary>
  
```bash
cat << EOF > requirements.yaml
roles:
- src: https://github.com/stuttgart-things/install-requirements.git
  scm: git
- src: https://github.com/stuttgart-things/generate-selfsigned-certs.git
  scm: git
EOF

ansible-galaxy install -r requirements.yaml
```
</details>

## GENERATE selfsigned-certs

```bash
cat << EOF > selfsignedcerts.yaml
---
- hosts: localhost
  become: true

  vars:
    ssl_subject: rancher-things.${INGRESS_HOSTNAME}.${INGRESS_DOMAIN}
    ssl_ip: <ingress-ip>
    ca_subject: stuttgart-things
    certs_copy_target: "/tmp/certs/"
    trustbundle_name: cacerts.pem
    key_name: tls.key
    crt_name: tls.crt
    remote_src: true
    generate_certs: true
    install_public_certs: false

  roles:
    - generate-selfsigned-certs
EOF

ansible-playbooks -i inventory selfsignedcerts.yaml -vv
```

### Official documentation
https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/resources/update-rancher-certificate

### Add namespace
```bash
kubectl create namespace cattle-system
```

### Deploy certs in cluster
```bash
kubectl -n cattle-system create secret tls tls-rancher-ingress \
  --cert=/tmp/certs/tls.crt \
  --key=/tmp/certs/tls.key
```
```bash
kubectl -n cattle-system create secret generic tls-ca \
  --from-file=/tmp/certs/cacerts.pem
```

### Apply CRDs
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.crds.yaml
```

### Create values file for Rancher bootstrap installation

### Add Helm Repos for Rancher Installation

```bash
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
```

```bash
cat << EOF > values.yaml
global:
  cattle:
    psp:
      enabled: false
bootstrapPassword: ${BOOTSTRAP_PASSWORD}
hostname: ${INGRESS_HOSTNAME}.${INGRESS_DOMAIN}
privateCA: true
ingress:
  enabled: true
  ingressClassName: nginx
  servicePort: 80
EOF
```

## Install Rancher /w Helm
```bash
helm upgrade --install rancher rancher-stable/rancher --version v2.7.9 \
  --values values.yaml -n cattle-system
```

## Test Login /w bootstrap password from values.yaml
open Browser of choice and connect to rancher-things.${INGRESS_HOSTNAME}.${INGRESS_DOMAIN} use bootstrap password for login

## Rancher create new Downstream cluster
### Copy/Install CA-Certs on Downstream Cluster
copy tls.crt to /usr/local/share/ca-certificates on new Host

```bash
update-ca-certificates
```

### create new Downstream cluster /w Rancher
e.g. in Rancher Cluster Manager create a new cluster
copy Registration Command from web ui and execute on new Host


### ADD ADDITIONAL CLUSTER NODE
get token from MASTER
```
cat /var/lib/rancher/rke2/token
```

create directory on additional node
```
mkdir -p /etc/rancher/rke2
```

create config yaml for cluster
```
cat << EOF > /etc/rancher/rke2/config.yaml
---
write-kubeconfig-mode: 644
server: https://<master-ip-address>:9345
token: <token_from_master>
cni: canal
disable:
  - rke2-ingress-nginx
  - rke-snapshot-controller
EOF
```

set env vars
```
export INSTALL_RKE2_VERSION=v1.28.2+rke2r1
export INSTALL_RKE2_CHANNEL_URL=https://update.rke2.io/v1-release/channels
export INSTALL_RKE2_CHANNEL=stable
export INSTALL_RKE2_METHOD=tar

curl -sfL https://get.rke2.io | sh -
```

enable service
```
systemctl enable --now rke2-server.service
```

