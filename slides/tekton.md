# /TEKTON
--
### /TEKTON-PIPELINES
--
* Tekton Pipelines is a Kubernetes extension that installs and runs on your Kubernetes cluster <!-- .element: class="fragment fade-up" -->
* It defines a set of Kubernetes Custom Resources that act as building blocks from which you can assemble CI/CD pipelines <!-- .element: class="fragment fade-up" -->
### /TEKTON-PIPELINES
--
* Once installed, Tekton Pipelines becomes available via the Kubernetes CLI (kubectl) and via API calls, just like pods and other resources <!-- .element: class="fragment fade-up" -->
* Tekton is open-source and part of the CD Foundation, a Linux Foundation project <!-- .element: class="fragment fade-up" -->
--
### /TASK

Defines a series of steps which launch specific build or delivery tools that ingest specific inputs and produce specific outputs.
--


TaskRun
Instantiates a <code>Task</code> for execution with specific inputs, outputs, and execution parameters. Can be invoked on its own or as part of a <code>Pipeline</code>
--

Pipeline

Defines a series of <code>Tasks</code> that accomplish a specific build or delivery goal. Can be triggered by an event or invoked from a <code>PipelineRun
--


PipelineRun
Instantiates a <code>Pipeline</code> for execution with specific inputs, outputs, and execution parameters.
--
