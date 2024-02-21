# INTRO
--
## PIPELINES AS CODE ON KUBERETES
* FLEXIBILITY: CONTAINER(-IMAGES) <!-- .element: class="fragment fade-up" -->
* SCALABILITY <!-- .element: class="fragment fade-up" -->
* STANDARDIZED <!-- .element: class="fragment fade-up" -->
--
# /PIPELINES AS CODE
* Can be audited for changes just like any other files in the repository <!-- .element: class="fragment fade-up" -->
* Codify build, test + deploy process for code <!-- .element: class="fragment fade-up" -->
* empower teams to create standard processes across multiple repositories <!-- .element: class="fragment fade-up" -->
--
### /TEKTON-PIPELINES
--
* Tekton Pipelines is a Kubernetes extension that installs and runs on your Kubernetes cluster <!-- .element: class="fragment fade-up" -->
* It defines a set of Kubernetes Custom Resources that act as building blocks from which you can assemble CI/CD pipelines <!-- .element: class="fragment fade-up" -->
--
### /TASK
* Defines a series of steps <!-- .element: class="fragment fade-up" -->
* which launch specific build or delivery tools that ingest specific inputs and produce specific outputs.
--
### /Pipeline
* Defines a series of <code>Tasks</code> that accomplish a specific build or delivery goal  <!-- .element: class="fragment fade-up" -->
* Can be triggered by an event or invoked from a <code>PipelineRun  <!-- .element: class="fragment fade-up" -->
--
### /PipelineRun
Instantiates a <code>Pipeline</code> for execution with specific inputs, outputs, and execution parameters  <!-- .element: class="fragment fade-up" -->
--
## TEKTON-TERMINOLOGY
* TASKS e.g. git-clone; kaniko <!-- .element: class="fragment fade-up"
* PIPELINES e.g. package-helm-chart <!-- .element: class="fragment fade-up"
* PIPELINERUNS <!-- .element: class="fragment fade-up"
--
### WHY THIS PROJECT/TALK?
* PIPELINES AS MICROSERVICES <!-- .element: class="fragment fade-up"
* RUN PIPELINERUNS IN STAGES <!-- .element: class="fragment fade-up"
    * PARALLEL (=SAME STAGE) <!-- .element: class="fragment fade-up"
    * RUN OF A SEQUENCE OF STAGES <!-- .element: class="fragment fade-up"
--
### STAGETIME
* BEGININGS IN 2022 <!-- .element: class="fragment fade-up"
* TEAM SÜD-WEST <!-- .element: class="fragment fade-up"
--
### DESIGN PRINCIPLES TEKTON PIPELINES/RUNS
* PIPELINE AS MICROSERVICES <!-- .element: class="fragment fade-up"
* RESOLVER (GIT) <!-- .element: class="fragment fade-up"
* CSI DRIVER (SECRETS) <!-- .element: class="fragment fade-up"
* VOLUMEN CLAIM TEMPLATES (K8S) <!-- .element: class="fragment fade-up"
--
### GOALS STAGETIME
* EVENT-DRIVEN PIPELINERUNS (BY COMMIT/REVISION) <!-- .element: class="fragment fade-up"
* PARALLEL/DEPENDET RUNS <!-- .element: class="fragment fade-up"
* STANDARDIZED BUILDING BLOCKS OF CI/CD <!-- .element: class="fragment fade-up"
* HOUSEKEEPING TEKTON PIPELINERUNS/PODS/PVCS <!-- .element: class="fragment fade-up"
--