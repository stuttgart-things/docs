# INTRO
--
### /CI-CD TASKS
* Lint: to keep our code clean and maintainable <!-- .element: class="fragment fade-up" -->
* Build: put all of our code together into runnable software bundle <!-- .element: class="fragment fade-up" -->
* Test: to ensure we don't break existing features <!-- .element: class="fragment fade-up" -->
* Package: Put it all together as build artifacts <!-- .element: class="fragment fade-up" -->
--
## PIPELINES AS CODE
* Can be audited for changes just like any other files in the repository <!-- .element: class="fragment fade-up" -->
* Codify build, test + deploy process for code <!-- .element: class="fragment fade-up" -->
* empower teams to create standard processes across multiple repositories <!-- .element: class="fragment fade-up" -->
--
## PIPELINES AS CODE ON K8S
* CUSTOMIZABLE <!-- .element: class="fragment fade-up" -->
* REUSABLE<!-- .element: class="fragment fade-up" -->
* SCALABLE <!-- .element: class="fragment fade-up" -->
* STANDARD <!-- .element: class="fragment fade-up" -->
--
## /TEKTON-PIPELINES
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/tekton-horizontal-color.png" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->

* Tekton Pipelines is a Kubernetes extension <!-- .element: class="fragment fade-up" -->
* Runs on every Kubernetes cluster <!-- .element: class="fragment fade-up" -->
* Defines a set of Custom Resources that act as building blocks <!-- .element: class="fragment fade-up" -->
--
## /TASK
* Defines a series of steps <!-- .element: class="fragment fade-up" -->

```
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: git-clone
spec:
  steps:
    - name: clone-git
      image: gcr.io/git-init:v0.40.2
      script: |
        #!/bin/sh
        echo "Cloning git repository"
        # ..
```
<!-- .element: class="fragment fade-up" -->
--
### /Pipeline
* Series of Tasks that accomplish a specific build goal  <!-- .element: class="fragment fade-up" -->

```
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: clone-build-push
spec:
  params:
  - name: repo-url
    type: string
  workspaces:
  - name: shared-data
  tasks:
  - name: fetch-source
    taskRef:
      name: git-clone
    # ..
```
<!-- .element: class="fragment fade-up" -->
--
## /PipelineRun
Instantiates a Pipeline for execution with specific inputs, outputs, and execution parameters  <!-- .element: class="fragment fade-up" -->

```
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  generateName: clone-build-push-run-
spec:
  pipelineRef:
    name: clone-build-push
  params:
  - name: repo-url
    value: https://github.com/google/docsy-example.git
  workspaces:
  - name: shared-data
  # ..
```
<!-- .element: class="fragment fade-up" -->
--
## /LIST PIPELINERUNS
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/prlist.gif" width="700"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
## /PIPELINERUN LOGS
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/prlogs.gif" width="1000"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
## /WHY THIS PROJECT/TALK?
* PIPELINES AS MICROSERVICES <!-- .element: class="fragment fade-up" -->
* RUN PIPELINERUNS IN STAGES <!-- .element: class="fragment fade-up" -->
    * PARALLEL (=SAME STAGE) <!-- .element: class="fragment fade-up" -->
    * RUN OF A SEQUENCE OF STAGES <!-- .element: class="fragment fade-up" -->
--
## /WHY THIS PROJECT/TALK?
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/stages.png" width="700"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
## /STAGETIME
* BEGININGS IN 2022 <!-- .element: class="fragment fade-up"
* TEAM SÜD-WEST <!-- .element: class="fragment fade-up"
--
## /DESIGN PRINCIPLES TEKTON PIPELINES/RUNS
* PIPELINE AS MICROSERVICES <!-- .element: class="fragment fade-up" -->
* RESOLVER (GIT) <!-- .element: class="fragment fade-up" -->
* CSI DRIVER (SECRETS) <!-- .element: class="fragment fade-up" -->
* VOLUMEN CLAIM TEMPLATES (K8S) <!-- .element: class="fragment fade-up" -->
--
### GOALS STAGETIME
* EVENT-DRIVEN PIPELINERUNS (BY COMMIT/REVISION) <!-- .element: class="fragment fade-up" -->
* PARALLEL/DEPENDET RUNS <!-- .element: class="fragment fade-up" -->
* STANDARDIZED BUILDING BLOCKS OF CI/CD <!-- .element: class="fragment fade-up" -->
* HOUSEKEEPING TEKTON PIPELINERUNS/PODS/PVCS <!-- .element: class="fragment fade-up" -->
--
