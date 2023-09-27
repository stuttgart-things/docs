# /TEKTON
--
### /What is tekton?
* kubernetes native ci/cd system <!-- .element: class="fragment fade-up" -->
* You want to declaritvely manage your entire setup: <!-- .element: class="fragment fade-up" -->

```
kustomize build ./tekton-pipelines | kubectl apply -f -
```
will have your entire build system setup
<!-- .element: class="fragment fade-up" -->
--
### /What is tekton?

step: smallest unit of execution, a container image
task: multiple steps run sequentially
pipeline: multiple tasks, can be in parallel or any DAG
taskrun: an execution of a task
pipelinerun: an execution of a pipeline
workspace: directories you can pass between tasks, mounted in all steps in task
params: strings (or arrays) you can declare and pass one level down