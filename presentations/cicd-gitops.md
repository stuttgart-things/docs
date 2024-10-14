# CI/CD WORKSHOP

### CI/CD WORKSHOP

<!-- .slide: data-transition="zoom" -->
---
# /AGENDA
--
#/SLOT1
* INTRO <!-- .element: class="fragment fade-up" -->
* GIT BASICS <!-- .element: class="fragment fade-up" -->
* TRUNK-BASED DEVOLPMENT <!-- .element: class="fragment fade-up" -->
* ARGOCD APPSETS <!-- .element: class="fragment fade-up" -->
--
### /Introduction

<span style="color:orange">#DevOps #CICD #Automation #Cloud #IAC</span>
<span style="color:orange">#Kubernetes #Containerization</span> <br><br>

Patrick Hermann
System-Engineer SVA Stuttgart
patrick.hermann@sva.de
---
# /CICD
--
## /CI-CD-CD
![cicdcd](https://www.redhat.com/rhdc/managed-files/styles/wysiwyg_full_width/private/ci-cd-flow-desktop.png.webp?itok=mDEvsSsp)
--
## /Source Control
![source](https://codefresh.io/wp-content/uploads/2023/07/everything-in-git.png)
--
## /Source Control
![source](https://codefresh.io/wp-content/uploads/2023/07/not-everything-in-git.png)
--
## /STAGING
![staging](https://codefresh.io/wp-content/uploads/2023/07/same-artifact-for-all.png)
--
## /STAGING
![staging](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*0RwREBh9PBZDvy9a.png)
--
## /STAGING
![staging](https://codefresh.io/wp-content/uploads/2023/07/with-caching.png)
--
## /ARGO-CD
![staging](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*SHF6VyFUkqBiStSNgJ6NHQ.gif)
--
## /DevOps vs GitOps
* GitOps is a development mechanism, which mainly focuses on automating and tracking environment changes in a declarative manner.
* DevOps is a pipeline process, which mainly focuses on the operational aspects of software development.
--
## Imperative and declarative configurations
* DevOps can be both imperative and declarative. 
    * scripting of deployment operations(imperative)  * containerized apps (declarative)
* GitOps only allows declarative configuration.
--
## /GitOps PullRequest
* Changes to application configuration
* Changes to container images
* Changes to Kubernetes cluster configuration
* Fixes to errors in an environment
* Defining new infrastructure via declarative configuration
* Updating an environment to new requirements
--

