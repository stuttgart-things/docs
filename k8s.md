# K8S

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
