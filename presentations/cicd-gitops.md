# CI/CD WORKSHOP

![why](https://media.makeameme.org/created/why-cicd.jpg)

<!-- .slide: data-transition="zoom" -->
---
# /AGENDA
--
#/AGENDA
* CI <!-- .element: class="fragment fade-up" -->
* CD <!-- .element: class="fragment fade-up" -->
* GITOPS <!-- .element: class="fragment fade-up" -->
--
### /Introduction

<span style="color:orange">#DevOps #CICD #Automation #Cloud #IAC</span>
<span style="color:orange">#Kubernetes #Containerization</span> <br><br>

Patrick Hermann
System-Engineer SVA Stuttgart
patrick.hermann@sva.de
---
# /CI-CD
--
## /CI-CD PIPELINE
![cicdcd](https://miro.medium.com/v2/resize:fit:786/format:webp/0*OC11hb1WJ-th-154.png)
--
## /CI-CD-CD
[<img src="https://www.redhat.com/rhdc/managed-files/styles/wysiwyg_full_width/private/ci-cd-flow-desktop.png.webp?itok=mDEvsSsp" width="1000"/>](https://www.sva.de/index.html)
--
## /EXAMPLE
[<img src="https://docs.gitlab.com/ee/ci/quick_start/img/pipeline_graph_v13_6.png" width="1000"/>](https://www.sva.de/index.html)
--
## /EXAMPLE
```
stages:
  - build

build:
  stage: build
  image: python:3.19
  script:
    - pip install -r requirements.txt
    - python manage.py makemigrations
    - python manage.py migrate
```
---
# /CI
--
## /CI
![cicdcd](https://miro.medium.com/v2/resize:fit:786/format:webp/0*IC_N9P4Eu1NO1UkE.png)
--

## /Source Control
![source](https://codefresh.io/wp-content/uploads/2023/07/everything-in-git.png)
--
## /Source Control
![source](https://codefresh.io/wp-content/uploads/2023/07/not-everything-in-git.png)
--
## /BRANCHING
![source](https://codefresh.io/wp-content/uploads/2023/07/use-short-branches.png)
--
## /BUILD
[<img src="https://codefresh.io/wp-content/uploads/2023/07/single-build-step.png" width="800"/>](https://www.sva.de/index.html)
--
## /BUILD
[<img src="https://codefresh.io/wp-content/uploads/2023/07/many-build-steps.png" width="650"/>](https://www.sva.de/index.html)
--
## /LOCAL VS PIPELINE
[<img src="https://i.redd.it/134ir143zl8a1.jpg" width="650"/>](https://www.sva.de/index.html)
--
## /TASKFILE
![staging](https://tsh.io/wp-content/uploads/2021/04/taskfile-preference-meme.png)
--
## /TASKFILE
```
tasks:
  build:
    cmds:
      - go build -v -i main.go
```
--
## /DRY
[<img src="https://preview.redd.it/r2e86rrndns41.jpg?width=1080&crop=smart&auto=webp&s=4fe4832eaa7d75762850ec174b7e9f99bc358bc9" width="650"/>](https://www.sva.de/index.html)
--
## /STAGING
![staging](https://codefresh.io/wp-content/uploads/2023/07/same-artifact-for-all.png)
--
## /STAGING
![staging](https://codefresh.io/wp-content/uploads/2023/07/same-artifact-for-all.png)
---
# /CD
--
## /CONTAINERIZATION
[<img src="https://miro.medium.com/v2/resize:fit:786/format:webp/0*hYDV_AEZOTZBRVrr.png") width="400"/>](https://www.sva.de/index.html)
--
## /CONTAINERIZATION
[<img src="https://www.atatus.com/images/content/containers.png") width="550"/>](https://www.sva.de/index.html)
--
## /Kubernetes and CI/CD
* Images instead of binaries  <!-- .element: class="fragment fade-up" -->
* Clusters: Many environments  <!-- .element: class="fragment fade-up" -->
* Microservices instead of monoliths (Managing dependencies between all services is going to be challenging)  <!-- .element: class="fragment fade-up" -->
--
## /TEKTON CD
[<img src="https://miro.medium.com/v2/resize:fit:1356/format:webp/1*SqHHsH7dTGNEVd6zTD_-XA.png") width="1200"/>](https://www.sva.de/index.html)
--
## /TEKTON CD
[<img src="https://miro.medium.com/v2/resize:fit:1086/format:webp/1*e5yv4QARvrGgqG7xkkdfSw.png") width="1200"/>](https://www.sva.de/index.html)
--
## /TEKTON TASK
```
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: hello
spec:
  steps:
    - name: echo
      image: alpine
      script: |
        #!/bin/sh
        echo "Hello World"
```
--
## /TEKTON TASKRUN
```
apiVersion: tekton.dev/v1beta1
kind: TaskRun
metadata:
  name: hello-task-run
spec:
  taskRef:
    name: hello
```
---
# /GITOPS
--
## /PUSH
[<img src="https://blog.sparkfabrik.com/hs-fs/hubfs/Blog/cicd-push-based-deployment.png?width=2560&name=cicd-push-based-deployment.png") width="800"/>](https://www.sva.de/index.html)
--
## /PULL
[<img src="https://blog.sparkfabrik.com/hs-fs/hubfs/Blog/CI-CD-GitOps-Push-Based-Deployments.png?width=2560&name=CI-CD-GitOps-Push-Based-Deployments.png") width="800"/>](https://www.sva.de/index.html)
--
## /GitOps PullRequest
* Changes to application configuration <!-- .element: class="fragment fade-up" -->
* Changes to container images <!-- .element: class="fragment fade-up" -->
* Changes to Kubernetes cluster configuration <!-- .element: class="fragment fade-up" -->
* Fixes to errors in an environment <!-- .element: class="fragment fade-up" -->
* Defining new infrastructure via declarative configuration <!-- .element: class="fragment fade-up" -->
* Updating an environment to new requirements <!-- .element: class="fragment fade-up" -->
--
## /GITOPS (EXAMPLE) FLOW
![staging](https://www.inovex.de/wp-content/uploads/2019/07/argocd-workflow.png)
--
## /DevOps vs GitOps
* DevOps is a pipeline process (focuses on the operational aspects of software development) <!-- .element: class="fragment fade-up" -->
* GitOps is a development mechanism (focuses on automating and tracking environment changes in a declarative manner) <!-- .element: class="fragment fade-up" -->
--
## /imperative and declarative
* scripting of deployment operations (imperative) <!-- .element: class="fragment fade-up" -->
* containerized apps (declarative) <!-- .element: class="fragment fade-up" -->
* GitOps only allows declarative configuration <!-- .element: class="fragment fade-up" -->.
--
## /ARGOCD vs. FLUX
[<img src="https://i.imgflip.com/6nklq1.jpg" width="400"/>](https://www.sva.de/index.html)
--
## /ARGOCD vs. FLUX
[<img src="https://miro.medium.com/v2/resize:fit:1400/format:webp/0*0RwREBh9PBZDvy9a.png" width="700"/>](https://www.sva.de/index.html)
--
## /FLUX
[<img src="https://earthly.dev/blog/assets/images/k8s-GitOps-with-FluxCD/bwYwEEQ.jpeg" width="700"/>](https://www.sva.de/index.html)
--
## /FLUX BOOSTRAP
```
flux bootstrap github
--owner=$GITHUB_USER
--repository=fluxcd-demo
--branch=main
--path=./clusters/my-cluster
--personal
```
--
## /FLUX Kustomization
```
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: cert-manager
  namespace: flux-system
spec:
  sourceRef:
    kind: GitRepository
    name: stuttgart-things-github
  path: ./infra/cert-manager
  postBuild:
    substituteFrom:
      - kind: Secret
        name: vault-flux-secrets
```
--
## /ARGO-CD
![staging](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*SHF6VyFUkqBiStSNgJ6NHQ.gif)
--
## /ARGO-CD Application
```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: guestbook
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/argoproj/argocd-example-apps.git
    targetRevision: HEAD
    path: guestbook
  destination:
    server: https://kubernetes.default.svc
    namespace: guestbook
```
