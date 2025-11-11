# ANSIBLE SPRECHSTUNDE

[<img src="https://artifacts.homerun-dev.sthings-vsphere.labul.sva.de/images/sprechstunde_4.jpeg" width="500"/>](https://www.sva.de/index.html)

<!-- .slide: data-transition="zoom" -->
--
### /AGENDA
* Begrüßung und Zielsetzung <!-- .element: class="fragment fade-up" -->
* Einführung in Ansible <!-- .element: class="fragment fade-up" -->
    * Was ist Ansible? <!-- .element: class="fragment fade-up" -->
    * Relevanz der Technologie für Kunden und SEs <!-- .element: class="fragment fade-up" -->
    * Beispiele aus der Sprechstunde <!-- .element: class="fragment fade-up" -->
* Einsatz von Ansible beim Kunden <!-- .element: class="fragment fade-up" -->
* Fragen <!-- .element: class="fragment fade-up" -->
---
# /Einführung in Ansible
--
### /Was ist Ansible?
[<img src="https://hvops.com/news/ansible/11/batman-robin-ansible.jpg" width="450"/>](https://www.sva.de/index.html)
* De facto Standard-Configuration-Management-Tool
* On-Premise und Cloud (ready)
--
### /INFRASTRUCTURE AS CODE

```
- name: Create a VM from a template
  hosts: localhost
  tasks:
  - name: Clone the template
    vmware_guest:
      hostname: "{{ vcenter_ip }}"
      username: "{{ vcenter_username }}"
      password: "{{ vcenter_password }}"
      validate_certs: False
      name: testvm_2
      template: template_el7
      datacenter: "{{ datacenter_name }}"
```

* automatisierbar, wiederholbar und versionierbar
--
### /IAC
[<img src="https://www.meme-arsenal.com/memes/cc44149278ca0067e7dd198911ef5553.jpg" width="700"/>](https://www.sva.de/index.html)
--
### /IMPERATIV (e.g. SHELL)

```
#!/bin/bash

# Benutzer erstellen und Home-Verzeichnis festlegen

useradd -m -d /home/user1 -s /bin/bash user1
echo "Passwort1" | passwd --stdin user1

useradd -m -d /home/user2 -s /bin/bash user2
echo "Passwort2" | passwd --stdin user2
```
 * Befehle, die zum Erreichen der gewünschten Konfiguration erforderlich sind
--
### /DEKLARATIV (e.g. ANSIBLE)

```
- hosts: all
  become: true
  tasks:
    - name: Create users with home directories and bash shell
      user:
        name: "{{ item.name }}"
        home: "{{ item.home }}"
        shell: /bin/bash
        state: present
        create_home: yes
      loop:
        - { name: "user1", home: "/home/user1" }
        - { name: "user2", home: "/home/user2" }
        - { name: "user3", home: "/home/user3" }
```
 * Der gewünschte Zustand des Systems wird festgelegt
--
## /ANSIBLE SPRECHSTUNDE

[<img src="https://raw.githubusercontent.com/stuttgart-things/docs/main/hugo/sthings-ansible.png" width="300"/>](https://www.sva.de/index.html)

* Jeden zweiten Donnerstag des Monats
* 14:00 bis 16:00 / Raum: ST M3 -01
--
[<img src="https://artifacts.homerun-dev.sthings-vsphere.labul.sva.de/images/sprechstunde_3.jpeg" width="800"/>](https://www.sva.de/index.html)
---
### /ANSIBLE ARCHITEKTUR

[<img src="https://artifacts.homerun-dev.sthings-vsphere.labul.sva.de/images/architecture.png" width="900"/>](https://www.sva.de/index.html)
--
### /ANSIBLE CLI
[<img src="https://miro.medium.com/v2/resize:fit:1400/1*BJTeJ0HQsV08ucvG3Vuj8w.png" width="900"/>](https://www.sva.de/index.html)
* Python + SSH + ANSIBLE = 🚀
--
### /ANSIBLE INVENTORY

```
initial_master_node:
  hosts:
    rke2-test-molecule.labul.sva.de
additional_master_nodes:
  hosts:
    rke2-test-molecule-2.labul.sva.de:
    rke2-test-molecule-3.labul.sva.de:
```

* Deklaration von Zielen (Hosts) welche über SSH erreicht werden
--
### /ANSIBLE PLAYBOOK

```
- name: Install a package using the package module
  hosts: all
  become: true
  tasks:
    - name: Ensure nginx is installed
      package:
        name: nginx
        state: present
  roles:
    - deploy-rke-loadbalancer
```
* Deklaration:
  * welche tasks or roles
  * auf welchen hosts ausgeführt werden sollen
---
# /ANSIBLE (CLI DEMO)
---
# /Einsatz beim Kunden
--
### /USE CASES
[<img src="https://media.licdn.com/dms/image/v2/C4E12AQGylXwK8s3m2w/article-inline_image-shrink_400_744/article-inline_image-shrink_400_744/0/1606757391660?e=1733356800&v=beta&t=P_-D0mPQO_VN-PQ--CheaaENbJBwBsqhKOUYu3aTsdo" width="700"/>](https://www.sva.de/index.html)
* Viele Einsatz-Möglichkeiten
--
### /Provisioning
[<img src="https://www.visualstudiogeeks.com/images/screenshots/tarun/post08_DevOpsFunnyImage.jpg" width="500"/>](https://www.sva.de/index.html)
* Wiederherstellbarkeit + Vermeidung von Configuration-Drifts
--
### /Automatisierung Wiederkehrender Aufgaben
[<img src="https://preview.redd.it/was-it-even-worth-v0-n0dugfgrz5l81.gif?format=png8&s=526d607a75f20065a354d3702369244375715614" width="400"/>](https://www.sva.de/index.html)
* User|updates|backups|config ..
---
### /ANSIBLE AUTOMATION PLATFORM
[<img src="https://www.redhat.com/rhdc/managed-files/ansible-hero-img-ohs1.png" width="600"/>](https://www.sva.de/index.html)
* Ansible Ausführung zentralisieren und kontrollieren <!-- .element: class="fragment fade-up" -->
---
# /AWX DEMO
---
## /ANSIBLE SPRECHSTUNDE

* Jeden zweiten Donnerstag des Monats
* 14:00 bis 16:00 Uhr
* Raum: ST M3 -01
* Wiki: https://wiki.sva.de/pages/viewpage.action?pageId=453482787

[<img src="https://raw.githubusercontent.com/stuttgart-things/docs/main/hugo/sthings-ansible.png" width="200"/>](https://www.sva.de/index.html)
---
# /WIKI
---
# /Fragen?
[<img src="https://github.com/stuttgart-things/docs/raw/main/hugo/sthings-coffee.png" width="500"/>](https://www.sva.de/index.html)
