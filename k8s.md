# stuttgart-things/docs/k8s

## TEST REGISTRY SECRETS W/ HELM 
```
kubectl run helm-pod -it --rm --image alpine/k8s:1.24.15 -- sh

mkdir -p ~/.docker/
cat <<EOF > ~/.docker/config.json 
{"auths": #...
EOF

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm pull bitnami/nginx --version 15.1.0
tar xvfz nginx-15.1.0.tgz 
yq e -i '.version = "9.9.9"' nginx/Chart.yaml
helm package nginx
helm push nginx-9.9.9.tgz oci://eu.gcr.io/stuttgart-things/
```

## DELETE ALL EVICTED PODS IN ALL NAMESPACES
```
kubectl get pods --all-namespaces | grep Evicted | awk '{print $2 " --namespace=" $1}' | xargs kubectl delete pod
```

## WORK W/ OFTEN MANUALY RESTARTED/DELETED PODS FOR DEV/TESTING
```
kubectl -n <NAMESPACE> get po | grep <PART-OF-POD-NAME> | awk '{ print $1}'
kubectl -n sweatshop delete po $(kubectl -n sweatshop get po | grep creator | awk '{ print $1}')
kubectl -n sweatshop logs -f $(kubectl -n sweatshop get po | grep creator | awk '{ print $1}')
```

## BUILDAH

BUILD OCI-IMAGE
```
buildah --storage-driver=overlay bud --format=oci \
--tls-verify=true --no-cache \
-f ~/projects/github/stuttgart-things/images/sthings-alpine/Dockerfile \
-t scr.app.4sthings.tiab.ssc.sva.de/sthings-alpine/alpine:123
```

## SKOPEO

### INSTALL
```
SKOPEO_VERSION=1.12.0
wget https://github.com/lework/skopeo-binary/releases/download/v${SKOPEO_VERSION}/skopeo-linux-amd64
sudo chmod +x skopeo-linux-amd64
sudo mv skopeo-linux-amd64 /usr/bin/skopeo && skopeo --version
```

### COPY IMAGE BETWEEN REGISTRIES (TAG)

* Copy images between registries

```
skopeo copy --insecure-policy docker://nginx:1.21
docker://whatever.cloud/gtc1fe/web:1.21
```

### COPY IMAGE BETWEEN REGISTRIES (DIGEST)

* Copy images between registries

```
skopeo copy --all --insecure-policy
docker://nginx@sha256:ff2a5d557ca22fa93669f5e70cfbeefda32b98f8fd3d33b38028c582d700f93a \ docker://whatever.cloud/gtc1fe/web@sha256:ff2a5d557ca22fa93669f5e70cfbeefda32b98f8fd3d33b38028c582d700f93a
```

## CLEANUP W/ NERDCTL
```
# clean images by id
sudo nerdctl rmi $(sudo nerdctl images | grep "2 months ago" | awk '{ print $3 }')

# clean images by name+tag
sudo nerdctl rmi $(sudo nerdctl images | grep "7 weeks ago" | awk '{ print $1":"$2 }')

# stop & delete all containers
sudo nerdctl stop $(sudo nerdctl container ls -a | grep "weeks ago" | awk '{ print $1 }') \
&& sudo nerdctl rm $(sudo nerdctl container ls -a | grep "weeks ago" | awk '{ print $1 }')
```

## CONTAINERD CTR
```
# pull image w/ crt
sudo ctr images pull docker.io/library/redis:alpine

# list images
ctr --namespace k8s.io images ls -q

# load/import conatiner image
ctr -n=k8s.io images import <IMAGE_NAME>
```

## INSTALL CONTAINERD

### INSTALL RUNC

```
wget https://github.com/containerd/containerd/releases/download/v1.7.1/containerd-1.7.1-linux-amd64.tar.gz
sudo tar Cxzvf /usr/local containerd-1.7.1-linux-amd64.tar.gz
wget https://raw.githubusercontent.com/containerd/containerd/main/containerd.service
sudo mv containerd.service /usr/lib/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable --now containerd
sudo systemctl status containerd

sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml

sudo systemctl restart containerd
sudo systemctl status containerd
sudo journalctl -u containerd
```

### INSTALL RUNC
```
wget https://github.com/opencontainers/runc/releases/download/v1.1.7/runc.amd64
sudo install -m 755 runc.amd64 /usr/local/sbin/runc
sudo ls /usr/local/sbin/ #check
```

### INSTALL CNI PLUGINS
```
wget https://github.com/containernetworking/plugins/releases/download/v1.3.0/cni-plugins-linux-amd64-v1.3.0.tgz
sudo mkdir -p /opt/cni/bin
sudo tar Cxzvf /opt/cni/bin cni-plugins-linux-amd64-v1.3.0.tgz
```


## RKE2
```
# list images
journalctl -u rke2-server | grep Import
```

### IMPORT RKE2 IMAGES INTO CONTAINERD NAMESPACE

```
wget https://github.com/rancher/rke2/releases/download/v1.25.7%2Brke2r1/rke2-images-all.linux-amd64.txt
```

```
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


## CURL/TEST SERVICE INSIDE CLUSTER
```
kubectl run curler --image=radial/busyboxplus:curl -i --tty --rm
ping/curl/nslookup <SERVICE_NAME>.<NAMESPACE>.svc.cluster.local
curl elastic-cluster-master.elastic.svc.cluster.local:9200
```

## NAMESPACE STUCK IN DELETION

#### OPTION1: DELETE PENDING APISERVICES
```
kubectl get apiservice|grep False
kubectl delete APIServices v1alpha1.apps.kio.kasten.io # example
```

#### OPTIONW: CHANGE FINALIZER
```
kubectl get namespace "<NAMESPACE>" -o json \
  | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" \
  | kubectl replace --raw /api/v1/namespaces/<NAMESPACE>/finalize -f -
```

## DEPLOY INGRESS-NGINX W/ DEFAULT WILDCARD CERT

### CREATE TLS SECRET 

```
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

```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install my-ingress-nginx ingress-nginx/ingress-nginx --version 4.7.0 \
--set controller.extraArgs.default-ssl-certificate="ingress-nginx/tls-wildcard"
```

## TEST INGRESS-NGINX DEPLOYMENTS

<details><summary><b>wildcard</b></summary>

```
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

```
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
