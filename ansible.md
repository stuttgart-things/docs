# Ansible

## Molecule

https://cloudautomation.pharriso.co.uk/post/vmware-molecule/
https://medium.com/@fabio.marinetti81/validate-ansible-roles-through-molecule-delegated-driver-a2ea2ab395b5

<details><summary><b>Custom Inventory with Molecule</b></summary>

```bash
molecule init scenario --driver-name=default
```

```bash
cat <<EOF > ./molecule/default/inventory.yaml
---
all:
  hosts:
    michigan.labul.sva.de
EOF
```

```bash
cat <<EOF > ./molecule/default/molecule.yml
---
role_name_check: 1
driver:
  name: default
  managed: False
platforms:
  - name: localhost #michigan.labul.sva.de
provisioner:
  name: ansible
  env:
    ANSIBLE_VERBOSITY: 3
  playbooks:
    converge: ${MOLECULE_PLAYBOOK:-converge.yml}
  inventory:
    links:
      hosts: inventory.yaml

scenario:
  name: default
  test_sequence:
    - dependency
    - syntax
    - prepare
    - converge
EOF
```

</details>

<details><summary><b>Test Existing Role with Molecule Docker Driver</b></summary>

```bash
mkdir -p molecule-testing && cd $_
```

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U setuptools pip 'molecule'
pip install molecule-docker
molecule --version
```

```bash
ansible-galaxy init hardening && cd hardening
molecule init scenario -d docker docker_test

yq eval '.galaxy_info.role_name = "hardening"' -i meta/main.yml
yq eval '.galaxy_info.author = "patrick hermann"' -i meta/main.yml
yq eval '.galaxy_info.namespace = "sthings"' -i meta/main.yml

# hardening/tasks
cat <<EOF >> ./tasks/main.yml
---
- name: OS Hardening task
  debug:
    msg: "Performing OS hardening tasks for {{ ansible_distribution }} {{ ansible_distribution_version }}"
EOF

cat <<EOF > ./molecule/docker_test/converge.yml
---
- name: Converge
  hosts: all
  gather_facts: true

  roles:
    - sthings.hardening
EOF

cat <<EOF > ./molecule/docker_test/molecule.yml
---
driver:
  name: docker
platforms:
  - name: instance
    image: quay.io/centos/centos:stream9
    pre_build_image: false
EOF

molecule test -s docker_test
```

</details>

## Snippets

<details><summary><b>Create Collections</b></summary>

```bash
# EXAMPLE COLLECTION CREATION
ansible-galaxy collection init sthings.deploy_rke

# BUILD COLLECTION
ansible-galaxy collection build sthings/deploy_rke/ --force

# INSTALL COLLECTION
ansible-galaxy collection install sthings-deploy_rke-1.0.0.tar.gz --force
```

</details>

<details><summary><b>Copy Standalone Role</b></summary>

```bash
# CREATE ROLE DIR INSIDE COLLECTION ROLES DIR
mkdir -p sthings/deploy_rke/roles/install_configure_docker

# COPY ROLE CONTENT TO COLLECTION ROLE
cp -R install-configure-docker/* sthings/deploy_rke/roles/install_configure_docker

# RENAME (OLD) ROLE NAME/REFERENCES
sed -i 's/install-configure-docker/install_configure_docker/g' $(find sthings/deploy_rke/roles/install_configure_docker -type f)
```

</details>

<details><summary><b>Import Playbook from Collection</b></summary>

```bash
# CREATE PLAYBOOK DIR INSIDE COLLECTION
mkdir -p sthings/deploy_rke/playbooks

# CREATE PLAYBOOK INSIDE COLLECTION
cat <<EOF > sthings/deploy_rke/playbooks/install_docker.yml
---
- hosts: "{{ hosts | default('all') }}"
  tasks:
    - include_role:
        name: install_configure_docker
EOF

# BUILD +INSTALL ROLE
ansible-galaxy collection build sthings/deploy_rke/ --force
ansible-galaxy collection install sthings-deploy_rke-1.0.0.tar.gz --force

# SET COLLECTIONS PATH AS ENV VAR
export ANSIBLE_COLLECTIONS_PATH=/home/sthings/projects/ansible/test/collections/

# IMPORT PLAY FROM COLLECTION
cat <<EOF > /tmp/import-install-docker.yaml
---
- import_playbook: sthings.deploy_rke.install_docker
EOF

# RUN PLAY FROM COLLECTION
ansible-playbook sthings.deploy_rke.install_docker -i inv -vv
```

</details>

## Task Snippets

<details><summary><b>Loop Over Dict</b></summary>

```yaml
---
- hosts: localhost
  vars:
    organizations:
      stuttgartThings:
        name: stuttgart-things
        description: stuttgart-things organization
        state: present

  tasks:
    - name: Create organizations
      awx.awx.organization:
        name: "{{ item.value.name }}"
        description: "{{ item.value.description }}"
        state: "{{ item.value.state }}"
        validate_certs: no
      loop: "{{ lookup('dict', organizations, wantlist=True) }}"
```

</details>

<details><summary><b>Wait for Custom K8s Resource to be Created/Ready</b></summary>

```yaml
---
- hosts: localhost
  become: no
  gather_facts: no
  environment:
    K8S_AUTH_KUBECONFIG: "~/.kube/automationLab"
  vars:
    resource_name: warschau
    resource_namespace: terraform
    api_version: machineshop.sthings.tiab.ssc.sva.de/v1beta1

  tasks:
    - name: Wait until resource is created
      kubernetes.core.k8s_info:
        api_version: "{{ api_version }}"
        kind: terraform
        name: "{{ resource_name }}"
        namespace: "{{ resource_namespace }}"
        wait: yes
        wait_timeout: 900

    - name: Wait for operator to build vm
      ansible.builtin.shell: |
        kubectl get terraform {{ resource_name }} -n {{ resource_namespace }} -o jsonpath={.status.conditions[0].status}
      register: resource_state
      until: resource_state.stdout == "True"
      retries: 60
      delay: 15
```

</details>

## Extend Ansible

<details><summary><b>Add (Local) Custom (Python) Module</b></summary>
```bash
# GET MODULES PATH
ansible-config dump |grep DEFAULT_MODULE_PATH
# output e.g. /usr/share/ansible/plugins/modules

# CREATE MODULES DIR (IF NOT EXISTS)
sudo mkdir -p /usr/share/ansible/plugins/modules

# OPTIONAL: DOWNLOAD SCRIPT FROM WEB
wget https://raw.githubusercontent.com/krahul084/python_scripts/master/get_checksum.py

# MOVE THE SCRIPT TO MODULES DIR
sudo mv get_checksum.py /usr/share/
ansible/plugins/modules
```

```yaml
# USE MODULE IN ANSIBLE TASK
# ...
- get_checksum:
    path: "{{ golang_install_dir }}go"
    checksum_type: "{{ go_checksum_type }}"
  register: checksum_old
  when: check_golang.stat.exists
# ...
```

</details>

## Event-Driven Ansible (EDA)

### Installation

<details><summary><b>Example Installation</b></summary>

```bash
sudo apt install python3-pip openjdk-17-jdk maven
export PATH=$PATH:$HOME/.local/bin
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PIP_NO_BINARY=jpy
export PATH=/home/vagrant/.local/bin:$PATH
pip install wheel ansible-rulebook ansible ansible-runner
ansible-galaxy collection install community.general ansible.eda
```

</details>

### Installation Elasticsearch Source Plugin

<details><summary><b>Example Installation Elasticsearch Plugin</b></summary>

```bash
pip install aiohttp elasticsearch python-dateutil pyyaml
ansible-galaxy collection install cloin.eda
```

</details>

### Webhook Rulebook

<details><summary><b>Example Webhook Rulebook</b></summary>

```yaml
---
- name: Listen for events on a webhook
  hosts: all

  ## Define our source for events
  sources:
    - ansible.eda.webhook:
        host: 0.0.0.0
        port: 5000
      filters:
        - ansible.eda.insert_hosts_to_meta:
            host_path: event.payload.source

  rules:
    - name: Say Hello
      condition: event.payload.message == "install RKE"
      action:
        run_playbook:
          name: deployK3s2.yaml
```

</details>

### Elasticsearch Rulebook

<details><summary><b>Example Elasticsearch Rulebook</b></summary>

```yaml
---
- name: Elastic events
  hosts: all
  sources:
    - cloin.eda.elastic:
        elastic_host: <elasticsearch_url>
        elastic_port: 9200
        elastic_index_pattern: metricbeat-*
        query: |
          term:
            vsphere.virtualmachine.memory.used.guest.bytes: 0
        interval: 60

  rules:
    - name: Start vm if state is powerd off
      condition: event.ecs is defined and event.vsphere.virtualmachine.name == "vm-name"
      action:
        run_playbook:
          name: vsphere.yaml
```

</details>

### Inventory Example

<details><summary><b>Example Inventory</b></summary>

```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
```

</details>

### Playbook Examples

<details><summary><b>Example Playbook</b></summary>

```yaml
- hosts: localhost
  connection: local
  tasks:
    - debug:
        msg: "Thank you, my friend!"
```

```yaml
---
- hosts: localhost
  vars:
    vcenter_hostname: <vcenter_url>
    vcenter_username: <user>
    vcenter_password: <password>
    vcenter_datacenter: <datacenter>
    vm_name: <vm-name>
    vm_folder: <folder>

  tasks:
    - name: "Get uuid of {{ vm_name }}"
      community.vmware.vmware_guest_info:
        hostname: "{{ vcenter_hostname }}"
        username: "{{ vcenter_username }}"
        password: "{{ vcenter_password }}"
        datacenter: "{{ vcenter_datacenter }}"
        name: "{{ vm_name }}"
        folder: "{{ vm_folder }}"
        validate_certs: False
      register: vm_facts

    - name: "Set facts of {{ vm_name }}"
      ansible.builtin.set_fact:
        vm_uuid: "{{ vm_facts.instance.hw_product_uuid }}"
        power_status: "{{ vm_facts.instance.hw_power_status }}"

    - name: "Check power status of {{ vm_name }}"
      ansible.builtin.debug:
        var: power_status

    - name: Set powerstate of a virtual machine to poweroff by using UUID
      community.vmware.vmware_guest:
        hostname: "{{ vcenter_hostname }}"
        username: "{{ vcenter_username }}"
        password: "{{ vcenter_password }}"
        validate_certs: no
        uuid: "{{ vm_uuid }}"
        state: poweredon
      delegate_to: localhost
      when: power_status == "poweredOff"
```

</details>

### Rulebook Execution

<details><summary><b>Example Rulebook Execution</b></summary>

```bash
ansible-rulebook --rulebook webhook-source.yaml -i rulebook-inv -vv
```

</details>

### Rulebook/EDA Triggering

<details><summary><b>Example Rulebook/EDA Triggering</b></summary>

```bash
curl -v -H 'Content-Type: application/json' -d '{"message": "install RKE"}' 10.31.103.137:5000/endpoint
```

</details>

## Ansible-Lint

<details><summary><b>Example Ansible Linting</b></summary>

```yaml
pip3 install ansible-lint
cat ./.ansible-lint
skip_list:
  - 'yaml'
  - 'role-name'
ansible-lint
```

</details>

## Development Snippets

<details><summary><b>(Further) Development of Existing Ansible Roles</b></summary>

### Clone or Switch to Existing Remote Branch

```bash
mkdir -p ~/ansible/dev/ && cd ~/ansible/dev/ # example dir
git clone git@github.com:stuttgart-things/download-install-binary.git # example role
cd download-install-binary

# CREATE NEW BRANCH AND CHANGE INTO
BRANCH_NAME=feature/issue-x/feature-name
git checkout main && git branch && git pull
git checkout -b ${BRANCH_NAME}
git push origin ${BRANCH_NAME}
git branch --set-upstream-to=origin/main ${BRANCH_NAME}
git branch

# OR SWITCH TO EXISTING REMOTE BRANCH
git fetch && git branch -r
BRANCH=feature/issue-1/update-version-check # example
git pull origin main
git switch feature/issue-1/update-version-check && git pull
```

### Test with Dev Role (if Role is Already Installed Systemwide)

```bash
# RUN THE (TEST) PLAYBOOK FROM ROLES DIR OR FROM ROLES TESTS FOLDER
cd ~/ansible/dev/download-install-binary && cd ..
ansible-playbook ./download-install-binary/tests/execute-download-install-binary.yaml -vv

# OR SET ROLES PATH AS ENV VAR
export ANSIBLE_ROLES_PATH=~/projects/ansible/dev/ # example
# VERIFY TASK PATH: IN ANSIBLE OUTPUT
```

</details>

<details><summary><b>Install Roles from Requirements File</b></summary>

```yaml
# roles.yaml
---
roles:
  - src: https://github.com/stuttgart-things/deploy-configure-rke.git
    scm: git
    version: main
```

```bash
ansible-galaxy install -r ./roles.yaml -p ./roles
```

</details>

## Vault Lookups/Refresh Inventory

<details><summary><b>Running Multiple Playbooks with Vault Secrets</b></summary>

### Overview

In this example two playbooks are run automatically and consecutively.

- The first playbook run is meant to obtain the login information of the host from vault secrets and modify.
- The second playbook is meant to run through the host, using the login data obtained on the previous playbook.

In order for the second playbook to connect to the host, the data obtained from the first playbook is written into the inventory file and the inventory file is then refreshed to work with the new data.

There are two methods for ansible to connect with the host:

- User and Password
- ssh-key

The example shows the use of user and password, however the clarification on how to connect with ssh-key will be done. To connect this way, you have to previously make sure that the ssh-key has already been added to the host. If necesary change _/.ssh/config_ to include the proper key path.

### Before we Start

In order to prepare the system, the following environment variables have to be set in case that they have not been set by then.

```bash
export ANSIBLE_HASHI_VAULT_ADDR=<vault-url-addr>
export ANSIBLE_HASHI_VAULT_ROLE_ID=<approle-id>
export ANSIBLE_HASHI_VAULT_SECRET_ID=<secret-id>
```

### Inventory Setup

An inventory file should be created with the name of the desired host. Note: This file will change automatically throughout the process.

**inventory.ini:**
```bash
[all]
hostname
```

### Playbook 1 - Retrieve Vault Secrets

The following playbook uses the environment variables to connect into vault and extract the secrets needed to connect to the host. The username and password are saved into the inventory file (if the inv file is not in the same directory as the playbook, then the path under the "Write vars on inv file" task must be modified.). The ssh-keys (public and private) are stored as _~/.ssh/vault_key_. Finally the inventory is refreshed with the new user data included.

**playbook1.yaml:**
```yaml
---
- hosts: localhost
  become: true

  vars:
    home_dir: "{{ lookup('env','HOME') }}"
    vault_approle_id: "{{ lookup('env', 'ANSIBLE_HASHI_VAULT_ROLE_ID') }}"
    vault_approle_secret: "{{ lookup('env', 'ANSIBLE_HASHI_VAULT_SECRET_ID') }}"
    vault_url: "{{ lookup('env', 'ANSIBLE_HASHI_VAULT_ADDR') }}"

    username: "{{ lookup('community.hashi_vault.hashi_vault', 'secret=ssh/data/sthings:username validate_certs=false auth_method=approle role_id={{ vault_approle_id }} secret_id={{ vault_approle_secret }} url={{ vault_url }}') }}"
    password: "{{ lookup('community.hashi_vault.hashi_vault', 'secret=ssh/data/sthings:password validate_certs=false auth_method=approle role_id={{ vault_approle_id }} secret_id={{ vault_approle_secret }} url={{ vault_url }}') }}"
    pubKey: "{{ lookup('community.hashi_vault.hashi_vault', 'secret=ssh/data/sthings:publicKey validate_certs=false auth_method=approle role_id={{ vault_approle_id }} secret_id={{ vault_approle_secret }} url={{ vault_url }}') }}"
    privKey: "{{ lookup('community.hashi_vault.hashi_vault', 'secret=ssh/data/sthings:privateKey validate_certs=false auth_method=approle role_id={{ vault_approle_id }} secret_id={{ vault_approle_secret }} url={{ vault_url }}') }}"

  tasks:
  - name: Write vars on inv file
    ansible.builtin.lineinfile:
      path: "inventory.ini"
      line: |
        [all:vars]
        ansible_user={{ username }}
        ansible_password={{ password }}
        #ansible_connection=ssh

  - name: Creating ssh private key file
    ansible.builtin.copy:
      dest: "{{ home_dir }}/.ssh/vault_key"
      content: "{{ privKey | b64decode }}"
      mode: 0644

  - name: Creating ssh public key file
    ansible.builtin.copy:
      dest: "{{ home_dir }}/.ssh/vault_key.pub"
      content: "{{ pubKey | b64decode }}"
      mode: 0644

  - meta: refresh_inventory  # Reloads the Inventory
```

**For SSH connection**: To connect via ssh instead of username and password, change the line within the task "Write vars on inv file". Remove the hashtag (#) before ansible_connection and add a hashtag before ansible_user and ansible_password.

**After the first playbook is run**, the inventory will look as follows:

```bash
[all:vars]
ansible_user=sthings
ansible_password=<password>
#ansible_connection=ssh
```

### Playbook 2 - Execute Tasks on Host

The second playbook connects to the host with the information obtained by the first playbook and then runs the desired tasks on the host. The playbook contains a general example of a task to be run within the host, and it is currently used to verify that the connection was made.

**playbook2.yaml:**
```yaml
---
- hosts: all
  tasks:
    - name: env lookup
      ansible.builtin.shell: |
        whoami
        uptime
```

### Main Playbook - Orchestration

The following format can be used to list the playbooks in the order in which they should be run.

**main.yaml:**
```yaml
---
- name: Playbook_1
  import_playbook: playbook1.yaml

- name: Playbook_2
  import_playbook: playbook2.yaml
```

### Execution

Afterwards, you can run the following command, and the playbooks will be run:

```bash
ansible-playbook main.yaml -i inventory.ini
```

</details>
