# # stuttgart-things/docs/ansible

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
  
```
export ANSIBLE_HASHI_VAULT_ADDR=<vault-url-addr>
export ANSIBLE_HASHI_VAULT_ROLE_ID=<approle-id>
export ANSIBLE_HASHI_VAULT_SECRET_ID=<secret-id>
```
  </details>

### Running multiple playbooks in a sequence.

#### Inventory
  
An inventory file should be created with the name of the desired host. Note: This file will change automatically throughout the process. 
<details><summary><b>inventory.ini</b></summary>
```
[all]
hostname
```
</details>


#### Playbook1
The following playbook uses the enviornment variables to connect into vault and extract the secrets needed to connect to the host. The username and password are saved into the inventory file (if the inv file is not in the same directory as the playbook, then the path under the "Write vars on inv file" task must be modified.). The ssh-keys (public and private) are stored as *~/.ssh/vault_key*. Finally the inventory is refreshed with the new user data included.
  
<details><summary><b>Playbook1.yaml: </b></summary>

  ```
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
  
```
[all:vars]
ansible_user=sthings
ansibel_password=Atlan7is
#ansible_connection=ssh

```
</details>


#### Playbook2
The second playbook connects to the host with the information obtained by the first playbook and then runs the desired tasks on the host. The playbook contains a general example of a task to be run within the host, and it is currenlty used to verify that the connection was made.
  
<details><summary><b>Playbook2.yaml</b></summary>
  
```
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
  
```
---
- name: Playbook_1
  import_playbook: playbook1.yaml

- name: Playbook_2
  import_playbook: playbook2.yaml
```
</details>
  
Afterwards, you can run the following command, and the playbooks will be run:
  
```
ansible-playbook main.yaml -i inventory.ini
```
