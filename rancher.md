# stuttgart-things/docs/rancher

## CREATE VSPHERE CLUSTER W/ CLUSTER API

<details><summary>VSPHERE-CREDENTIALS</summary>

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: labda-vsphere
  namespace: cattle-global-data
  annotations:
    field.cattle.io/description: "labda-vsphere"
    field.cattle.io/name: "labda-vsphere"
    provisioning.cattle.io/driver: "vmwarevsphere"
  labels:
    cattle.io/creator: norman
type: Opaque
stringData:
  vmwarevspherecredentialConfig-password: "<passwort for vshere>"
  vmwarevspherecredentialConfig-username: "<user>"
  vmwarevspherecredentialConfig-vcenter: "<vshere ip>"
  vmwarevspherecredentialConfig-vcenterPort: "<vshere port>"

```

</details>

<details><summary>VMWAREVSPHERECONFIG</summary>

```yaml
apiVersion: rke-machine-config.cattle.io/v1
kind: VmwarevsphereConfig
metadata:
  name: <your-maschine-pool-name>-<cluster-name>
  namespace: fleet-default
common:
  cloudCredentialSecretName: cattle-global-data:labda-vsphere
cloneFrom: /NetApp-HCI-Datacenter/vm/stuttgart-things/vm-templates/u22-rke2-ipi
cfgparam:
  - disk.enableUUID=TRUE
datacenter: /NetApp-HCI-Datacenter
datastoreCluster: /NetApp-HCI-Datacenter/datastore/DatastoreCluster
hostsystem: null
folder: /NetApp-HCI-Datacenter/vm/stuttgart-things/rancher-things
network:
  - /NetApp-HCI-Datacenter/host/NetApp-HCI-Cluster-01/10.100.135.44/tiab-prod
cpuCount: "6"
diskSize: "20480"
memorySize: "6144"
creationType: template
sshPort: "22"
sshUser: docker
sshUserGroup: staff
tag: []
vappProperty: []
customAttribute: []
boot2dockerUrl: ""
contentLibrary: ""
vcenter: "10.100.135.50"
vcenterPort: "443"
vappTransport: null
vappIpallocationpolicy: null
vappIpprotocol: null
cloudinit: |
  runcmd:
    - wget -O /usr/local/share/ca-certificates/labda-vsphere-ca.crt https://vault-vsphere.tiab.labda.sva.de:8200/v1/pki/ca/pem --no-check-certificate
    - update-ca-certificates
     
```

</details>


<details><summary>CLUSTER</summary>

```yaml
apiVersion: provisioning.cattle.io/v1
kind: Cluster
metadata:
  name: <clustername>
  namespace: fleet-default
  finalizers:
    - wrangler.cattle.io/provisioning-cluster-remove
spec:
  kubernetesVersion: v1.25.9+rke2r1
  cloudCredentialSecretName: cattle-global-data:labda-vsphere
  localClusterAuthEndpoint: {}
  rkeConfig:
    chartValues:
      rke2-calico: {}
    etcd:
      snapshotRetention: 5
      snapshotScheduleCron: 0 */5 * * *
    machineGlobalConfig:
      cni: calico
      disable:
        - rke2-ingress-nginx
        - rke2-metrics-server
      disable-kube-proxy: false
      etcd-expose-metrics: false
      profile: null
    machineSelectorConfig:
      - config:
          protect-kernel-defaults: false
          cloud-provider-name: vsphere
    machinePools:
      - name: <your-master-machine-pool-name>-<cluster-name>
        quantity: 1
        displayName: <your-master-machine-pool-name>-<cluster-name>
        controlPlaneRole: true
        etcdRole: true
        workerRole: false
        machineConfigRef:
          kind: VmwarevsphereConfig
          name: <your-vmwarevsphereconfig-name>
        paused: false
      - name: <your-worker-machine-pool-name>-<cluster-name>
        quantity: 1
        displayName: <your-worker-machine-pool-name>-<cluster-name>
        controlPlaneRole: false
        etcdRole: false
        workerRole: true
        machineConfigRef:
          kind: VmwarevsphereConfig
          name: <your-vmwarevsphereconfig-name>
        paused: false
    registries: {}
    upgradeStrategy:
      controlPlaneConcurrency: 10%
      controlPlaneDrainOptions:
        timeout: 0
      workerConcurrency: 10%
      workerDrainOptions:
        timeout: 0
```
</details>

```text
For programmatically creating clusters via rest api calls you need to make sure that every 
cluster you want to create needs theire own and specific MaschinePoolConfig as well as VmwarevsphereConfig, in order to work
properly. MachinepoolConfigs as well as VmwarevsphereConfig cant no be shared clusterwide as a global ressource.   
```
## GENERAL

### KUBECONFIG

```bash
export KUBECONFIG=/etc/rancher/rke2/rke2.yaml
/var/lib/rancher/rke2/bin/kubectl get nodes
```

### LIST CONTAINERS USING CTR

```bash
/var/lib/rancher/rke2/bin/ctr --address /run/k3s/containerd/containerd.sock --namespace k8s.io container ls
```

### CRICTL

```bash
export CRI_CONFIG_FILE=/var/lib/rancher/rke2/agent/etc/crictl.yaml
/var/lib/rancher/rke2/bin/crictl ps

/var/lib/rancher/rke2/bin/crictl --runtime-endpoint unix:///run/k3s/containerd/containerd.sock ps -a
```

### LOGGING

```bash
journalctl -f -u rke2-server
/var/lib/rancher/rke2/agent/containerd/containerd.log
/var/lib/rancher/rke2/agent/logs/kubelet.log
```

## DEPLOY HA-SERVER (UPSTREAM)

### REQURIEMENTS

#### INVENTORY

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

#### REQUIREMENTS

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

## DEPLOY RKE2 W/ PLAYBOOK

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

## INSTALL METALLB /W HELM

<details><summary> INSTALL METALLB /W HELM</summary>

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm upgrade --install metallb -n metallb-system --create-namespace bitnami/metallb
```

</details>

### CREATE IPADDRESSPOOL

<details><summary>CREATE IPADDRESSPOOL</summary>

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

### CREATE L2ADVERTISEMENT

<details><summary>CREATE L2ADVERTISEMENT</summary>

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

## DEPLOY INGRESSNGINX /W HELM

<details><summary>DEPLOY INGRESSNGINX</summary>

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm upgrade --install ingress-nginx -n ingress-nginx --create-namespace ingress-nginx/ingress-nginx
```

</details>

## CREATE DNS ENTRY FOR IP ADDRESS
depending on the infrastructure, you need to create an A-record for the Ingress IP-Address

## CREATE SELFSIGNED-CERTS

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

### GENERATE SELFSIGNED-CERTS

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

### OFFICIAL DOCUMENTATION
https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/resources/update-rancher-certificate

### ADD NAMESPACE
```bash
kubectl create namespace cattle-system
```

### DEPLOY CERTS IN CLUSTER
```bash
kubectl -n cattle-system create secret tls tls-rancher-ingress \
  --cert=/tmp/certs/tls.crt \
  --key=/tmp/certs/tls.key
```
```bash
kubectl -n cattle-system create secret generic tls-ca \
  --from-file=/tmp/certs/cacerts.pem
```

### APPLY CRDS
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.crds.yaml
```

### ADD HELM REPOS FOR RANCHER INSTALLATION
```bash
helm repo add rancher-stable https://releases.rancher.com/server-charts/stable
```

### CREATE VALUES FILE FOR RANCHER BOOTSTRAP INSTALLATION
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

## INSTALL RANCHER /W HELM
```bash
helm upgrade --install rancher rancher-stable/rancher --version v2.7.9 \
  --values values.yaml -n cattle-system
```

## TEST LOGIN /W BOOTSTRAP PASSWORD FROM VALUES.YAML
open Browser of choice and connect to rancher-things.${INGRESS_HOSTNAME}.${INGRESS_DOMAIN} > use bootstrap password from values.yaml for login

## RANCHER CREATE NEW DOWNSTREAM CLUSTER
### COPY/INSTALL CA-CERTS ON DOWNSTREAM CLUSTER
copy tls.crt to /usr/local/share/ca-certificates on new Host

```bash
update-ca-certificates
```

### CREATE NEW DOWNSTREAM CLUSTER /W RANCHER
e.g. in Rancher Cluster Manager create a new cluster > copy Registration Command from web ui > execute on new Hosts cli

## ADD ADDITIONAL CLUSTER NODE (TO HA SERVER)

### GET TOKEN + CONFIG FROM MASTER NODE

```bash
cat /var/lib/rancher/rke2/token
cat /etc/rancher/rke2/config.yaml
```

### CREATE DIRECTORY ON ADDITIONAL NODE

```bash
mkdir -p /etc/rancher/rke2
```

### CREATE CONFIG YAML FOR CLUSTER

Add token to (copied) config

```bash
cat << EOF > /etc/rancher/rke2/config.yaml
---
write-kubeconfig-mode: 644
server: https://<master-ip-address>:9345
token: <token_from_master>
cni: <CNI> # e.g. canal
disable: # example
  - rke2-ingress-nginx
  - rke-snapshot-controller
EOF
```

### SET ENV VARS

```bash
export INSTALL_RKE2_VERSION=v1.28.2+rke2r1 #example - check version/github
export INSTALL_RKE2_CHANNEL_URL=https://update.rke2.io/v1-release/channels #example
export INSTALL_RKE2_CHANNEL=stable #example
export INSTALL_RKE2_METHOD=tar #example

curl -sfL https://get.rke2.io | sh -
```

### ENABLE SERVICE

```bash
systemctl enable --now rke2-server.service
```
