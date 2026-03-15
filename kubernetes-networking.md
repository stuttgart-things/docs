# stuttgart-things/docs/kubernetes-networking

## CERTIFICATES

<details><summary>CERT MANAGER + DEFAULT CERT INGRESS-NGINX</summary>

GENERATE ROOT CERTIFICATE

```bash
# CREATE A FOLDER TO STORE CERTIFICATE FILES
mkdir -p .ssl
# GENERATE AN RSA KEY
openssl genrsa -out .ssl/root-ca-key.pem 2048
# GENERATE ROOT CERTIFICATE
openssl req -x509 -new -nodes -key .ssl/root-ca-key.pem \
  -days 3650 -sha256 -out .ssl/root-ca.pem -subj "/CN=kube-ca"
```

DEPLOY CERT-MANAGER

```bash
helm upgrade --install --wait --timeout 15m \
  --namespace cert-manager --create-namespace \
  --repo https://charts.jetstack.io cert-manager cert-manager \
  --values - <<EOF
installCRDs: true
EOF
```

CREATE ROOT CERTIFICATE SECRET

```bash
kubectl create secret tls -n cert-manager root-ca \
  --cert=.ssl/root-ca.pem \
  --key=.ssl/root-ca-key.pem
```

CREATE CLUSTER ISSUER

```bash
kubectl apply -n cert-manager -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: ca-issuer
spec:
  ca:
    secretName: root-ca
EOF
```

CREATE INGRESS CERT

```bash
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: default-ssl-certificate-tls
  namespace: ingress-nginx
spec:
  dnsNames:
  - hello.server.com
  issuerRef:
    group: cert-manager.io
    kind: ClusterIssuer
    name: ca-issuer
  secretName: default-ssl-certificate-tls
  usages:
  - digital signature
  - key encipherment
EOF
```

UPDATE INGRESS NGINX DEPLOYMENT ARGS

```
spec:
  containers:
  - args:
    - --default-ssl-certificate=ingress-nginx/default-ssl-certificate-tls
```

+ add root-ca.pem to your system trust store

</details>

<details><summary>INGRESS TLS CERTS UNDER WINDOWS</summary>

READ SECRET AND SAVE IN .crt FILE

```bash
kubectl -n cert-manager get secret ca-issuer -o jsonpath="{.data['tls\.crt']}" | base64 -d > ca.crt
```

USE SCP ON LOCAL WINDOWS MACHINE

```bash
# execute this from local windows machine to copy from remote ubuntu VM
scp user@hostname:/path/to/ca.crt /local/path/to/ca.crt
```

IMPORT .crt INTO WINDOWS TRUST STORE

```
-> double-click the certificate
-> click on <install certificate>
-> choose local machine
-> Select <Place all certificates in the following store>
-> Choose <Trusted Root Certification Authorities>
-> Finish and Confirm

(you need to restart the browser session)
```

</details>

<details><summary>k3s-setup(WIP)</summary>

```
cd /home/sthings/project/andre

Delete Cluster:
ansible-playbook sthings.rke.k3s -e k3s_k8s_version=1.34.1 -i ~/project/andre/inventory -e cilium_lbrange_start_ip=192.168.50.100 -e cilium_lbrange_stop_ip=192.168.50.200 -e k3s_state=absent -vv

create Cluster:
ansible-playbook sthings.rke.k3s -e k3s_k8s_version=1.34.1 -i ~/project/andre/inventory -e cilium_lbrange_start_ip=192.168.50.100 -e cilium_lbrange_stop_ip=192.168.50.200 -vv

fetch kubeconfig:
on target machine:
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chmod 0644 ~/.kube/config

scp kubeconfig to source machine:
scp sthings@192.168.50.11:~/.kube/config ~/.kube/panda-config

export KUBECONFIG=~/.kube/panda-config

deploy issuer selfsigned:
kubectl apply -f /home/sthings/project/andre/issuer.yaml

deploy headlamp:
ansible-playbook sthings.container.deploy_to_k8s -i ~/project/andre/inventory -e path_to_kubeconfig=~/.kube/panda-config -vv -e state=present -e ansible_user=sthings -e path=/home/sthings/.ansible/collections/ansible_collections/sthings/container/playbooks/vars -e profile=headlamp -e target_host=192.168.50.11 -e create_cert_resource=true

change clusterip to loadbalancer:
kubectl patch svc headlamp -n kube-system -p '{"spec": {"type": "ClusterIP"}}'
kubectl patch svc ingress-nginx-controller -n ingress-nginx -p '{"spec": {"type": "LoadBalancer"}}'


install Cert ubuntu:
kubectl get secret root-ca -n cert-manager -o jsonpath="{.data['tls\.crt']}" | base64 -d > headlamp-ca.crt
sudo cp headlamp-ca.crt /usr/local/share/ca-certificates/headlamp-ca.crt
sudo update-ca-certificates

install cert browser:
For Firefox:

    Go to Settings > Privacy & Security > Certificates > View Certificates

    Under Authorities, click Import

    Select headlamp-ca.crt

    Check Trust this CA to identify websites

For Chrome/Chromium:

    Open chrome://settings/security

    Scroll to Manage certificates

    Under Authorities, click Import

    Select headlamp-ca.crt

    Enable Trust this certificate for identifying websites

Change ingress-nginx-controller service loadbalancing ip to static:
kubectl patch svc ingress-nginx-controller -n ingress-nginx --type='merge' -p '{"spec": {"loadBalancerIP": "192.168.50.50"}}'


Helm changes of ingress-nginx (HostNetwork cant be true in this setup):
Check values:
helm get values ingress-nginx -n ingress-nginx
reinstall if hostNetwork=true:
helm uninstall ingress-nginx -n ingress-nginx
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install -n ingress-nginx ingress-nginx/ingress-nginx --version 4.14.0
helm install ingress-nginx ingress-nginx/ingress-nginx --version 4.14.0 -n ingress-nginx



```

</details>


## CURL/TEST SERVICE INSIDE CLUSTER

```bash
kubectl run curler --image=radial/busyboxplus:curl -i --tty --rm
ping/curl/nslookup <SERVICE_NAME>.<NAMESPACE>.svc.cluster.local
curl elastic-cluster-master.elastic.svc.cluster.local:9200
```

## NAMESPACE STUCK IN DELETION

### OPTION1: DELETE PENDING APISERVICES

```bash
kubectl get apiservice|grep False
kubectl delete APIServices v1alpha1.apps.kio.kasten.io # example
```

### OPTIONW: CHANGE FINALIZER

```bash
kubectl get namespace "<NAMESPACE>" -o json \
  | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" \
  | kubectl replace --raw /api/v1/namespaces/<NAMESPACE>/finalize -f -
```

## DEPLOY INGRESS-NGINX W/ DEFAULT WILDCARD CERT

### CREATE TLS SECRET

```bash
# CMD
kubectl create secret tls tls-wildcard --cert=lab.crt --key=lab.key -n ingress-nginx

# OR AS FILE
---
cat <<EOF > tls-wildcard.yaml
apiVersion: v1
data:
  tls.crt: {{ ssl_cert_crt | b64encode }}
  tls.key: {{ ssl_cert_key | b64encode }}
kind: Secret
metadata:
  name: tls-wildcard
  namespace: ingress-nginx
type: kubernetes.io/tls
EOF

kubectl apply -f tls-wildcard.yaml
```

### DEPLOY

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install my-ingress-nginx ingress-nginx/ingress-nginx --version 4.7.0 \
--set controller.extraArgs.default-ssl-certificate="ingress-nginx/tls-wildcard"
```

## TEST INGRESS-NGINX DEPLOYMENTS

<details><summary><b>wildcard</b></summary>

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: kuard
spec:
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
  selector:
    app: kuard
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kuard
spec:
  selector:
    matchLabels:
      app: kuard
  replicas: 1
  template:
    metadata:
      labels:
        app: kuard
    spec:
      containers:
      - image: gcr.io/kuar-demo/kuard-amd64:1
        imagePullPolicy: Always
        name: kuard
        ports:
        - containerPort: 8080
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: guard-ingress
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - guard.<DOMAIN>
  rules:
  - host: guard.<DOMAIN>
    http:
      paths:
      - path: /
        pathType: ImplementationSpecific
        backend:
          service
            name: kuard
            port:
              number: 80
```

</details>

<details><summary><b>path-based</b></summary>

```yaml
---
kind: Pod
apiVersion: v1
metadata:
  name: apple-app
  labels:
    app: apple
spec:
  containers:
    - name: apple-app
      image: hashicorp/http-echo
      args:
        - "-text=apple"
---
kind: Pod
apiVersion: v1
metadata:
  name: banana-app
  labels:
    app: banana
spec:
  containers:
    - name: banana-app
      image: hashicorp/http-echo
      args:
        - "-text=banana"
---
kind: Service
apiVersion: v1
metadata:
  name: banana-service
spec:
  selector:
    app: banana
  ports:
    - port: 5678 # Default port for image
---
kind: Service
apiVersion: v1
metadata:
  name: apple-service
spec:
  selector:
    app: apple
  ports:
    - port: 5678 # Default port for image
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fruit-ingress
spec:
  ingressClassName: nginx
  rules:
    - http:
        paths:
          - path: /apple
            pathType: Prefix
            backend:
              service:
                name: apple-service
                port:
                  number: 5678
          - path: /banana
            pathType: Prefix
            backend:
              service:
                name: banana-service
                port:
                  number: 5678
```

</details>


## LB-IPAM

```bash
cat <<EOF | kubectl apply -f -
apiVersion: "cilium.io/v2alpha1"
kind: CiliumLoadBalancerIPPool
metadata:
  name: "first-pool"
spec:
  blocks:
    - start: "10.31.102.18"
      stop: "10.31.102.19"
EOF
```

```bash
cat <<EOF > ~/cilium-config.yaml
k8sServiceHost: "10.31.102.162" # <IP>
k8sServicePort: "6443" # <PORT>
kubeProxyReplacement: true
l2announcements:
  enabled: true

externalIPs:
  enabled: true

operator:
  replicas: 1  # Uncomment this if you only have one node
  rollOutPods: true
  rollOutCiliumPods: true

k8sClientRateLimit:
  qps: 50
  burst: 200

ingressController:
  enabled: true
  default: true
  loadbalancerMode: shared
  service:
    annotations:
      io.cilium/lb-ipam-ips: 10.31.102.18
EOF

cilium upgrade -f ~/cilium-config.yaml
cilium connectivity test
```

```bash
cat <<EOF | kubectl apply -f -
apiVersion: cilium.io/v2alpha1
kind: CiliumL2AnnouncementPolicy
metadata:
  name: default-l2-announcement-policy
  namespace: kube-system
spec:
  externalIPs: true
  loadBalancerIPs: true
EOF
```

<details><summary><b>UNISTALLATION</b></summary>

```bash
/usr/local/bin/k3s-uninstall.sh
```

</details>



```bash



