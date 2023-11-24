# Install Rancher Cluster

## Deploy RKE2 on Host e.g. /w ansible role

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
```

```bash
ansible-playbook -i <hostlist> deployRKE2.yaml
```

### Add Helm Repos for Rancher Installation
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
```

## Install MetalLB
### Install MetalLB /w Helm
```bash
helm upgrade --install metallb -n metallb-system --create-namespace bitnami/metallb
```

### create IPAddressPool

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
### create L2Advertisement

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

## Install IngressNginx
### Install IngressNginx /w Helm
```bash
helm upgrade --install ingress-nginx -n ingress-nginx --create-namespace ingress-nginx/ingress-nginx
```

## create DNS entry for ip address
depending on the infrastructure, you need to create an A-record for the Ingress IP-Address

## create Selfsingned Certificates for the Cluster
### create playbook to execute generate-selfsigned-certs role

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
```

### deploy selfsigned certmanager
```bash
ansible-playbooks -i <inventory> selfsignedcerts.yaml
```

## Add namespace
```bash
kubectl create namespace cattle-system
```

## Official documentation
https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/resources/update-rancher-certificate

## Install Rancher
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

## Create values file for Rancher bootstrap installation

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

## Rancher create new Downstream cluster
### Copy/Install CA-Certs on Downstream Cluster
copy tls.crt to /usr/local/share/ca-certificates on new Host

```bash
update-ca-certificates
```

### create new Downstream cluster /w Rancher
e.g. in Rancher Cluster Manager create a new cluster
copy Registration Command from web ui and execute on new Host
