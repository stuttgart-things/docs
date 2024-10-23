# ANSIBLE

[<img src="https://lh4.googleusercontent.com/proxy/T1l-uRgNzFbx8DcZvsfUqpZ_0nqYCtPdVdymyGSCcynHlO69i6POvT-JVpruB6Hm1cdEXZM1r-0Nwg" width="700"/>](https://www.sva.de/index.html)


<!-- .slide: data-transition="zoom" -->
---
/AGENDA
* Begrüßung und Zielsetzung <!-- .element: class="fragment fade-up" -->
* Einführung in Ansible <!-- .element: class="fragment fade-up" -->
    * Was ist Ansible? <!-- .element: class="fragment fade-up" -->
    * Relevanz der Technologie für Kunden und SEs <!-- .element: class="fragment fade-up" --> 
* Einsatz von Ansible beim Kunden <!-- .element: class="fragment fade-up" -->
* Beispiele aus der Sprechstunde <!-- .element: class="fragment fade-up" -->
* Fragen <!-- .element: class="fragment fade-up" -->
---
## /ANSIBLE SPRECHSTUNDE

* Jeden zweiten Donnerstag des Monats
* 14:00 bis 16:00
* Raum: ST M3 -01
* Wiki: https://wiki.sva.de/pages/viewpage.action?pageId=453482787 

[<img src="https://raw.githubusercontent.com/stuttgart-things/docs/main/hugo/sthings-ansible.png" width="200"/>](https://www.sva.de/index.html)
---
# /Einführung in Ansible
--

### /INFRASTRUCTURE AS CODE
[<img src="https://www.meme-arsenal.com/memes/cc44149278ca0067e7dd198911ef5553.jpg" width="700"/>](https://www.sva.de/index.html)
--

### /INFRASTRUCTURE AS CODE
* Infrastruktur eines Systems – Netzwerke, Server, Speicher, Datenbanken und andere Ressourcen – mittels Konfigurationsdateien definieren, bereitstellen und verwalten
* Statt manuell Hardware und Software zu konfigurieren, erfolgt dies durch Code. 
--

### /INFRASTRUCTURE AS CODE

* Bereitstellung von Infrastruktur wird automatisierbar, wiederholbar und versionierbar.
* IaC kann auf 2 Arten angegangen werden: deklarativ und imperativ.
--

### /DEKLARATIV VS. IMPERATIV

* Deklarativ: 
 * Der gewünschte Zustand des Systems wird festgelegt. 
 * Ressourcen und Eigenschaften werden auf die Ressource angewendet, sobald der Benutzer den gewünschten Zustand angibt.
 * Bsp: AWS CloudFormation
--

### /DEKLARATIV VS. IMPERATIV
* Imperativ: 
 * Befehle, die zum Erreichen der gewünschten Konfiguration erforderlich sind. 
 * Der Benutzer gibt die gewünschten Befehle an und die Befehle werden ausgeführt, um das System in den gewünschten Zustand zu bringen.
 * Bsp: AWS CLI
--

### /Was ist Ansible?
* De facto Standard-Configuration-Management-Tool
* Cloud- und On-Premise
--

### /ANSIBLE ARCHITEKTUR

[<img src="https://k21academy.com/wp-content/uploads/2021/06/Ansible_Diagram2-16-1536x692.png" width="900"/>](https://www.sva.de/index.html)
--
### /ANSIBLE MODULE
* Skriptartige Programme, die geschrieben werden, um den gewünschten Zustand des Systems zu spezifizieren. 
--
### /ANSIBLE INVENTORY
* Ansible liest Informationen über die Maschinen, die es verwaltet, aus dem Inventory.
--
### /ANSIBLE PLAYBOOK
* Beschreiben die Aufgaben, die zu erledigen sind, indem sie Konfigurationen deklarieren, um einen verwalteten Knoten in den gewünschten Zustand zu bringen.
--

### /BEISPIEL ANSIBLE PLAYBOOK

```
- name: Update web servers
  hosts: webservers
  remote_user: root

  tasks:
  - name: Ensure apache is at the latest version
    ansible.builtin.yum:
      name: httpd
      state: latest
```

--

### /ANSIBLE AUTOMATION PLATFORM


[<img src="https://www.redhat.com/rhdc/managed-files/ansible-hero-img-ohs1.png" width="700"/>](https://www.sva.de/index.html)
--
### /ANSIBLE AUTOMATION PLATFORM
* gesamte IT-Infrastruktur mit einem visuellen Dashboard in Echtzeit zentralisieren und kontrollieren. 
* Funktionen wie rollenbasierte Zugriffskontrolle (RBAC), Auftragsplanung und Bestandsverfolgung über mehrere Cloud-Anbieter hinweg können leicht organisiert und automatisiert werden.

--

### /USE CASES

[<img src="https://media.licdn.com/dms/image/v2/C4E12AQGylXwK8s3m2w/article-inline_image-shrink_400_744/article-inline_image-shrink_400_744/0/1606757391660?e=1733356800&v=beta&t=P_-D0mPQO_VN-PQ--CheaaENbJBwBsqhKOUYu3aTsdo" width="600"/>](https://www.sva.de/index.html)

<span style="color:orange">#DevOps #CICD #Automation #Cloud #IAC</span>
<span style="color:orange">#Kubernetes #Containerization</span> <br><br>
---
## /Einsatz von Ansible beim Kunden
--

### /Provisioning
* Einrichtung einer neuen Infrastruktur. 
* Anwendungsmanagement, Bereitstellung, Orchestrierung und Konfigurationsmanagement.
--

### /Continuous Delivery
* Mit dem CI-Tool kann ein Ansible-Playbook ausgeführt werden, das zum Testen und automatischen Bereitstellen der Anwendung für die Produktion verwendet werden kann.
--

### /Application Deployment
* Ansible bietet eine einfache Methode zur Bereitstellung von Anwendungen in der gesamten Infrastruktur. 
* Die Bereitstellung von mehrschichtigen Anwendungen kann vereinfacht werden, und die Infrastruktur kann im Laufe der Zeit leicht geändert werden.
--

### /Cloud Computing
* Ansible erleichtert die Bereitstellung von Instanzen bei allen Cloud-Anbietern. 
* Ansible enthält mehrere Module und ermöglicht die Verwaltung großer Cloud-Infrastrukturen über die Public-Private- und Hybrid-Cloud.
--

### /Security und Compliance
* In Ansible können Sicherheitsrichtlinien definiert werden, die die Sicherheitsrichtlinien für alle Maschinen im Netzwerk automatisieren.

---
## /ANSIBLE SPRECHSTUNDE

* Jeden zweiten Donnerstag des Monats
* 14:00 bis 16:00 Uhr
* Raum: ST M3 -01
* Wiki: https://wiki.sva.de/pages/viewpage.action?pageId=453482787 

[<img src="https://raw.githubusercontent.com/stuttgart-things/docs/main/hugo/sthings-ansible.png" width="200"/>](https://www.sva.de/index.html)
--
## /Beispiele aus der Sprechstunde

```
#!/bin/bash

# Benutzer erstellen und Home-Verzeichnis festlegen

useradd -m -d /home/user1 -s /bin/bash user1
echo "Passwort1" | passwd --stdin user1

useradd -m -d /home/user2 -s /bin/bash user2
echo "Passwort2" | passwd --stdin user2
```

--

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

--



[<img src="https://miro.medium.com/v2/resize:fit:826/0*oZ6czP8_xU-amLfL.jpg" width="400"/>](https://www.sva.de/index.html)
--

[<img src="https://artifacts.homerun-dev.sthings-vsphere.labul.sva.de/images/sprechstunde_1.png" width="200"/>](https://www.sva.de/index.html)
--

[<img src="https://artifacts.homerun-dev.sthings-vsphere.labul.sva.de/images/sprechstunde_2.jpeg" width="600"/>](https://www.sva.de/index.html)
--

[<img src="https://artifacts.homerun-dev.sthings-vsphere.labul.sva.de/images/sprechstunde_3.jpeg" width="600"/>](https://www.sva.de/index.html)
--

[<img src="https://artifacts.homerun-dev.sthings-vsphere.labul.sva.de/images/sprechstunde_4.jpeg" width="600"/>](https://www.sva.de/index.html)

---
# /Fragen?

[<img src="https://github.com/stuttgart-things/docs/raw/main/hugo/sthings-coffee.png" width="500"/>](https://www.sva.de/index.html)




--
Patrick Hermann
System-Engineer SVA Stuttgart
patrick.hermann@sva.de
--
