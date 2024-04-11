# stuttgart-things/docs/yq

## SNIPPETS

<details><summary><b>READ YAML KEYS</b></summary>

```bash
cat <<EOF > ./collection.yaml
---
name: deploy_rke
namespace: sthings
requirements: |
  roles:
    - src: https://github.com/stuttgart-things/deploy-configure-rke.git
      scm: git
      version: main
EOF

yq -r ".name" ./collection.yaml # = deploy_rke
yq -r ".requirements" ./collection.yaml # = roles ..
```

</details>

<details><summary><b>READ YAML LIST IN BASH LOOP</b></summary>

```yaml
# data.yaml
---
runners:
  - repository: download-install-binary
    cluster: cicd
  - repository: vsphere-vm
    cluster: cicd

clusters:
  cicd:
    namespace: crossplane-system
    folder: clusters/labul/vsphere/sthings-cicd/
```

```bash
#!/bin/bash

for runner in $(yq eval -o=j data.yaml | jq -cr '.runners[]'); do
      repository=$(echo $runner | jq -r '.repository' -)
      cluster=$(echo $runner | jq -r '.cluster' -)
      namespace=$(yq -r ".clusters.${cluster}.namespace" data.yaml)
      folder=$(yq -r ".clusters.${cluster}.folder" data.yaml)

      echo repository=$repository, cluster=$cluster, namespace=$namespace, folder=$folder
done

# output
# repository=download-install-binary, cluster=cicd, namespace=crossplane-system, folder=clusters/labul/vsphere/sthings-cicd/
# repository=vsphere-vm, cluster=cicd, namespace=crossplane-system, folder=clusters/labul/vsphere/sthings-cicd/
```

</details>

<details><summary><b>UPDATE/SET YAML KEYS</b></summary>

```bash
cat <<EOF > ./Chart.yaml
---
version: 1.2.3
EOF

# UPDATE KEY
yq e -i '.version = "1.2.4"' Chart.yaml

# SET KEY
yq e -i '.name = "serviceA"' Chart.yaml
```

</details>

<details><summary><b>READ YAML DICT IN A BASH LOOP</b></summary>

```yaml
playbooks:
  - name: rke1
    play: |
      - hosts: all
        become: true

        vars:
          rke_docker_version: '=5:23.0.6-1~ubuntu.22.04~jammy'
          rke_docker_ce_version: '5:23.0.6*'
          rke_version: 1
          rke_user_name: rke
          rke_installer_version: 1.4.8
          rke_kubernetes_version: v1.26.7-rancher1-1
          project_folder: rancher-things
          rke_create_rke_user: true
          network_plugin: calico
          rke2_airgapped_installation: false

        roles:
          - role: deploy-configure-rke
  - name: rke2
    play: |
      - hosts: all
        become: true
        vars:
          rke_version: 2
          rke2_k8s_version: 1.26.0
          rke2_airgapped_installation: true
          rke2_release_kind: rke2r2 # rke2r1
          disable_rke2_components:
            - rke2-ingress-nginx
            - rke-snapshot-controller
          cluster_setup: multinode
          install_containerd: false # bring your own containerd
          containerdRootPath: /var/lib/containerd/ # directory must not exist

        roles:
          - role: deploy-configure-rke
```

```bash
#!/bin/bash

# GET COUNT OF ALL KEYS OF SUBKEY PLAYBOOKS
loops=$(yq '.playbooks | keys' collection.yaml | wc -l)
echo $loops

COUNTER=0
while [ $COUNTER != $loops ]; do

   echo PLAYBOOK $COUNTER

   # GET SUBKEY
   yq ".playbooks[$COUNTER].name" collection.yaml
   filename=$(yq ".playbooks[$COUNTER].name" collection.yaml)
   play_content=$(yq ".playbooks[$COUNTER].play" collection.yaml)

   echo "$play_content" > "$filename.yaml"
   let COUNTER=COUNTER+1

done
```

</details>
