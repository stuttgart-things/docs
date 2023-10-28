# stuttgart-things/docs/ansible

## EVENT-DRIVEN-ANSIBLE (EDA)

### INSTALLATION

```bash
sudo apt install python3-pip openjdk-17-jdk maven
export PATH=$PATH:$HOME/.local/bin
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PIP_NO_BINARY=jpy
export PATH=/home/vagrant/.local/bin:$PATH
pip install wheel ansible-rulebook ansible ansible-runner
ansible-galaxy collection install community.general ansible.eda
```

### INSTALLATION ELASTICSEARCH SOURCE PLUGIN

```bash
pip install aiohttp elasticsearch python-dateutil pyyaml
ansible-galaxy collection install cloin.eda
```

### WEBHOOK RULEBOOK

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

### ELASTICSEARCH RULEBOOK

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

### INVENTORY EXAMPLE

```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
```

### PLAYBOOK EXAMPLES

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

### RULEBOOK EXECUTION

```bash
ansible-rulebook --rulebook webhook-source.yaml -i rulebook-inv -vv
```

### RULEBOOK/EDA TRIGGERING

```bash
curl -v -H 'Content-Type: application/json' -d '{"message": "install RKE"}' 10.31.103.137:5000/endpoint
```

## ANSIBLE-LINT

```yaml
pip3 install ansible-lint
cat ./.ansible-lint
skip_list:
  - 'yaml'
  - 'role-name'
ansible-lint
```

## VAULT LOOKUPS/REFRESH INVENTORY

In this example two playbooks are run automatically and consecutively.
 - The first playbook run is meant to obtain the login information of the host from vault secrets and modify.
 - The second playbook is meant to run through the host, using the login data obtained on the prevoius playbook.

In order for the second playbook to connect to the host, the data obtained from the first playbook is written into the inventory file and the inventory file is then refreshed to work with the new data.

There are two methods for ansible to connect with the host:
 - User and Password
 - ssh-key
 The example shows the use of user and password, however the clarification on how to connect with ssh-key will be done. To connect this way, you have to previously make sure that the ssh-key has already been added to the host. If necesary change */.ssh/config* to include the proper key path.

### Before we Start

  In order to prepare the system, the following environment variables have to be set in case that they have not ben set by then.

  <details><summary><b>Environment Variables</b></summary>

```bash
export ANSIBLE_HASHI_VAULT_ADDR=<vault-url-addr>
export ANSIBLE_HASHI_VAULT_ROLE_ID=<approle-id>
export ANSIBLE_HASHI_VAULT_SECRET_ID=<secret-id>
```

  </details>

### Running multiple playbooks in a sequence.

#### Inventory

An inventory file should be created with the name of the desired host. Note: This file will change automatically throughout the process.
<details><summary><b>inventory.ini</b></summary>

```bash
[all]
hostname
```

</details>

#### Playbook1

The following playbook uses the enviornment variables to connect into vault and extract the secrets needed to connect to the host. The username and password are saved into the inventory file (if the inv file is not in the same directory as the playbook, then the path under the "Write vars on inv file" task must be modified.). The ssh-keys (public and private) are stored as *~/.ssh/vault_key*. Finally the inventory is refreshed with the new user data included.

<details><summary><b>Playbook1.yaml: </b></summary>

```yaml
---
- hosts: localhost
  become: true

  vars:
    home_dir: "{{ lookup('env','HOME') }}"
    inv_dir
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
        ansibel_password={{ password }}
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

</details>

 **For ssh connection**: To connect via ssh instead of username and password, change the line within the task "Write vars on inv file". Remove the hashtag (#) before ansible_connection and add a hashtag before ansible_user and ansible_pasword.

After the first playbook is run, the inventory will look as follows:

<details><summary><b>Inventory</b></summary>

```bash
[all:vars]
ansible_user=sthings
ansible_password=<password>
#ansible_connection=ssh
```

</details>

#### Playbook2

The second playbook connects to the host with the information obtained by the first playbook and then runs the desired tasks on the host. The playbook contains a general example of a task to be run within the host, and it is currenlty used to verify that the connection was made.

<details><summary><b>Playbook2.yaml</b></summary>

```yaml
---
- hosts: all
  tasks:
    - name: env lookup
      ansible.builtin.shell: |
        whoami
        uptime
```

</details>

#### Consecutively running multiple playbooks within one playbook

The following format can be used to list the playbooks in the order in which they should be run.

<details><summary><b>main.yaml</b></summary>

```yaml
---
- name: Playbook_1
  import_playbook: playbook1.yaml

- name: Playbook_2
  import_playbook: playbook2.yaml
```

</details>

Afterwards, you can run the following command, and the playbooks will be run:

```bash
ansible-playbook main.yaml -i inventory.ini
```
