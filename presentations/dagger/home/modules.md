+++
weight = 50
+++

{{< slide id=modules background-color="#FFD4B3" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# MODULES

---

### /MODULES

<img src="https://media.makeameme.org/created/modules-modules-everywhere-5bd745.jpg" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /Dagger Modules

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/star.png" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />

- Modules are just source code
- Binary artifacts are built locally, and cached.
- Git is the source of truth.
- Dependencies are pinned by default.
- Semantic versioning using git tags.

---

### /(Reusable) Modules

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/idp/module.png" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />

- Definition: A module is a reusable package of CI/CD logic written in code (e.g., Go, Python, or any supported language).

- Structure: Typically lives in its own Git repo or folder and contains multiple functions.

- Purpose: Encapsulates a set of related workflows (e.g., a Docker build pipeline, a Kubernetes deployment strategy).

---

### /(Reusable) Modules

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/functions_crane.gif" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />


- Analogy: Like a library or plugin for CI/CD workflows.

- Example: A module called docker might expose functions like build, push, and scan.

---





{{% /section %}}
