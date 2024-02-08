# MAKING OF stageTime

//ADD STAGE TIME IMAGE

### MAKING OF stageTime

<!-- .slide: data-transition="zoom" -->
---
# /AGENDA
--
#/CHAPTER1: Challenge 
* INTRO <!-- .element: class="fragment fade-up" -->
* PIPELINE AS CODE ON KUBERETES <!-- .element: class="fragment fade-up" -->
* TEKTON <!-- .element: class="fragment fade-up" -->
* CHALLENGES <!-- .element: class="fragment fade-up" -->
--
#/CHAPTER2: Server
* FEATURES <!-- .element: class="fragment fade-up" -->
* GOLANG <!-- .element: class="fragment fade-up" -->
* GRPC <!-- .element: class="fragment fade-up" -->
* VCLUSTER <!-- .element: class="fragment fade-up" -->
--
#/CHAPTER2: CREATOR
* FEATURES <!-- .element: class="fragment fade-up" -->
* DYNAMIC KUBERNETES W/ GOLANG <!-- .element: class="fragment fade-up" -->
* TASKFILE <!-- .element: class="fragment fade-up" -->
--
#/CHAPTER3: INFORMER
* FEATURES <!-- .element: class="fragment fade-up" -->
* DYNAMIC KUBERNETES W/ GOLANG <!-- .element: class="fragment fade-up" -->
* HELMTEST <!-- .element: class="fragment fade-up" -->
* INFORMER <!-- .element: class="fragment fade-up" -->
--
#/CHAPTER4: OPERATOR
* FEATURES <!-- .element: class="fragment fade-up" -->
* DYNAMIC KUBERNETES W/ GOLANG <!-- .element: class="fragment fade-up" -->
* HELMFILE <!-- .element: class="fragment fade-up" -->
--
#/CHAPTER5: DEMO + COMING UP
* DEMO-CLUSTER <!-- .element: class="fragment fade-up" -->
* ANALYZER <!-- .element: class="fragment fade-up" -->
* FETCHER <!-- .element: class="fragment fade-up" -->
---
### /Introduction

<span style="color:orange">#DevOps #CICD #Automation #Cloud #IAC</span>
<span style="color:orange">#Kubernetes #Containerization</span> <br><br>

Patrick Hermann
System-Engineer SVA Stuttgart
patrick.hermann@sva.de
--

#/CHAPTER1: Challenge 

#/ INTRO

--
#/ PIPELINE AS CODE ON KUBERETES
* FLEXIBILITY: CONTAINER(-IMAGES)  
* COSTS
* SCALABILITY
--
#/ TEKTON
* BUILDING BOCKS
* 
#/ ADVANTAGES
* Customizable - define a highly detailed catalog of building blocks for developers
* Reusable + Expandable - quickly build complex pipelines 
* Standardized - Tekton installs and runs as an extension on your Kubernetes cluster and uses the well-established Kubernetes resource model. Tekton workloads execute inside Kubernetes containers.
* Scalable. To increase your workload capacity, you can simply add nodes to your cluster. Tekton scales with your cluster without the need to redefine your resource allocations or any other modifications to your pipelines.
--
