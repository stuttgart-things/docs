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

> ### ❓ Audience
>
> **HOW DO YOU BUILD CONTAINER IMAGES?**
>
> - Docker/Buildx
> - Buildah
> - Kaniko
> - Apko
> - Ko
> - ..?

---

### /KCL

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl-k8s.png" alt="Alt Text" width="620" style="border: 1px; box-shadow: none;" />

- **functional language** for complex configurations
- **Cloud-native focused** - perfect for Kubernetes and platform engineering

---

### **KCL Key Characteristics**
- **Easy-to-use** - Python/Golang-like syntax
- **Safety-first** - No system-level functions, low security risk
- **Rich tooling** - IDE extensions, formatting, linting, testing
- **High performance** - Built with Rust, compiles to native/WASM
- **Reusable Modules** - Compose and override configs using functions, imports, and variables.

---

### /KCL RUN

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl-run.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

* runs the kcl code and renders the output (=yaml)

---

### /KCL TEKTON INTEGRATION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tekton-lib.png
" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

* ✅ Version compatibility
* ✅ Autocompletion
* ✅ Easier composition and reuse

---

### TEKTON KCL SCHEMA (SNIPPET)

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl-schema.png" alt="Alt Text" width="1400" style="border: 1px; box-shadow: none;" />

* ✅ Type safety
* ✅ Schema validation

---

### VARIABLES/DEFAULTS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl-defaults.png" alt="Alt Text" width="1400" style="border: 1px; box-shadow: none;" />

---

### KCL RUN TEKTON

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl_tkn.gif" alt="Alt Text" width="1400" style="border: 1px; box-shadow: none;" />

---

> ### ❓ Audience
>
> **DO YOU LIKE YAML?**
>
> - YES
> - NO
> - NEXT
> - ..?

---

### 🎨 **GUM: Glue for Command Line Tools**

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
