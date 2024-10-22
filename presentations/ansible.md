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
    * Was ist Ansible? <!-- .element: class="fragment fade-up" -->
    * Neuigkeiten <!-- .element: class="fragment fade-up" --> 
* Fragen <!-- .element: class="fragment fade-up" -->
---
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

### /INFRASTRUCTURE AS CODE

--

### /DEKLARATIV VS. IMPERATIV

### /MODULES


Ansible kann sowohl deklarativ als auch prozedural sein: Viele Module arbeiten deklarativ, andere folgen einem prozeduralen Programmieransatz. Darüber hinaus können Nutzende mit einigen Konstrukten der Ansible-Sprache, wie Bedingungen und Schleifen, eine prozedurale Logik definieren. Dank dieser Flexibilität können Sie sich auf Ihre eigentliche Arbeit konzentrieren, anstatt sich strikt an ein Modell halten zu müssen. 


https://www.redhat.com/de/topics/automation/ansible-vs-terraform



--
### /USE CASES

[<img src="https://media.licdn.com/dms/image/v2/C4E12AQGylXwK8s3m2w/article-inline_image-shrink_400_744/article-inline_image-shrink_400_744/0/1606757391660?e=1733356800&v=beta&t=P_-D0mPQO_VN-PQ--CheaaENbJBwBsqhKOUYu3aTsdo" width="500"/>](https://www.sva.de/index.html)


<span style="color:orange">#DevOps #CICD #Automation #Cloud #IAC</span>
<span style="color:orange">#Kubernetes #Containerization</span> <br><br>


---
# /ANSIBLE
--

---
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
