# stuttgart-things/docs/packer

## GENERAL

<details><summary><b>PACKER BUILD</b></summary>

```bash
touch meta-data
packer build -force -var "username=<USERNAME>" -var "password=<PASSWORD>" ubuntu23.pkr.hcl
```

</details>

<details><summary><b>PACKER BUILD WITH LOGS</b></summary>

```bash
export PACKER_LOG_PATH="packerlog.txt"
export PACKER_LOG=1
touch meta-data
packer build -force -var "username=<USERNAME>" -var "password=<PASSWORD>" ubuntu23.pkr.hcl
```

</details>

## SNIPPETS VSPHERE

<details><summary><b>GOVC</b></summary>

```bash
# INSTALL
export GOVC_VERSION=0.34.2
sudo curl -L https://github.com/vmware/govmomi/releases/download/v{{ GOVC_VERSION }}/govc_linux_amd64.gz |sudo gunzip > /usr/local/bin/govc

# CONFIG
export GOVC_INSECURE='TRUE'
export GOVC_URL='https://${USER}:${PASSWORD}@${VCENTER_FQDN}/sdk'

# USAGE
govc version
govc ls

# COPY ISO TO DATASTORE (EXAMPLE)
govc datastore.upload -ds="/NetApp-HCI-Datacenter/datastore/DatastoreCluster/NetApp-HCI-Datastore-04" ./ubuntu-22.04.4-server-amd64.iso iso-files/ubuntu-22.04.4-server-amd64.iso

# IMPORT OVA TO DATASTORE (EXAMPLE)
govc import.ova -ds="/NetApp-HCI-Datacenter/datastore/DatastoreCluster/NetApp-HCI-Datastore-04" ubuntu-18.04-server-cloudimg-amd64.ova
```


</details>

<details><summary><b>UBUNTU23</b></summary>

```hcl
#u23.pkr.hcl
packer {
  required_version = ">= 1.10.1"
  required_plugins {
    vmware = {
      source  = "github.com/hashicorp/vsphere"
      version = ">= 1.2.4"
    }
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = ">= 1.1.1"
    }
  }
}

source "vsphere-iso" "autogenerated_1" {
  CPUs                 = 8
  RAM                  = 8192
  RAM_reserve_all      = true
  boot_command         = ["<esc><esc><esc><esc>e<wait>", "linux /casper/vmlinuz autoinstall quiet ---<enter><wait>", "initrd /casper/initrd<enter><wait>", "boot<enter>", "<enter><f10><wait720>"]
  boot_order           = "disk,cdrom"
  ip_settle_timeout    = "20s"
  boot_wait            = "5s"
  cd_files             = ["/home/sthings/projects/packer/u23-labul-vsphere/user-data", "/home/sthings/projects/packer/u23-labul-vsphere/meta-data"]
  cd_label             = "cidata"
  cluster              = "/LabUL/host/Cluster-V6.5"
  convert_to_template  = "true"
  datastore            = "/LabUL/datastore/UL-ESX-SAS-01"
  disk_controller_type = ["pvscsi"]
  folder               = "/stuttgart-things/packer"
  guest_os_type        = "ubuntu64Guest"
  host                 = "/LabUL/host/Cluster-V6.5/10.31.101.41"
  insecure_connection  = "true"
  ip_wait_timeout      = "30m"
  iso_checksum         = "c7cda48494a6d7d9665964388a3fc9c824b3bef0c9ea3818a1be982bc80d346b"
  iso_urls             = ["https://releases.ubuntu.com/lunar/ubuntu-23.04-live-server-amd64.iso"]
  network_adapters {
    network      = "/LabUL/network/LAB-10.31.102"
    network_card = "vmxnet3"
  }
  notes                  = "stuttgart-things/ubuntu23\n\nBuild Date: ${local.packerstarttime} w/ packer\nOS: ubuntu23\nISO: https://releases.ubuntu.com/lunar/ubuntu-23.04-live-server-amd64.iso\nProvisioning: base-os\n\n/Patrick Hermann (patrick.hermann@sva.de)\n/Christian Mueller (christian.mueller@sva.de)\n"
  password               = "${var.password}"
  ssh_handshake_attempts = "900"
  ssh_password           = "ubuntu"
  ssh_timeout            = "30m"
  ssh_username           = "ubuntu"
  storage {
    disk_size             = 15360
    disk_thin_provisioned = true
  }
  username       = "${var.username}"
  vcenter_server = "10.31.101.51"
  vm_name        = "u23-04-24"
}

build {
  sources = ["source.vsphere-iso.autogenerated_1"]

  provisioner "shell" {
    inline = ["sudo apt-get -y update; sudo apt-get -y upgrade; sudo apt-get -y install python3; sudo apt-get autoremove --purge -y && sudo apt-get autoclean -y && sudo apt-get clean -y; sudo truncate -s 0 /etc/machine-id && echo 'machine-id was reset successfully'; sudo systemctl stop systemd-resolved; sudo sed -i 's/#DNSStubListener=yes/DNSStubListener=no/g' /etc/systemd/resolved.conf; sudo rm /etc/resolv.conf; sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf; sudo systemctl start systemd-resolved"]
  }

  provisioner "ansible" {
    ansible_env_vars     = ["ANSIBLE_REMOTE_TEMP=/tmp", "ANSIBLE_HOST_KEY_CHECKING=False", "ANSIBLE_SSH_ARGS=-oForwardAgent=yes -oControlMaster=auto -oControlPersist=60s -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa", "ANSIBLE_NOCOLOR=True"]
    extra_arguments      = ["-e ansible_ssh_pass=ubuntu -vv"]
    keep_inventory_file  = "true"
    playbook_file        = "/home/sthings/projects/packer/u23-labul-vsphere/base-os.yaml"
    galaxy_file          = "/home/sthings/projects/packer/u23-labul-vsphere/requirements.yaml"
    galaxy_force_install = "true"
    use_proxy            = "false"
    user                 = "ubuntu"
  }
}

locals {
  packerstarttime = formatdate("YYYYMMDD", timestamp())
}

variable "password" {
  type = string
}

variable "username" {
  type = string
}
```

```
#user-data
#cloud-config
autoinstall:
  version: 1
  network:
    version: 2
    renderer: networkd
    ethernets:
      ens192:
        dhcp4: false
        dhcp6: false
        addresses:
          - 10.31.102.221/24
        routes:
          - to: default
            via: 10.31.102.251
        nameservers:
          addresses: [10.31.101.50]
  locale: en_US.UTF-8
  keyboard:
    layout: de
    toggle: null
    variant: ''
  apt:
    disable_components: []
    geoip: true
    preserve_sources_list: false
    primary:
    - arches:
      - amd64
      - i386
      uri: http://de.archive.ubuntu.com/ubuntu
    - arches:
      - default
      uri: http://ports.ubuntu.com/ubuntu-ports
  drivers:
    install: false
  kernel:
    package: linux-generic
  storage:
    config:
      -
        id: disk-sda
        type: disk
        grub_device: true
        name: ""
        #path: /dev/sda
        match:
          size: largest
        preserve: false
        ptable: gpt
        wipe: superblock
      -
        id: partition-0
        type: partition
        device: disk-sda
        flag: bios_grub
        number: 1
        preserve: false
        size: 1048576
      -
        id: partition-1
        type: partition
        device: disk-sda
        flag: ""
        number: 2
        preserve: false
        size: 536870912
        wipe: superblock
      -
        id: partition-2
        type: partition
        device: disk-sda
        number: 3
        preserve: false
        flag: ""
        size: -1
        wipe: superblock
      -
        id: lvm_volgroup-0
        type: lvm_volgroup
        devices:
          - partition-2
        name: vg0
        preserve: false
      -
        id: lvm_partition-0
        type: lvm_partition
        name: swap
        preserve: false
        size: 2147483648
        volgroup: lvm_volgroup-0
      -
        id: lvm_partition-1
        type: lvm_partition
        name: var
        preserve: false
        size: 2147483648
        volgroup: lvm_volgroup-0
      -
        id: lvm_partition-2
        type: lvm_partition
        name: home
        preserve: false
        size: 2147483648
        volgroup: lvm_volgroup-0
      -
        id: lvm_partition-3
        type: lvm_partition
        name: root
        preserve: false
        size: -1
        volgroup: lvm_volgroup-0
      -
        id: format-0
        type: format
        fstype: ext4
        preserve: false
        volume: partition-1
      -
        id: format-1
        type: format
        fstype: swap
        preserve: false
        volume: lvm_partition-0
      -
        id: format-2
        type: format
        fstype: xfs
        preserve: false
        volume: lvm_partition-1
      -
        id: format-3
        type: format
        fstype: xfs
        preserve: false
        volume: lvm_partition-2
      -
        id: format-4
        type: format
        fstype: xfs
        preserve: false
        volume: lvm_partition-3
      -
        id: mount-0
        type: mount
        device: format-0
        path: /boot
      -
        id: mount-1
        type: mount
        device: format-4
        path: /
      -
        id: mount-2
        type: mount
        device: format-2
        path: /var
      -
        id: mount-3
        type: mount
        device: format-3
        path: /home
  identity:
    hostname: localhost
    username: ubuntu
    password: $6$rounds=656000$r6635QXd9WQ08Tgk$wDjmJsQa4GcTsh/XZG47f7mzVUeYOd1QietsPwbDFh9E.8wjogt8c5DIzLU1q6s.htUfmlslKpD9bznyQD0cb1
  ssh:
    install-server: yes
  packages:
    - qemu-guest-agent
    - open-vm-tools
    - network-manager
  user-data:
    disable_root: false
  late-commands:
    - sed -i 's/^#*\(send dhcp-client-identifier\).*$/\1 = hardware;/' /target/etc/dhcp/dhclient.conf
    - 'sed -i "s/dhcp4: true/&\n      dhcp-identifier: mac/" /target/etc/netplan/00-installer-config.yaml'
    - 'sed -i "s/version: 2/&\n  renderer: NetworkManager/" /target/etc/netplan/00-installer-config.yaml'
    - echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' > /target/etc/sudoers.d/ubuntu
    - systemctl disable systemd-networkd.service --now
```

```yaml
#base-os.yaml
---
- name: Provision vm template during packer build w/ ansible
  hosts: default
  become: true

  vars:
    update_packages: true
    install_requirements: true
    install_motd: false
    cloudinit: false
    create_rke_user: false
    update_os: true
    install_docker: false
    install_docker_compose: false
    set_docker_proxy: false
    template_creation_setup: false
    configure_rke_node: false
    create_user: true
    admin_group: "{{ 'wheel' if ansible_os_family == 'RedHat' else 'sudo' }}"
    reboot_prio_provisioning: false
    send_to_msteams: true
    vault_instances:
      - https://vault.tiab.labda.sva.de:8200
      - https://vault.labul.sva.de:8200
      - https://vault-vsphere.labul.sva.de:8200
      - https://vault-vsphere.tiab.labda.sva.de:8200
      - https://vault-vsphere.tiab.labda.sva.de:8200
    ubuntu_network_config: |
      # This is the network config written by 'subiquity'
      network:
        ethernets:
          ens18:
            dhcp4: true
            dhcp-identifier: mac
        version: 2
        renderer: NetworkManager
    path_ubuntu_network_config: /etc/netplan/00-installer-config.yaml
    copy_network_config: true

    msteams_webhook_url: "https://365sva.webhook.office.com/webhookb2/2f14a9f8-4736-46dd-9c8c-31547ec37180@0a65cb1e-37d5-41ff-980a-647d9d0e4f0b/IncomingWebhook/37a805a0a2624dc2ac1aedd7dec6ad49/dc3a27ed-396c-40b7-a9b2-f1a2b6b44efe"
    groups_to_create:
      - name: sthings
        gid: 3000

    users:
      - username: sthings
        name: sthings user
        uid: 1112
        home: /home/sthings
        enable_ssh_tcp_forwarding: false
        groups: ["{{ admin_group }}", "sthings"]
        password: "$6$rounds=656000$7ala77Ra$8/cD2EL.AIGNZhXyjB/MJS2Uru0k37I3yWZ.7jFKwQiG1VvMZtKb.B.z5nX2jb.bsLGlZejM4JwGgVrQHyONO."
        ssh_key:
          - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCslDwiVO/EvWLVVY1Twpc7Lhr9laLPgu+iiOuvMEg8E4hnEDHRPZpdD6YnnJYsLnVHbi8Y3EPDQ2UDbHnfgeYPa94XHdhGSCsIX+tA5+PLFSFgoyCtA5oWc3vrm58RX6DQXf7fPytwxIESPjIgEDv2BTOEc+pk0S09e3jttmFsrKzB7tOutB3FktcLnxGD75JgBa9/i0zmfcchF2VNZcgZRXJ5JiMGKhaKB7qZ6AoMQlDmCvllLSdCxGIxu/quiBcGhaJBMmpkSTeRouU1YWg05wEjyg47DwJyyEMzvYe6LIHxN3zBXMTBzUKJC1thGNC9yaFeywrz+iaIk66RGcjL sthings"
          - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCsHiyet7tO+qXYKEy6XBiHNICRfGsBZYIo/JBQ2i16WgkC7rq6bkGwBYtni2j0X2pp0JVtcMO+hthqj37LcGH02hKa24eAoj2UdnFU+bhYxA6Mau1B/5MCkvs8VvBjxtM3FVJE7mY5bZ19YrKJ9ZIosAQaVHiGUu1kk49rzQqMrwT/1PNbUYW19P8J2LsfnaYJIl4Ljbxr0k52MGdbKwgxdph3UKciQz2DhutrmO0gf3Ncn4zpdClldaBtDB0EMMqD3BAtEVsucttzqdeYQwixMTtyuGpAKAJNUqhpleeVhShPZLke0vXxlA6/fyfkSM78gN2FQcRGVPN6hOMkns/b patrick@TPPHERMANN"
          - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDvaTdixTdzySc6qQZavxvrBk1KNy4g30pIu9SbxVe6GuPyJzEWUYHvJt6d4YqdpavT21IQkmuex7n4qxg8ZgrmXUTpELLM2y2Uu7va/OUol4t2Q0O7hFr9nsE4CybXBxxutFCfekv4NedJ5WW0zUdrXdM6SWvN4f9kdn7FaECjAdWfz5I4nAz4nztwDh/obWqkNSe0ASPqnTqpxCbsIxLB6dxUnw43v8qBgWVUbIldhos/xtsVQyGRKHNOvGTg+7rCbhhgsy3vpiiCaTBdMtfBEjWrKR9SsHTlS7ftisJXCIBJMbhmc0mjnZ834m9qHXYe1+IoyL3d9dourDTerhBAe3DRLavcUynV6yrMIZor6FWgGrvxf/ZlKPYaFllL7WrAKMGiZLNhwoMvTYmdhXAfZjx2vab+pTvXzDlELKf3kxJcGuasWxV8BdN2x3uzMYvmf+Fp+nfTVk0z9ecEDTwK1wyghGudc4zAo61mHII+GdNMADDDnrg4HLB+9NHPKjNKCmETKymFdQnaoraQ7sj+sSYyWncPZVaYCCA6tMJxEOnu2AnK0G9CG4mF7xmR3LFoVPnHuF4maroPolMInSsCbSNU6IehWujHKGmyVyO09rcEbRaYo0cI9l4X8OBEXbLFeUp7PNnOocU1sjK6zAFxXR9DUOQyKi722vhdporoFQ== odittus"
          - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCv17/cfbIKB8JBeDY/SoWz55tYu7e64BarYpj3UeYrbG/UjbyWh3EnsLyG9cL/Sg4C9by2rsyW2ppJSDCO7R3u+b46RufDVebznHqq1KV1vLwR+eEDANCDnkZswFNG1CZd9VU0zwLuEw8e/gy//qDO2DU4pALe/4BtnHkrNodY+Y6szMP4zkouag+myK4Hzn/vz+95sZ0w+/WUc726uiak8CI1IEBofTnFZCSSKYLRxY779D1+j+rOqE6IW4IOwojGBj0c6UDRQVAhSreLiOvVltyAASZWUGJjoa8zzeC4wH4mtOR/86mHI/zaovHuA6hzoBfP/gYWw74TO+WXQwqMBPvW1n8l3WIthvny2y53OTmdGG4GGI0UcLxehsxRp/ZiAlrwSGA9R735Qnq/IH6jt5NQ/qIxs5S+Ww5oQq90J/5MGAqSv8od1fNqTDRoNDvQRo/wSH0Dt11GNCqk4weqFBpij3h3oykhsRXniuYbsM2n/RRmJ4Q9dL2xdYKfBA0= acalva@TPACALVA-1"

  pre_tasks:

    - name: Create pip config dir
      ansible.builtin.file:
        path: /root/.config/pip/
        state: directory

    - name: Create pip config
      ansible.builtin.copy:
        dest: /root/.config/pip/pip.conf
        content: |
          [global]
          break-system-packages = true

    - name: Remove maybe existing apt lock
      block:

        - name: Reboot template
          ansible.builtin.reboot:
          when: reboot_prio_provisioning == 'Ubuntu'

        - name: Remove maybe existing lock
          ansible.builtin.shell: |
            sudo rm -rf /var/lib/apt/lists/*
            sudo apt-get clean
            sudo apt-get update

        - name: Update apt list
          ansible.builtin.apt:
            update_cache: yes

      when: ansible_distribution == 'Ubuntu'

  roles:
    - role: install-requirements
      when: install_requirements|bool

    - role: create-os-user
      when: create_user|bool

    - role: configure-rke-node
      when: configure_rke_node|bool

  post_tasks:
    - name: Install vault ca certificate to local system from multiple instances
      ansible.builtin.include_role:
        name: install-configure-vault
        tasks_from: install-ca-auth
      vars:
        vault_url: "{{ vault_instance }}"
      loop: "{{ vault_instances }}"
      loop_control:
        loop_var: vault_instance
      when: vault_instances is defined

    - name: Copy network config for enabling dhcp on ubuntu
      ansible.builtin.copy:
        content: "{{ ubuntu_network_config }}"
        dest: "{{ path_ubuntu_network_config }}"
      when: ansible_distribution == 'Debian' or ansible_distribution == 'Ubuntu' and copy_network_config|bool

    - name: Send webhook to msteams
      ansible.builtin.include_role:
        name: create-send-webhook
      vars:
        summary_text: base-os-setup during packer build was executed
        msteams_url: https://365sva.webhook.office.com/webhookb2/2f14a9f8-4736-46dd-9c8c-31547ec37180@0a65cb1e-37d5-41ff-980a-647d9d0e4f0b/IncomingWebhook/37a805a0a2624dc2ac1aedd7dec6ad49/dc3a27ed-396c-40b7-a9b2-f1a2b6b44efe
        card_title: base-os-setup was executed
        act_image: "{{ logo_pic }}"
        act_title: "{{ quotes | random }}"
        act_text: "{{ quotes | random }}"
        os_facts: |
          base-os-setup during packer build was executed on "{{ ansible_fqdn }}"
        ms_teams_notification_type: "simple"
      tags: notify
      ignore_errors: true
      when: send_to_msteams|bool
```

```yaml
#requirements.yaml
---
collections:
  - name: community.crypto
    version: 2.16.2
  - name: community.general
    version: 8.1.0
  - name: ansible.posix
    version: 1.5.2
  - name: kubernetes.core
    version: 3.0.0
  - name: community.vmware
    version: 4.0.1
  - name: community.hashi_vault
    version: 6.0.0

roles:
  - src: https://github.com/stuttgart-things/deploy-configure-rke.git
    scm: git
  - src: https://github.com/stuttgart-things/download-install-binary.git
    scm: git
  - src: https://github.com/stuttgart-things/install-configure-powerdns.git
    scm: git
  - src: https://github.com/stuttgart-things/configure-rke-node.git
    scm: git
  - src: https://github.com/stuttgart-things/install-requirements.git
    scm: git
  - src: https://github.com/stuttgart-things/create-send-webhook.git
    scm: git
  - src: https://github.com/stuttgart-things/create-os-user.git
    scm: git
  - src: https://github.com/stuttgart-things/install-configure-vault.git
    scm: git
  - src: https://github.com/stuttgart-things/install-configure-nfs.git
    scm: git
  - src: https://github.com/stuttgart-things/install-configure-docker.git
    scm: git
  - src: https://github.com/stuttgart-things/manage-filesystem.git
    scm: git
```

</details>


## SNIPPETS PROXMOX

<details><summary><b>UBUNTU23</b></summary>

```yaml
packer {
  required_version = ">= 1.9.4"
  required_plugins {
    proxmox = {
      version = ">= 1.1.5"
      source  = "github.com/hashicorp/proxmox"
    }
  }
}

locals {
  packerstarttime = formatdate("YYYYMMDD", timestamp())
  vmdate = formatdate("YYMM", timestamp())
}

variable "password" {
  type = string
}

variable "username" {
  type = string
}

source "proxmox-iso" "autogenerated_1" {
  boot                    = "order=virtio0;ide2;net0"
  boot_command            = ["<esc><esc><esc><esc>e<wait>", "linux /casper/vmlinuz autoinstall ds=nocloud quiet ---<enter><wait>", "initrd /casper/initrd<enter><wait>", "boot<enter>", "<enter><f10><wait>"]
  boot_wait               = "3s"
  cloud_init              = "false"
  cloud_init_storage_pool = "v3700"
  cores                   = 8
  cpu_type                = "host"
  disks {
    disk_size         = "15G"
    format            = "raw"
    storage_pool      = "v3700"
    type              = "virtio"
  }

  additional_iso_files {
    cd_files = ["./meta-data", "./user-data"]
    cd_label = "cidata"
    unmount = true
    iso_storage_pool = "local"
  }

  insecure_skip_tls_verify = true
  iso_checksum             = "c7cda48494a6d7d9665964388a3fc9c824b3bef0c9ea3818a1be982bc80d346b"
  iso_storage_pool         = "datastore"
  iso_url                  = "https://releases.ubuntu.com/lunar/ubuntu-23.04-live-server-amd64.iso"
  memory                   = 8192

  network_adapters {
    bridge = "vmbr101"
    model  = "virtio"
  }

  node                 = "<PVE-NODE>"
  os                   = "l26"
  password             = var.password
  pool                 = "packer"
  proxmox_url          = "<PVE-API-URL>"
  ssh_password         = "ubuntu"
  ssh_timeout          = "20m"
  ssh_username         = "ubuntu"
  template_description = "Packer VM Template\n---\nSpecs  \nOS: ubuntu23  \nBuild Date: ${local.packerstarttime}\n---\nProvisioning \nUser: packer  \nPassword: Pac7er\n---\nMaintainer  \nPatrick Hermann patrick.hermann@sva.de  \nChristian Mueller christian.mueller@sva.de  \nMartin Wolf martin.wolf@sva.de\n---"
  template_name        = "ubuntu23-eva"
  unmount_iso          = true
  username             = var.username
}

build {
  sources = ["source.proxmox-iso.autogenerated_1"]

  provisioner "shell" {
    inline = ["sudo rm -rf /var/cache/apt/*.bin; sudo apt-get -y update; sudo apt-get -y upgrade; sudo apt-get -y install python3 cloud-init; sudo apt-get autoremove --purge -y && sudo apt-get autoclean -y && sudo apt-get clean -y; sudo rm -rf /var/lib/cloud/seed/nocloud.net; echo 'datasource_list: [ NoCloud, ConfigDrive ]' | sudo tee -a /etc/cloud/cloud.cfg.d/99_pve.cfg > /dev/null; sudo truncate -s 0 /etc/machine-id && echo 'machine-id was reset successfully'; sudo systemctl stop systemd-resolved; sudo sed -i 's/#DNSStubListener=yes/DNSStubListener=no/g' /etc/systemd/resolved.conf; sudo rm /etc/resolv.conf; sudo ln -sf /run/systemd/resolve/resolv.conf /etc/resolv.conf; sudo systemctl start systemd-resolved"]
  }

}
```

</details>

<details><summary><b>USER-DATA</b></summary>

```yaml
#cloud-config
autoinstall:
  version: 1
  locale: en_US.UTF-8
  keyboard:
    layout: de
    toggle: null
    variant: ''
  apt:
    disable_components: []
    geoip: true
    preserve_sources_list: false
    primary:
    - arches:
      - amd64
      - i386
      uri: http://de.archive.ubuntu.com/ubuntu
    - arches:
      - default
      uri: http://ports.ubuntu.com/ubuntu-ports
  drivers:
    install: false
  kernel:
    package: linux-generic
  storage:
    config:
      -
        id: disk-sda
        type: disk
        grub_device: true
        name: ""
        #path: /dev/sda
        match:
          size: largest
        preserve: false
        ptable: gpt
        wipe: superblock
      -
        id: partition-0
        type: partition
        device: disk-sda
        flag: bios_grub
        number: 1
        preserve: false
        size: 1048576
      -
        id: partition-1
        type: partition
        device: disk-sda
        flag: ""
        number: 2
        preserve: false
        size: 536870912
        wipe: superblock
      -
        id: partition-2
        type: partition
        device: disk-sda
        number: 3
        preserve: false
        flag: ""
        size: -1
        wipe: superblock
      -
        id: lvm_volgroup-0
        type: lvm_volgroup
        devices:
          - partition-2
        name: vg0
        preserve: false
      -
        id: lvm_partition-0
        type: lvm_partition
        name: swap
        preserve: false
        size: 2147483648
        volgroup: lvm_volgroup-0
      -
        id: lvm_partition-1
        type: lvm_partition
        name: var
        preserve: false
        size: 2147483648
        volgroup: lvm_volgroup-0
      -
        id: lvm_partition-2
        type: lvm_partition
        name: home
        preserve: false
        size: 2147483648
        volgroup: lvm_volgroup-0
      -
        id: lvm_partition-3
        type: lvm_partition
        name: root
        preserve: false
        size: -1
        volgroup: lvm_volgroup-0
      -
        id: format-0
        type: format
        fstype: ext4
        preserve: false
        volume: partition-1
      -
        id: format-1
        type: format
        fstype: swap
        preserve: false
        volume: lvm_partition-0
      -
        id: format-2
        type: format
        fstype: xfs
        preserve: false
        volume: lvm_partition-1
      -
        id: format-3
        type: format
        fstype: xfs
        preserve: false
        volume: lvm_partition-2
      -
        id: format-4
        type: format
        fstype: xfs
        preserve: false
        volume: lvm_partition-3
      -
        id: mount-0
        type: mount
        device: format-0
        path: /boot
      -
        id: mount-1
        type: mount
        device: format-4
        path: /
      -
        id: mount-2
        type: mount
        device: format-2
        path: /var
      -
        id: mount-3
        type: mount
        device: format-3
        path: /home
  identity:
    hostname: localhost
    username: ubuntu
    password: $6$rounds=656000$r6635QXd9WQ08Tgk$wDjmJsQa4GcTsh/XZG47f7mzVUeYOd1QietsPwbDFh9E.8wjogt8c5DIzLU1q6s.htUfmlslKpD9bznyQD0cb1
  ssh:
    install-server: yes
  packages:
    - qemu-guest-agent
    - open-vm-tools
    - network-manager
  user-data:
    disable_root: false
  late-commands:
    - sed -i 's/^#*\(send dhcp-client-identifier\).*$/\1 = hardware;/' /target/etc/dhcp/dhclient.conf
    - 'sed -i "s/dhcp4: true/&\n      dhcp-identifier: mac/" /target/etc/netplan/00-installer-config.yaml'
    - 'sed -i "s/version: 2/&\n  renderer: NetworkManager/" /target/etc/netplan/00-installer-config.yaml'
    - echo 'ubuntu ALL=(ALL) NOPASSWD:ALL' > /target/etc/sudoers.d/ubuntu
    - systemctl disable systemd-networkd.service --now
```

</details>


