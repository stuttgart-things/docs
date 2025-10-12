+++
weight = 20
+++

{{< slide id=tekton_kcl background-color="#b36ed0ff" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /TEKTON+KCL

---

> ### ❓ Audience
>
> **WHAT CI/CD DO YOU USE?**
>
> - 🦊 GitLab CI
> - 🐙 GitHub Workflows
> - ⚙️ Jenkins
> - 🚀 Tekton
> - 🚀 Dagger
> - ..?

---

### /TEKTON-PIPELINES

* SHOW GIF OF RUNNING PIPELINE

---

### /TEKTON-TASK(S)

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton-task.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /TEKTON-RESOLVERS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton-resolvers.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /KCL

* Type Safety: The schema enforces proper types for all fields
* Reusability: The schema can be reused for multiple PipelineRun configurations
* Validation: KCL will validate the configuration against the schema
* Maintainability: Clear separation between schema definition and configuration
* Extensibility: Easy to add new fields or modify existing ones

---

### /GENERAL KCL-EXAMPLE

* SHOW EASY MANIFEST (FREEZE, SERVICE)
* SHOW GIF FROM TRANSFORMING (KUBECTL APPLY)

---

💬 TL;DR

You can define Kubernetes objects manually — but importing the k8s library gives you:

✅ Type safety

✅ Schema validation

✅ Version compatibility

✅ Autocompletion

✅ Easier composition and reuse
---

# /KCL TEKTON INTEGRATION

---

### MODULE CREATION

GIF + INIT + MOD DL

---

### SCHEMA

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl-schema.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---


* TEKTON LIB
* USECASE EXMAPLE (BUILDAH PR)
* MODULE CODE
* TASKFILE + GUM



{{% /section %}}
