# stuttgart-things/docs/kubernetes-distributions

## RKE2

```bash
# list images
journalctl -u rke2-server | grep Import
```

### IMPORT RKE2 IMAGES INTO CONTAINERD NAMESPACE

```bash
wget https://github.com/rancher/rke2/releases/download/v1.25.7%2Brke2r1/rke2-images-all.linux-amd64.txt
```

```bash
#!/bin/bash

FILES="./rke2-images-all.linux-amd64.txt"

while read image; do

  image=$(echo $image | cut -d'/' -f 3)
  tag=$(echo $image| cut -d':' -f 2)
  imagename=$(echo $image| cut -d':' -f 1)

  echo pulling "$image"

  sudo ctr image pull $image

  echo exporting "$image"

  sudo ctr image export $(echo $image | cut -d'/' -f 2)-$imagename-$tag.tar $image

  echo importing "$image"

  sudo ctr -n=k8s.io image import $(echo $image | cut -d'/' -f 2)-$imagename-$tag.tar

done <${FILES}
```


## K3S

<details><summary><b>INSTALLATION</b></summary>

```bash
cat <<EOF > ~/k3s.yaml
flannel-backend: "none"
disable-kube-proxy: true
disable-network-policy: true
cluster-init: true
disable:
  - servicelb
  - traefik
EOF

curl -sfL https://get.k3s.io | sh -s - --config=$HOME/k3s.yaml
```

</details>

<details><summary><b>GET KUBECONFIG</b></summary>

```bash
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl  get nodes
```

</details>

<details><summary><b>INSTALL CILIUM CLI</b></summary>

```bash
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz
```

</details>

<details><summary><b>INSTALL CILIUM ON CLUSTER</b></summary>

```bash
API_SERVER_IP=10.31.102.162 # <IP>
API_SERVER_PORT=6443 # <PORT>
cilium install \
  --set k8sServiceHost=${API_SERVER_IP} \
  --set k8sServicePort=${API_SERVER_PORT} \
  --set kubeProxyReplacement=true \
  --helm-set=operator.replicas=1 # FOR SINGLE NODE CLUSTER

cilium status --wait
```

</details>

<details><summary><b>INSTALL INGRESS NGINX (HOSTNETWORK - NOT LB)</b></summary>

```bash
helm upgrade --install my-ingress-nginx ingress-nginx/ingress-nginx --version 4.11.2 --set controller.hostNetwork=true -n ingress-nginx --create-namespace
```

</details>


<details><summary><b>CERT-MANAGER SELF SIGNED</b></summary>

```bash
helm repo add cert-manager https://charts.jetstack.io
helm upgrade --install cert-manager cert-manager/cert-manager --version 1.16.0 --set installCRDs=true -n cert-manager --create-namespace
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
EOF

cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: test-ca
spec:
  isCA: true
  commonName: test-ca
  subject:
    organizations:
      - stuttgart-things
    organizationalUnits:
      - Widgets
  secretName: test-ca-secret
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: selfsigned-issuer
    kind: Issuer
    group: cert-manager.io
EOF

cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: test-ca-issuer
spec:
  ca:
    secretName: test-ca-secret
EOF

cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: test-server
spec:
  secretName: test-server-tls
  isCA: false
  usages:
    - server auth
    - client auth
  dnsNames:
  - "michigan.labul.sva.de"
  - "test-server"
  issuerRef:
    name: test-ca-issuer
EOF
```
</details>



