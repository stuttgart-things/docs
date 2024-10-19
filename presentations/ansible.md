# ANSIBLE

[<img src="https://lh4.googleusercontent.com/proxy/T1l-uRgNzFbx8DcZvsfUqpZ_0nqYCtPdVdymyGSCcynHlO69i6POvT-JVpruB6Hm1cdEXZM1r-0Nwg" width="800"/>](https://www.sva.de/index.html)

# sthings coffee?



<!-- .slide: data-transition="zoom" -->
---
/AGENDA
* Einführung in Ansible <!-- .element: class="fragment fade-up" -->
    * Was ist Ansible? <!-- .element: class="fragment fade-up" -->
    * Relevanz der Technologie für Kunden und SEs <!-- .element: class="fragment fade-up" --> 
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

Ansible kann sowohl deklarativ als auch prozedural sein: Viele Module arbeiten deklarativ, andere folgen einem prozeduralen Programmieransatz. Darüber hinaus können Nutzende mit einigen Konstrukten der Ansible-Sprache, wie Bedingungen und Schleifen, eine prozedurale Logik definieren. Dank dieser Flexibilität können Sie sich auf Ihre eigentliche Arbeit konzentrieren, anstatt sich strikt an ein Modell halten zu müssen. 


https://www.redhat.com/de/topics/automation/ansible-vs-terraform



--
### /USE CASES

[<img src="https://media.licdn.com/dms/image/v2/C4E12AQGylXwK8s3m2w/article-inline_image-shrink_400_744/article-inline_image-shrink_400_744/0/1606757391660?e=1733356800&v=beta&t=P_-D0mPQO_VN-PQ--CheaaENbJBwBsqhKOUYu3aTsdo" width="900"/>](https://www.sva.de/index.html)




<span style="color:orange">#DevOps #CICD #Automation #Cloud #IAC</span>
<span style="color:orange">#Kubernetes #Containerization</span> <br><br>

Patrick Hermann
System-Engineer SVA Stuttgart
patrick.hermann@sva.de
---
# /ANSIBLE
--

---
# /AAP-AWX
--


