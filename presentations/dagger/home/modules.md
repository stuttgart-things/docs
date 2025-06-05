+++
weight = 50
+++

{{< slide id=module background-color="#FFD4B3" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# MODULES

<img src="https://media.makeameme.org/created/modules-modules-everywhere-5bd745.jpg" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /(Reusable) Modules

- Definition: A module is a reusable package of CI/CD logic written in code (e.g., Go, Python, or any supported language).

- Structure: Typically lives in its own Git repo or folder and contains multiple functions.

- Purpose: Encapsulates a set of related workflows (e.g., a Docker build pipeline, a Kubernetes deployment strategy).

- Analogy: Like a library or plugin for CI/CD workflows.

- Example: A module called docker might expose functions like build, push, and scan.

---

Dagger Modules are simply a collection of Dagger Functions, packaged together for easy sharing and consumption. Modules are language-agnostic, but their design is inspired by Go modules:

- Modules are just source code
- Binary artifacts are built locally, and cached.
- Git is the source of truth.
- Dependencies are pinned by default.
- Semantic versioning using git tags.

---



{{% /section %}}
