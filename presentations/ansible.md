# ANSIBLE SPRECHSTUNDE

[<img src="https://artifacts.homerun-dev.sthings-vsphere.labul.sva.de/images/sprechstunde_4.jpeg" width="500"/>](https://www.sva.de/index.html)

<!-- .slide: data-transition="zoom" -->
--
[<img src="https://hvops.com/news/ansible/11/batman-robin-ansible.jpg" width="650"/>](https://www.sva.de/index.html)
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
* De facto Standard-Configuration-Management-Tool
* Cloud- und On-Premise
--
### /INFRASTRUCTURE AS CODE
[<img src="https://www.meme-arsenal.com/memes/cc44149278ca0067e7dd198911ef5553.jpg" width="700"/>](https://www.sva.de/index.html)
--

### /INFRASTRUCTURE AS CODE
* virtuelle Maschinen, Datenbanken und andere Ressourcen – mittels Konfigurationsdateien (=Code) definieren, bereitstellen und verwalten <!-- .element: class="fragment fade-up" -->
* automatisierbar, wiederholbar und versionierbar <!-- .element: class="fragment fade-up" -->
--
### /IMPERATIV

```
#!/bin/bash

# Benutzer erstellen und Home-Verzeichnis festlegen

useradd -m -d /home/user1 -s /bin/bash user1
echo "Passwort1" | passwd --stdin user1

useradd -m -d /home/user2 -s /bin/bash user2
echo "Passwort2" | passwd --stdin user2
```
 * Befehle, die zum Erreichen der gewünschten Konfiguration erforderlich sind <!-- .element: class="fragment fade-up" -->
--
### /DEKLARATIV 

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
 * Der gewünschte Zustand des Systems wird festgelegt <!-- .element: class="fragment fade-up" -->
--
## /ANSIBLE SPRECHSTUNDE

* Jeden zweiten Donnerstag des Monats
* 14:00 bis 16:00
* Raum: ST M3 -01
* Wiki: https://wiki.sva.de/pages/viewpage.action?pageId=453482787 

[<img src="https://raw.githubusercontent.com/stuttgart-things/docs/main/hugo/sthings-ansible.png" width="200"/>](https://www.sva.de/index.html)
--
[<img src="https://artifacts.homerun-dev.sthings-vsphere.labul.sva.de/images/sprechstunde_2.jpeg" width="600"/>](https://www.sva.de/index.html)
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

* Deklaration von Zielen (Hosts) welche über SSH erreict werden 
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
  * auf welchen hostst ausgeführt werden sollen
---
# /ANSIBLE (CLI DEMO)
---
# /Einsatz beim Kunden
--
### /USE CASES
[<img src="https://media.licdn.com/dms/image/v2/C4E12AQGylXwK8s3m2w/article-inline_image-shrink_400_744/article-inline_image-shrink_400_744/0/1606757391660?e=1733356800&v=beta&t=P_-D0mPQO_VN-PQ--CheaaENbJBwBsqhKOUYu3aTsdo" width="700"/>](https://www.sva.de/index.html)
--
### /Provisioning
[<img src="https://www.visualstudiogeeks.com/images/screenshots/tarun/post08_DevOpsFunnyImage.jpg" width="500"/>](https://www.sva.de/index.html)
* Wiederherstellbarkeit + Vermeidung von Configuration-Drifts
--
### /Cloud Computing
* Ansible erleichtert die Bereitstellung von Instanzen bei allen Cloud-Anbietern <!-- .element: class="fragment fade-up" -->
--
### /Security und Compliance
* In Ansible können Sicherheitsrichtlinien definiert werden, die die Sicherheitsrichtlinien für alle Maschinen im Netzwerk automatisieren <!-- .element: class="fragment fade-up" -->
---
### /ANSIBLE AUTOMATION PLATFORM
[<img src="https://www.redhat.com/rhdc/managed-files/ansible-hero-img-ohs1.png" width="700"/>](https://www.sva.de/index.html)
* gesamte IT-Infrastruktur mit einem visuellen Dashboard in Echtzeit zentralisieren und kontrollieren <!-- .element: class="fragment fade-up" -->
* Funktionen wie rollenbasierte Zugriffskontrolle (RBAC), Auftragsplanung und Bestandsverfolgung über mehrere Cloud-Anbieter hinweg können leicht organisiert und automatisiert werden <!-- .element: class="fragment fade-up" -->
---
# /AWX DEMO
---
## /ANSIBLE SPRECHSTUNDE

* Jeden zweiten Donnerstag des Monats
* 14:00 bis 16:00 Uhr
* Raum: ST M3 -01
* Wiki: https://wiki.sva.de/pages/viewpage.action?pageId=453482787 

[<img src="https://raw.githubusercontent.com/stuttgart-things/docs/main/hugo/sthings-ansible.png" width="200"/>](https://www.sva.de/index.html)
--
# /Fragen?


[<img src="https://miro.medium.com/v2/resize:fit:826/0*oZ6czP8_xU-amLfL.jpg" width="400"/>](https://www.sva.de/index.html)
[<img src="https://artifacts.homerun-dev.sthings-vsphere.labul.sva.de/images/sprechstunde_1.png" width="400"/>](https://www.sva.de/index.html)

--


--



[<img src="https://artifacts.homerun-dev.sthings-vsphere.labul.sva.de/images/sprechstunde_4.jpeg" width="600"/>](https://www.sva.de/index.html)

---

[<img src="https://github.com/stuttgart-things/docs/raw/main/hugo/sthings-coffee.png" width="500"/>](https://www.sva.de/index.html)


