+++
weight = 40
+++

{{< slide id=outro background-color="#c718daff" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /DAGGER

---

### /OVERVIEW DAGGER

<img src="https://i.ytimg.com/vi/cwa_MBL1kek/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCUYIRpVO-rvIqoANUzRxM5BV4_2g" alt="Alt Text" width="400" style="border: 1px; box-shadow: none;" />

- Replace YAML-heavy complex CI pipelines with clean, reusable code
- Transform code into containerized + composable operations
- Build reproducible workflows in any language with custom environments and parallel processing + seamless chaining
- Run the same pipeline on your local machine or (any) CI runner
---

### /Dagger Team

<img src="https://techcrunch.com/wp-content/uploads/2022/03/Dagger-Redpoint.jpeg" alt="Alt Text" width="600" style="border: 1px; box-shadow: none;" />

- Dagger Inc. was co-founded by Solomon Hykes in 2021
- backed by many of the original Docker core engineers
- Core functionality (open source), Dagger Cloud (commercial)
---

> ### ❓ Audience
>
> **ARE YOU USING DAGGER (YET)?**
>
> - ✅ Yes, actively using it
> - 🧪 Tested it briefly
> - ❌ Not yet, but interested
> - 🚫 No, not planning to use

---

### DAGGER FUNCTION CALL


---

### DAGGER SERVICE

* GOLANG TESTING
* K8s / HELM TESTING

---

### /(Reusable) Modules

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/functions_crane.gif" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />


- Analogy: Like a library or plugin for CI/CD workflows.

- Example: A module called docker might expose functions like build, push, and scan.

---

### /CREATE MODULE

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/module.gif" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />

---

### /CHAINING + USE IMPORTS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/helm-lint.png" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />

- Usage of imported helm module

---

### /PIPELINE-DEFINITION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/pipeline.png" alt="Alt Text" width="700" style="border: none; box-shadow: none;" />

---

### DAGGER AI-AGENTS




---

### DAGGER SHELL

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/dagger_shell.gif" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />

---

### CONTAINER-USE - Isolated Dev Environments for AI Agents

- **CLI tool** that plugs into MCP-compatible agents (Claude Code, Cursor)
- **Gives AI agents superpower**: create/manage isolated dev environments on-demand
- **Enables parallel task execution** without conflicts
- **Powered by Dagger** under the hood

---

### CONTAINER USE CO-PILOT INTEGRATION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/container-use.png" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />

---

> ### ❓ Audience
>
> **ARE YOU IN USING/TESTING DAGGER?**
>
> - ✅ Yes
> - 🚫 No


{{% /section %}}
