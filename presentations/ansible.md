# ANSIBLE

[<img src="https://lh4.googleusercontent.com/proxy/T1l-uRgNzFbx8DcZvsfUqpZ_0nqYCtPdVdymyGSCcynHlO69i6POvT-JVpruB6Hm1cdEXZM1r-0Nwg" width="800"/>](https://www.sva.de/index.html)

# sthings coffee?



<!-- .slide: data-transition="zoom" -->
---
/AGENDA
* Begrüßung und Zielsetzung <!-- .element: class="fragment fade-up" -->
* Einführung in Ansible <!-- .element: class="fragment fade-up" -->
    * Was ist Ansible? <!-- .element: class="fragment fade-up" -->
    * Relevanz der Technologie für Kunden und SEs <!-- .element: class="fragment fade-up" --> 
* Einsatz von Ansible beim Kunden <!-- .element: class="fragment fade-up" -->
* Beispiele aus der Sprechstunde <!-- .element: class="fragment fade-up" -->
    * Kunden-Usecases <!-- .element: class="fragment fade-up" -->
    * Code von Kollegen + mögliche Optimierungen <!-- .element: class="fragment fade-up" --> 
    * Neuigkeiten <!-- .element: class="fragment fade-up" --> 
* Fragen <!-- .element: class="fragment fade-up" -->
---
# Einführung in Ansible
--

### /INFRASTRUCTURE AS CODE
bedeutet Idempotenz. Das bedeutet, dass Operationen, die mehr als einmal mit denselben Parametern aufgerufen werden, keine zusätzlichen Auswirkungen haben. Einige Tools, die nach dem IAC-Ansatz entwickelt wurden, sind Ansible, Terraform, AWS Cloud Formation und ARM-Templates. Infrastructure as Code IaC kann auf 2 Arten angegangen werden: deklarativ und imperativ
--

### /DEKLARATIV VS. IMPERATIV

* Deklarativ: Bei deklarativer IaC wird der gewünschte Zustand des Systems festgelegt. Ressourcen und Eigenschaften werden auf die Ressource angewendet, sobald der Benutzer den gewünschten Zustand angibt. Ein Beispiel für ein Tool, das einen deklarativen Ansatz verwendet, ist AWS CloudFormation.
* Imperativ: Imperative IaC spezifiziert spezifische Befehle, die zum Erreichen der gewünschten Konfiguration erforderlich sind. Der Benutzer gibt die gewünschten Befehle an und die Befehle werden ausgeführt, um das System in den gewünschten Zustand zu bringen. Ein Beispiel für ein Tool, das einen imperativen Ansatz für IaC verwendet, ist AWS CLI
--

### /Was ist Ansible?
Ansible ist ein einfaches Konfigurationsmanagement- und IT-Automatisierungsmodul für mehrstufige Bereitstellungen. Es automatisiert sowohl die Cloud- als auch die On-Premise-Bereitstellung und -Konfiguration.
--

### /ANSIBLE ARCHITECTURE

[<img src="https://k21academy.com/wp-content/uploads/2021/06/Ansible_Diagram2-16-1536x692.png"width="800"/>](https://www.sva.de/index.html)
--
### /ANSIBLE ARCHITECTURE
* Module: Module sind skriptartige Programme, die geschrieben werden, um den gewünschten Zustand des Systems zu spezifizieren. 
* Plugins: Plugins sind Codestücke, die die Kernfunktionalität von Ansible erweitern.
* Inventory: Ansible liest Informationen über die Maschinen, die es verwaltet, aus dem Inventory.
* Playbook: Playbooks beschreiben die Aufgaben, die zu erledigen sind, indem sie Konfigurationen deklarieren, um einen verwalteten Knoten in den gewünschten Zustand zu bringen.
--

### /BASICS

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
### /EXAMPLE ANSIBLE PLAYBOOK
```
- hosts: webservers
  vars:
    http_port: 80
    max_clients: 200
    remote_user: root
  tasks:
  - name: ensure apache is at the latest version
    yum: name=httpd state=latest
  - name: write the apache config file
    template: src=/srv/httpd.j2 dest=/etc/httpd.conf
    notify:
    - restart apache
  - name: ensure apache is running (and enable it at boot)
    service: name=httpd state=started enabled=yes
    handlers:
  - name: restart apache
    service: name=httpd state=restarted
```
--

### /MODULES

Ansible kann sowohl deklarativ als auch prozedural sein: Viele Module arbeiten deklarativ, andere folgen einem prozeduralen Programmieransatz. Darüber hinaus können Nutzende mit einigen Konstrukten der Ansible-Sprache, wie Bedingungen und Schleifen, eine prozedurale Logik definieren. Dank dieser Flexibilität können Sie sich auf Ihre eigentliche Arbeit konzentrieren, anstatt sich strikt an ein Modell halten zu müssen. 

https://www.redhat.com/de/topics/automation/ansible-vs-terraform

--
### /USE CASES

[<img src="https://media.licdn.com/dms/image/v2/C4E12AQGylXwK8s3m2w/article-inline_image-shrink_400_744/article-inline_image-shrink_400_744/0/1606757391660?e=1733356800&v=beta&t=P_-D0mPQO_VN-PQ--CheaaENbJBwBsqhKOUYu3aTsdo" width="500"/>](https://www.sva.de/index.html)

<span style="color:orange">#DevOps #CICD #Automation #Cloud #IAC</span>
<span style="color:orange">#Kubernetes #Containerization</span> <br><br>
--

### /USE CASES
* Provisioning: Einrichtung einer neuen Infrastruktur. Ansible ermöglicht das Anwendungsmanagement, die Bereitstellung, die Orchestrierung und das Konfigurationsmanagement.
* Continuous Delivery: Mit dem CI-Tool kann ein Ansible-Playbook ausgeführt werden, das zum Testen und automatischen Bereitstellen der Anwendung für die Produktion verwendet werden kann, wenn die Tests bestanden sind.
* Application Deployment: Ansible bietet eine einfachere Methode zur Bereitstellung von Anwendungen in der gesamten Infrastruktur. Die Bereitstellung von mehrschichtigen Anwendungen kann vereinfacht werden, und die Infrastruktur kann im Laufe der Zeit leicht geändert werden.
* Ansible für Cloud Computing: Ansible erleichtert die Bereitstellung von Instanzen bei allen Cloud-Anbietern. Ansible enthält mehrere Module und ermöglicht die Verwaltung großer Cloud-Infrastrukturen über die Public-Private- und Hybrid-Cloud.
* Ansible für Security und Compliance: In Ansible können Sicherheitsrichtlinien definiert werden, die die Sicherheitsrichtlinien für alle Maschinen im Netzwerk automatisieren.
--
### /ANSIBLE TOWER

Ansible Tower ermöglicht es, die gesamte IT-Infrastruktur mit einem visuellen Dashboard zu zentralisieren und zu kontrollieren. Es zeigt alles, was in der Ansible-Umgebung vor sich geht, in Echtzeit an. Funktionen wie rollenbasierte Zugriffskontrolle (RBAC), Auftragsplanung und Bestandsverfolgung über mehrere Cloud-Anbieter hinweg können leicht organisiert und automatisiert werden.

--
# /AAP-AWX
---
# Beispiele aus der Sprechstunde

[<img src="https://miro.medium.com/v2/resize:fit:826/0*oZ6czP8_xU-amLfL.jpg" width="400"/>](https://www.sva.de/index.html)
---
# Fragen?

[<img src="https://mtyurt.net/img/automate-all-the-things.jpg" width="400"/>](https://www.sva.de/index.html)


--
Patrick Hermann
System-Engineer SVA Stuttgart
patrick.hermann@sva.de
--
