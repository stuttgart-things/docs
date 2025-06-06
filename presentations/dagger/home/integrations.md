+++
weight = 40
+++

{{< slide id=integrations background-color="#A2D8FF" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# INTEGRATIONS

---

### /DAGGER CLOUD

<img src="https://blog.ogenki.io/post/dagger-intro/dagger-cloud.png" alt="Alt Text" width="600" style="border: 1px; box-shadow: none;" />

---

### /DAGGER CLOUD

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/idp/dagger-cloud.png" alt="Alt Text" width="4000" style="border: 1px; box-shadow: none;" />

- Visualize your pipeline's DAG, inputs/outputs, and execution logs
- Explore how your pipeline is structured, down to each function call

---

### /GITHUB WORKFLOW DEFINITION

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/gh.png" alt="Alt Text" width="4000" style="border: 1px; box-shadow: none;" />

- Runs on dagger runner

---

### /GITHUB EXECUTION

<img src="https://blog.ogenki.io/post/dagger-intro/github-actions-output.png" alt="Alt Text" width="4000" style="border: 1px; box-shadow: none;" />

- Workflow output

---

### /GITLAB WORKFLOW DEFINITION

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/idp/gl-dagger.png" alt="Alt Text" width="4000" style="border: 1px; box-shadow: none;" />

- Runs on dagger runner

---

### /GITLAB EXECUTION

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/gl-pipeline.png" alt="Alt Text" width="4000" style="border: 1px; box-shadow: none;" />

---

### /TASKFILE

<img src="https://tsh.io/wp-content/uploads/2021/04/taskfile-preference-meme.png" alt="Alt Text" width="4000" style="border: 1px; box-shadow: none;" />

---

### /TASKFILE

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/idp/task.png" alt="Alt Text" width="4000" style="border: 1px; box-shadow: none;" />

---

### /TASKFILE

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/idp/taskfile2.gif" alt="Alt Text" width="4000" style="border: 1px; box-shadow: none;" />

---

> ### ❓ Audience
>
> **HOW DO YOU AUTOMATE TASKS LOCALLY?**
>
> - 🛠️ make
> - 📦 Taskfile
> - 🌍 Earthfile / earthly
> - 📜 Shell scripts
> - 🧪 Justfile
> - 🚫 None

---

### /KUBERNETES / GITHUB

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/dind.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

- gh runner deployment w/ flux
- dind indicates the mode used to launch the containers.
- ⚠️Dagger must run as a root user and have elevated privileges in order to control containers, volumes, networks, etc.

---

### /KUBERNETES / EKS

<img src="https://blog.ogenki.io/post/dagger-intro/dagger-cache-kubernetes.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

- The Dagger Engine: A single pod exposes an HTTP service
- Specific Node Pool: A node pool with constraints to obtain local NVME disks

---

### /MORE INTEGRATIONS

- Google Cloud Run
- Nerdctl
- Podman
- OpenShift


{{% /section %}}
