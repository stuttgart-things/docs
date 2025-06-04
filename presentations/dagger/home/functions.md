+++
weight = 20
+++

{{< slide id=functions background-color="#B3B3FF" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /FUNCTIONS

single composable operationa within a module

<img src="https://i.kym-cdn.com/entries/icons/facebook/000/016/546/hidethepainharold.jpg" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

```bash
dagger call -m github.com/hidethepain@1.2.3 phone \
--who=harold -vv --progress plain
```
---

### /EXAMPLE: A(NY) YAML-FILE

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/freeze.png" alt="Alt Text" width="7000" style="border: none; box-shadow: none;" />

- YAML is indentation-sensitive and whitespace-dependent
- A small mistake can break the file.

---

> ### ❓ Audience
>
> **WHAT IS YOUR MAIN PROGRAMING LANGUAGE?**
>
> - BASH
> - PYTHON
> - GOLANG
> - RUST
> - JS/JAVA
> - ..?

---

### /DAGGERVERSE

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/daggerverse.png" alt="Alt Text" width="7000" style="border: none; box-shadow: none;" />

- free service run by Dagger
- indexes all publicly available Dagger Functions

---

### /YAML-LINT FUNCTION CALL

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/lint.gif" alt="Alt Text" width="1750" style="border: none; box-shadow: none;" />

- call it with parameters
- performs a CI/CD task.

---

### /FUNCTION PARAMETERS (EXAMPLE TRIVY)

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/function_help.gif" alt="Alt Text" width="1750" style="border: none; box-shadow: none;" />

- shows help text for a specific function

```bash
dagger call -m <module-path> <function-name> --help
```

> ### ❓ Audience
>
> **HOW DO YOU USE CI-FUNCTIONS **
>
> - 🦊 TO BE CONTINOUS
> - 🐙 GITHUB ACTIONS
> - ⚙️ Jenkins
> - 🚀 Tekton TASKRUNS
> - 🚀 MAKE/TASKFILE

> - ..?

---

### EXAMPLE CONTAINER DEFINTION / BUILD

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/kyverno_ctr.png" alt="Alt Text" width="1750" style="border: none; box-shadow: none;" />

- kyverno installation in container
- dagger golang sdk / wolfi linux as base
---

#### EXAMPLE FUNCTION (GOLANG)

- use of kyverno container + directory mounts

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/kyverno_validate.png" alt="Alt Text" width="800" style="border: none; box-shadow: none;" />

---

### EXAMPLE FUNCTION (PYTHON)

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/gitlab-mr.png" alt="Alt Text" width="800" style="border: none; box-shadow: none;" />

- no dedicated container used
- python json pakage import/usage

{{% /section %}}
