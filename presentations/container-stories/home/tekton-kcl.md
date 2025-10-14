+++
weight = 20
+++

{{< slide id=tekton_kcl background-color="rgba(232, 45, 85, 1)" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /TEKTON+KCL

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton-sthings.png" alt="Alt Text" width="400" style="border: 1px; box-shadow: none;" />

---

### /TEKTON

- **Kubernetes-native** pipeline automation
- **Custom Resource Definitions (CRDs)** for pipeline constructs
- **Serverless execution** - runs entirely within your K8s cluster
- **Open standard** - part of the CD Foundation

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

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton_pr.gif" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

* 🚀 Runs Everywhere Kubernetes Runs

---

### /TEKTON-TASK(S)

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton-task.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

* Reusable tasks

---

### /TEKTON-RESOLVERS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton-resolvers.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

* Resolve from git tasks

---

### /TEKTON-RESOLVERS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton-resolvers.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

* Resolve from oci reg

---

### /TEKTON-PIPELINERUN

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton-pr.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /KCL
- **Constraint-based record & functional language** for complex configurations
- **Cloud-native focused** - perfect for Kubernetes and platform engineering
- **Enhances configuration writing** with better modularity, scalability, and stability
- **Open-source** with production usage at Ant Group

---
### /KCL SCHMEA + DEFINTIION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl-k8s.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

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

---

### MODULE CREATION

GIF + INIT + MOD DL

---

### SCHEMA

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl-schema.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

# GUM

---

### **Glue for Command Line Tools**
- **Elegant shell scripts** made easy
- **Interactive components** for CLI applications
- **Bash script enhancer** with beautiful UI elements
- **Part of Charm ecosystem** (like Glow, Soft Serve)

---

### **Interactive Inputs**

| Component | Purpose | Example |
|-----------|---------|---------|
| `gum input` | Text input | `name=$(gum input --placeholder "Name")` |
| `gum choose` | Multiple choice | `env=$(gum choose "dev" "staging" "prod")` |
| `gum confirm` | Yes/No dialog | `gum confirm "Deploy to prod?"` |
| `gum filter` | Fuzzy search | `pkg=$(echo "pkg1 pkg2" | gum filter)` |

---

### CHOOSE

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/gum-choose.gif" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### INPUT

---

### SPIDER

---

### TASKFILE

---

GIF + INIT + MOD DL


* TEKTON LIB
* USECASE EXMAPLE (BUILDAH PR)
* MODULE CODE
* TASKFILE + GUM



{{% /section %}}
