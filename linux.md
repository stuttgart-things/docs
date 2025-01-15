# stuttgart-things/docs/linux

## BASH-SNIPPETS

<details><summary><b>USE GUM IN BASH SCRIPTS FOR CHOOSING FILES</b></summary>

```bash
KUBECONFIG_FOLDER=~/.kube 
ALL_KUBECONFIGS=$(ls ${KUBECONFIG_FOLDER} | xargs -n1 printf '"%s" ') &&
SELECTED_KUBECONFIG=$(gum choose ${ALL_KUBECONFIGS}) && echo Switching to ${SELECTED_KUBECONFIG//\"/} &&
export KUBECONFIG=${KUBECONFIG_FOLDER}/${SELECTED_KUBECONFIG//\"/}; kubectl get nodes
```

</details>

<details><summary><b>RESIZE LVM</b></summary>

```bash
sudo vgdisplay vg0

sudo lvextend -L+20G /dev/mapper/vg0-var
sudo xfs_growfs /var

sudo lvextend -L+10G /dev/mapper/vg0-home
sudo xfs_growfs /home

sudo lvextend -L+20G /dev/mapper/vg0-root
sudo xfs_growfs /

df -h
```

</details>

<details><summary><b>TMUX</b></summary>

```bash
# CREATE NEW SESSION
tmux new -s runner

# DETACH SESSION (= EXIT W/O END THE SESSION)
STRG + B + :detach

# LIST EXISTING SESSIONS
tmux ls

# ATTACH EXISTING SESSION
tmux a -t runner
```

</details>

<details><summary><b>REMOVE QUOTES FROM STRING</b></summary>

```bash
echo inventory: 10.31.102.119", "10.31.102.111", "10.31.102.110 | sed 's/.\(.*\)/\0/'
```

</details>

<details><summary><b>REMOVE SPACE FROM STRING</b></summary>

```bash
echo "   3918912k " | sed 's/ //g'
```

</details>

<details><summary><b>EXTRACT TAR.XZ</b></summary>

```bash
tar -xf podlet-x86_64-unknown-linux-gnu.tar.xz
```

</details>

<details><summary><b>APPEND TEXT TO FIRST LINE OF FILE</b></summary>

```bash
echo 'vsphere_vm_template="/path/to/template"' | cat -  /tmp/vsphere-vm-tfvars.tpl
```

</details>

<details><summary><b>TAR CURRENT DIR</b></summary>

```bash
artifact_name=$(basename $PWD).tar.gz
touch ${artifact_name}
tar -czf ${artifact_name} --exclude=${artifact_name} .
```

</details>

<details><summary><b>SPLIT DELIMITED STRING</b></summary>

```bash
branch=ubuntu23-labda-vsphere
echo $(echo $branch | cut -d "-" -f 1) #ubuntu23
echo $(echo $branch | cut -d "-" -f 2) #labda
echo $(echo $branch | cut -d "-" -f 3) #vsphere
```

</details>

<details><summary><b>SEARCH FOR PATTERN IN SUBFOLDERS</b></summary>

```bash
SEARCH_PATH="/home/sthings/projects/ansible/test/collections/ansible_collections/sthings/deploy_rke/roles"
grep -A2 -B2 -Hrn 'ansible.builtin.include_role' ${SEARCH_PATH}
```

</details>

<details><summary><b>PRINT ARRAY IN ONE LINE w/ JQ</b></summary>

```bash
files=(one two three)
jq -c -n '$ARGS.positional' --args "${files[@]}"

```

</details>

<details><summary><b>EXTRACTING A STRING BETWEEN LAST TWO SLASHES IN BASH</b></summary>

```bash
string='/a/b/c/d/e'  # initial data
dir=${string%/*}     # trim everything past the last /
dir=${dir##*/}       # ...then remove everything before the last / remaining
printf '%s\n' "$dir" # demonstrate output
```

</details>



<details><summary><b>CHECK FOR VALUES IN ARRAY / EXCLUDE FROM ARRAY</b></summary>

```bash
#! /bin/bash

DIR="/home/sthings/projects/ansible/test/roles"
DIRS=$(ls ${DIR})

EXCLUDE_ROLE="configure_rke_node"
ALL_ROLES=$(echo ${DIRS[@]/$EXCLUDE_ROLE})

CHECK_FOR="download_install_binary"

if [[ ${DIRS[@]/$ALL_ROLES} =~ $CHECK_FOR ]]
then
  echo "ROLE FOUND"
else
  echo "ROLE NOT FOUND"
fi
```

</details>

<details><summary><b>SEARCH AND REPLACE IN LOOP</b></summary>

```bash
# GET ALL FILES
all_files=$(find test/install-configure-docker -type f)

# ECHO ALL FILES
echo $all_files

# SET NAMES
old=install-configure-docker
new=install_configure_docker

sed -i "s/${old}/${new}/g" $all_files
```

</details>

<details><summary><b>FIND, SEARCH AND REPLACE</b></summary>

```bash
# SEARCH FOR ALL FILES IN (SUB-)FOLDERS
find sthings/deploy_rke/roles/install_cofigure_docker -type f

# SEARCH AND REPLACE FOR ALL (FOUND) FILES IN (SUB-)FOLDERS
sed -i 's/install-configure-docker/install_configure_docker/g' $(find sthings/deploy_rke/roles/install_cofigure_docker -type f)
```

</details>

<details><summary><b>STATIC IP UBUNTU23</b></summary>

```bash
sudo cat <<EOF > /etc/netplan/00-installer-config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens192:
      dhcp4: false
      dhcp6: false
      addresses:
        - 10.100.136.210/24
      routes:
        - to: default
          via: 10.100.136.254
      nameservers:
        addresses: [10.100.101.5]
EOF

sudo chmod 600 /etc/netplan/00-installer-config.yaml
sudo netplan --debug apply
```

</details>

<details><summary><b>CUT FOLDERPATH W/ SED FROM URL</b></summary>

```bash
git clone https://github.com/stuttgart-things/stuttgart-things.git
cd $(echo $(params.REPO_URL) | sed 's|.*/||' | sed 's/.git//g')
# https://github.com/stuttgart-things/stuttgart-things.git -> stuttgart-things
```

</details>

<details><summary><b>SPLIT STRINGS BY DELIMITER (+-) W/ AWK</b></summary>

```bash
path=$(awk -F+- '{print $1}' <<< 'git/data/github:token+-false+-GITHUB_TOKEN') # =git/data/github:token
convert=$(awk -F+- '{print $2}' <<< 'git/data/github:token+-false+-GITHUB_TOKEN') # =false
token=$(awk -F+- '{print $3}' <<< 'git/data/github:token+-false+-GITHUB_TOKEN') # =GITHUB_TOKEN
```

</details>

<details><summary><b>LOOP OVER PARAMETERS W/ SET + FOR LOOP</b></summary>

```bash
set great foo bar # set parameters
echo "$@" # test output
for argument in "$@"; do echo $argument ; done # loop over parameters

# loop over parameters andchange +- to : w/ sed
for argument in "$@"; do echo $argument | sed -e "s/+-/: /g" ; done
```

</details>

<details><summary><b>CONCATENATE SET PARAMETERS + FOR LOOP</b></summary>

```bash
set 'scanners vuln' 'timeout 30m'
output=" "; for argument in "$@"; do output=${output}'--'$argument' '; done
echo ${output} #--scanners vuln --timeout 30m
```

</details>

<details><summary><b>INSTALL PUB CERTS</b></summary>

```bash
# UBUNTU/ALPINE
VAULT_URL_LABUL=https://vault.labul.sva.de:8200
VAULT_URL_LABDA=https://vault.tiab.labda.sva.de:8200
VAULT_URL_LABUL_VSPHERE=https://vault-vsphere.labul.sva.de:8200
VAULT_URL_LABUL_PVE=https://vault-pve.labul.sva.de:8200
VAULT_URL_LABDA_VSPHERE=https://vault-vsphere.tiab.labda.sva.de:8200

# INSTALL VAULT CERTS
sudo wget -O /usr/local/share/ca-certificates/labul-ca.crt ${VAULT_URL_LABUL}/v1/pki/ca/pem --no-check-certificate \
sudo wget -O /usr/local/share/ca-certificates/labda-ca.crt ${VAULT_URL_LABDA}/v1/pki/ca/pem --no-check-certificate \
sudo wget -O /usr/local/share/ca-certificates/labul-vsphere-ca.crt ${VAULT_URL_LABUL_VSPHERE}/v1/pki/ca/pem --no-check-certificate \
sudo wget -O /usr/local/share/ca-certificates/labda-vsphere-ca.crt ${VAULT_URL_LABDA_VSPHERE}/v1/pki/ca/pem --no-check-certificate \
sudo wget -O /usr/local/share/ca-certificates/labul-pve.crt ${VAULT_URL_LABUL_PVE}/v1/pki/ca/pem --no-check-certificate \
sudo update-ca-certificates
```

</details>

<details><summary><b>GET VERSION NUMBER W/ AWK</b></summary>

```bash
python3 --version # Python 3.10.12
python3 --version | awk '{print $2}' # 3.10.12
```

</details>

<details><summary><b>UNTIL LOOP</b></summary>

```bash
#!/bin/bash

until skopeo inspect docker://registry.fedoraproject.org/fedora:latest
do
    echo checking..
    sleep 1
done
```

</details>

<details><summary><b>CHECK TEKTON PIPELINERUN STATUS IN WHILE LOOP W/ OPERATORS</b></summary>

```bash
#!/bin/bash
sleep=10
failed_prs=0
succeeded_prs=0
retries=0
max_retries=3

all_prs=$(tkn pr list -n tektoncd | grep -c alpine)
echo all pipelineRuns: ${all_prs}

while [[ ${failed_prs} -le 0  ]] || [[ ${succeeded_prs} -eq ${all_prs} ]] || [[ ${retries} -eq ${max_retries} ]]
do
    echo ${retries_left} retries left
    echo check/retry in ${sleep} seconds..
    sleep ${sleep}

    failed_prs=$(tkn pr list -n tektoncd | grep alpine | grep -c Failed)
    echo Failed pipelineRuns: ${failed_prs}
    tkn pr list -n tektoncd | grep alpine | grep Failed

    succeeded_prs=$(tkn pr list -n tektoncd | grep alpine | grep -c Succeeded)
    echo Succeeded pipelineRuns: ${succeeded_prs}
    tkn pr list -n tektoncd | grep alpine | grep Succeeded

    retries=`expr ${retries} + 1`
    retries_left=`expr ${max_retries} - ${retries}`
done

echo "Done watching pipelineRuns!"
echo Failed pipelineRuns: ${failed_prs}
echo Succeeded pipelineRuns: ${succeeded_prs}
```

</details>


<details><summary><b>DHCP Network config</b></summary>

```bash
cat <<EOF > 99_config.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true
EOF

sudo netplan apply
```

</details>

<details><summary><b>Enable ssh password authentication</b></summary>

```bash
vi /etc/ssh/sshd_config
# set this variable to yes to allow passwords
PaswordAuthentication yes
# Restart Service
sudo systemctl restart ssh
# Copy public key to remote machine
ssh-copy-id ubuntu@192.168.1.157
```

</details>
