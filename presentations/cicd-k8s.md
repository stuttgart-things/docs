# KUBERNETES CI/CD WORKSHOP

### K8S CI/CD WORKSHOP

<!-- .slide: data-transition="zoom" -->
---
# /AGENDA
--
#/SLOT1
* INTRO
* GIT BASICS
* TRUNK-BASED DEVOLPMENT
* EXECRISE #1: GITHUB ENTERPRISE
--
#/SLOT2
* CI/CD
* GITHUB ACTIONS
* EXECRISE #2: GITHUB ACTIONS
--
#/SLOT3
* TEKTON
* EXECRISE #3: TEKTON
* QUIZ
* SUMMARY
---
### /Introduction

<span style="color:orange">#DevOps #CICD #Automation #Cloud #IAC</span>
<span style="color:orange">#Kubernetes #Containerization</span> <br><br>

Patrick Hermann
System-Engineer SVA Stuttgart
patrick.hermann@sva.de
--
### /Introduction
* short introduction <!-- .element: class="fragment fade-up" -->
* container technology / kubernetes experiences/knowledge <!-- .element: class="fragment fade-up" -->
* workshop expectations <!-- .element: class="fragment fade-up" -->
--
## /TRUNK-BASED DEVOLPMENT
[<img src="https://statusneo.com/wp-content/uploads/2022/12/Beginners%20Guide%20to%20Trunk-Based%20Development.png" width="600"/>](www.google.com)
* Trunk-based development (TBD) is a source control workflow model that enables continuous integration <!-- .element: class="fragment fade-up" -->
* The primary purpose of trunk-based development is to avoid the creation of long-lived branches by merging partial changes to the entire feature <!-- .element: class="fragment fade-up" -->
--
## /TRUNK-BASED DEVOLPMENT
* Developers can achieve this by committing straight to the main branch or by using short-lived branches with an efficient code review process <!-- .element: class="fragment fade-up" -->
* Branches, by definition, should only live a few days <!-- .element: class="fragment fade-up" -->
--
## /TRUNK-BASED DEVOLPMENT
* trunk-based development, where each developer divides their own work into small batches and merges that work into trunk at least once (and potentially several times) a day <!-- .element: class="fragment fade-up" -->
* The key difference between these approaches is scope <!-- .element: class="fragment fade-up" -->
* Feature branches typically involve multiple developers and take days or even weeks of work <!-- .element: class="fragment fade-up" -->
--
## /TRUNK-BASED DEVOLPMENT
* In contrast, branches in trunk-based development typically last no more than a few hours, with many developers merging their individual changes into trunk frequently <!-- .element: class="fragment fade-up" -->
---
# /CICD
--
## /OVERVIEW
* frequently deliver apps to customers by introducing automation into the stages of app development <!-- .element: class="fragment fade-up" -->
* The main concepts: continuous integration, continuous delivery, and continuous deployment <!-- .element: class="fragment fade-up" -->
--
## /OVERVIEW
* ongoing automation and continuous monitoring throughout the lifecycle of apps -> from integration and testing phases to delivery and deployment  <!-- .element: class="fragment fade-up" -->
* often referred to as a "CI/CD pipeline" <!-- .element: class="fragment fade-up" -->
* supported by development and operations teams working together in an agile way  <!-- .element: class="fragment fade-up" -->
--
## /DIFFERENCE BETWEEN CI AND CD
* "CI" in CI/CD always refers to continuous integration <!-- .element: class="fragment fade-up" -->
* which is an automation process for developers <!-- .element: class="fragment fade-up" -->
* Successful CI means new code changes to an app are regularly built, tested, and merged to a shared repository <!-- .element: class="fragment fade-up" -->
* a solution to the problem of having too many branches of an app in development at once (that might conflict with each other) <!-- .element: class="fragment fade-up" -->
--
## /DIFFERENCE BETWEEN CI AND CD
* "CD" in CI/CD refers to continuous delivery and/or continuous deployment <!-- .element: class="fragment fade-up" -->
* which are related concepts that sometimes get used interchangeably <!-- .element: class="fragment fade-up" -->
* Both are about automating further stages of the pipeline <!-- .element: class="fragment fade-up" -->
* sometimes used separately to illustrate just how much automation is happening <!-- .element: class="fragment fade-up" -->
--
## /CONTINUOUS DELIVERY
usually means a developer’s changes to an application are automatically bug tested and uploaded to a repository (like GitHub or a container registry), where they can then be deployed to a live production environment by the operations team. It’s an answer to the problem of poor visibility and communication between dev and business teams. To that end, the purpose of continuous delivery is to ensure that it takes minimal effort to deploy new code.
--
## /CONTINUOUS DEPLOYMENT
Continuous deployment (the other possible "CD") can refer to automatically releasing a developer’s changes from the repository to production, where it is usable by customers. It addresses the problem of overloading operations teams with manual processes that slow down app delivery. It builds on the benefits of continuous delivery by automating the next stage in the pipeline.
--
![Alt text](https://www.redhat.com/rhdc/managed-files/styles/wysiwyg_full_width/private/ci-cd-flow-desktop.png?itok=NNRD1Zj0)
--

---
### /QUIZ
What's a shortcut to staging all the changes you have?
* git add <!-- .element: class="fragment fade-up" -->
* This command is used to stage all the changes you have made in your local repository <!-- .element: class="fragment fade-up" -->
* It allows you to prepare the changes for the next commit <!-- .element: class="fragment fade-up" -->
* By using "GIT add", you are indicating to Git which files or changes you want to include in the next commit <!-- .element: class="fragment fade-up" -->
--
What is k9s?
* provides a terminal UI to interact with your Kubernetes clusters <!-- .element: class="fragment fade-up" -->
--
What is .gitignore
* specify which files or parts of your project should be ignored by Git <!-- .element: class="fragment fade-up" -->
--
What is a helmfile?
* Helmfile is a declarative spec for deploying helm charts <!-- .element: class="fragment fade-up" -->
Keep a directory of chart value files and maintain changes in version control <!-- .element: class="fragment fade-up" -->
Apply CI/CD to configuration changes <!-- .element: class="fragment fade-up" -->
Periodically sync to avoid skew in environments <!-- .element: class="fragment fade-up" -->
--
What is a taskfile?
* Task is a task runner / build tool <!-- .element: class="fragment fade-up" -->
* aims to be simpler and easier to use than, for example, GNU Make <!-- .element: class="fragment fade-up" -->
* Since it's written in Go, Task is just a single binary and has no other dependencies <!-- .element: class="fragment fade-up" -->
--
How to generate a private ssh key?
* ssh-keygen <!-- .element: class="fragment fade-up" -->
--
What is kube-linter?
* KubeLinter analyzes Kubernetes YAML files and Helm charts <!-- .element: class="fragment fade-up" -->
* checks them against a variety of best practices <!-- .element: class="fragment fade-up" -->
* with a focus on production readiness <!-- .element: class="fragment fade-up" -->
--
How do you supply a commit message to a commit?
* To supply a commit message to a commit in GIT, the correct way is to use the command "GIT commit -m "I'm coding!". <!-- .element: class="fragment fade-up" -->
--
What's the git command that downloads your repository from a git server to your computer?
* git clone <!-- .element: class="fragment fade-up" -->
--
What is docker-compose?
--
Which is the correct order to submit your changes from the working directory all the way to the remote repository?
* git add, git commit, git push <!-- .element: class="fragment fade-up" -->
--
What is the opposite of a GIT clone?
* git push <!-- .element: class="fragment fade-up" -->
---
# /SUMMARY
--
### /SUMMARY
* GIT BASICS <!-- .element: class="fragment fade-up" -->
* LINTING / MARKDOWN <!-- .element: class="fragment fade-up" -->
* HELM / KUSTOMIZE <!-- .element: class="fragment fade-up" -->
* KIND <!-- .element: class="fragment fade-up" -->
* TASKFILE <!-- .element: class="fragment fade-up" -->
* PULL REQUEST WORKFLOW <!-- .element: class="fragment fade-up" -->
---
