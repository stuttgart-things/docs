# Install Rancher Cluster

## Run Playbook Deploy RKE2
ansible-playbook -i <hostlist> deployRKE2.yaml

v1.26.9+rke2r1 or less

## Add Helm Repo for Bitnami
helm repo add bitnami https://charts.bitnami.com/bitnami

## Install MetalLB /w Helm
helm upgrade --install metallb -n metallb-system --create-namespace bitnami/metallb

## Create ipAddressPool for MetalLB
### create IPAddressPool

```
kubectl apply -f - << EOF
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
    name: ip-pool
    namespace: metallb-system
spec:
    addresses:
    - 10.31.10x.x-10.31.10x.x
EOF
```
### create L2Advertisement

```
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

## Add Helm Repo for IngressNginx
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

## Install IngressNginx /w Helm
helm upgrade --install ingress-nginx -n ingress-nginx --create-namespace ingress-nginx/ingress-nginx

## DNS created
create DNS entry for ip address

## CERT
deploy selfsigned certmanager

```
---
- hosts: localhost
  become: true

  vars:
    ssl_subject: rancher-things.${INGRESS_HOSTNAME}.${INGRESS_DOMAIN}
    ssl_ip: 10.31.10x.x
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
```

## Add namespace
kubectl create namespace cattle-system

## Official documentation
https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/resources/update-rancher-certificate

## Add Helm Repo for Rancher
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable

## Deploy certs in cluster
kubectl -n cattle-system create secret tls tls-rancher-ingress --cert=/tmp/certs/tls.crt --key=/tmp/certs/tls.key

kubectl -n cattle-system create secret generic tls-ca --from-file=/tmp/certs/cacerts.pem

## Apply CRDs
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.crds.yaml

## Create values.yaml
create values.yaml

```
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
```

## Install Rancher /w Helm
helm upgrade --install rancher rancher-stable/rancher --version v2.7.9 --values values.yaml -n cattle-system

## Update CA-Certs on Downstream Cluster
copy tls.crt to /usr/local/share/ca-certificates on cluster
update-ca-certificates

