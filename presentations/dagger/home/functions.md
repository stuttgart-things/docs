+++
weight = 20
+++

{{< slide id=functions background-color="#B3B3FF" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /FUNCTIONS

<img src="https://i.kym-cdn.com/entries/icons/facebook/000/016/546/hidethepainharold.jpg" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

```bash
dagger call -m github.com/hidethepain@1.2.3 phone \
--who=harold -vv --progress plain
```
---

### /Functions

- Definition: A function is a single composable operation within a module.
- Structure: Think of it like a method—you call it with parameters and it performs a CI/CD task.
- Purpose: Represents one specific action in your workflow.
- Analogy: Like a function in any programming language, but declaratively building pipelines.
- Example: docker.build() or git.clone().

---

### /YAML-FILE


<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/freeze.png" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />

---

### /DAGGERVERSE

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/daggerverse.png" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />

---

### /YAML-LINT

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/lint.gif" alt="Alt Text" width="1750" style="border: none; box-shadow: none;" />

---

### /TRIVY-OPTIONS

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/function_help.gif" alt="Alt Text" width="1750" style="border: none; box-shadow: none;" />

- shows help text for a specific function within a Dagger module

```bash
dagger call -m <module-path> <function-name> --help
```

---



{{% /section %}}
