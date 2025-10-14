+++
weight = 20
+++

{{< slide id=tekton_kcl background-color="rgba(140, 196, 214, 1)" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /TEKTON+KCL

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton_ball.png" alt="Alt Text" width="600" style="border: 1px; box-shadow: none;" />

---

### /TEKTON

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton_pr.gif" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

- **Kubernetes-native** pipeline automation
- **Custom Resource Definitions (CRDs)** for pipeline constructs

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

### /TEKTON-TASK(S)

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton-task.png" alt="Alt Text" width="1000" style="border: 1px; box-shadow: none;" />

* Reusable tasks

---

### /TEKTON RESOLVER (GIT)

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton-resolvers.png" alt="Alt Text" width="700" style="border: 1px; box-shadow: none;" />

* Resolve task from git

---

### /TEKTON RESOLVER (OCI)

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/taskrun-oci.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

* Resolve task from oci registry

---

### /TEKTON-PIPELINERUN

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton-pr.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /KCL

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl-k8s.png" alt="Alt Text" width="700" style="border: 1px; box-shadow: none;" />

- **Constraint-based record & functional language** for complex configurations
- **Cloud-native focused** - perfect for Kubernetes and platform engineering

---

### **Key Characteristics**
- **Easy-to-use** - Python/Golang-like syntax
- **Safety-first** - No system-level functions, low security risk
- **Rich tooling** - IDE extensions, formatting, linting, testing
- **High performance** - Built with Rust, compiles to native/WASM

---

### /GENERAL KCL-EXAMPLE

* SHOW GIF FROM TRANSFORMING (KUBECTL APPLY)

---

### /💬 TL;DR

using the kcl k8s library gives you:

* ✅ Type safety
* ✅ Schema validation
* ✅ Version compatibility
* ✅ Autocompletion
* ✅ Easier composition and reuse

---

# /KCL TEKTON INTEGRATION
GIF + INIT + MOD DL


* TEKTON LIB
* USECASE EXMAPLE (BUILDAH PR)
* MODULE CODE
---

### SCHEMA

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl-schema.png" alt="Alt Text" width="1400" style="border: 1px; box-shadow: none;" />

---

### 🎨 **GUM: Glue for Command Line Tools**

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/gum-choose.gif" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

- **Elegant shell scripts** made easy
- **Interactive components** for CLI applications
- **Bash script enhancer** with beautiful UI elements

---
<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/gum-choose.gif" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

- **Elegant shell scripts** made easy
- **Interactive components** for CLI applications
- **Bash script enhancer** with beautiful UI elements

---

### GUM + KUBECTL + TKN

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/gum_tkn.gif" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### TASKFILE

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/taskfile-gum.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

{{% /section %}}
