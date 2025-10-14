+++
weight = 30
+++

{{< slide id=tinkerbell background-color="#dd44b9ff" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tinkerbell.jpeg" alt="Alt Text" width="350" style="border: 1px; box-shadow: none;" />

# /TINKERBELL-CROSSPLANE

**Tinkerbell brings cloud-native principles to physical infrastructure** 🌩️➡️🔧

---

### 🚀 Cloud-Native Bare Metal Provisioning

**What Tinkerbell Does**
- **Automates bare metal infrastructure** like VMs automate cloud infrastructure
- **Treats physical servers as cattle, not pets** - fully automated lifecycle management
- **Provisioning as code** - declarative workflows for consistent, repeatable deployments

---

### **Why Cloud-Native?** 🏗️

| Traditional Provisioning | Tinkerbell (Cloud-Native) |
|-------------------------|---------------------------|
| ❌ Manual/PXE boot scripts | ✅ **Declarative workflows** |
| ❌ Golden images | ✅ **Container-based actions** |
| ❌ Static configurations | ✅ **Dynamic, API-driven** |
| ❌ Monolithic tools | ✅ **Microservices architecture** |

---

### **Key Cloud-Native Benefits**

- **Containerized Actions**: Every operation runs in containers → portable, versioned
- **Orchestration**: Kubernetes-native workflow engine
- **API-Driven**: REST APIs for all operations
- **Declarative**: Infrastructure-as-Code approach
- **Extensible**: Custom actions via container images
- **GitOps Ready**: Version control for provisioning workflows

---

### **Use Cases**
- **Bare metal Kubernetes** cluster provisioning
- **Data center automation** at scale
- **Edge computing** deployments
- **Hybrid cloud** infrastructure
- **Disaster recovery** automation

---

> ### ❓ Audience
>
> **What are you using for BareMetal Provisioning?**
>
> - 🦊 Tinkerbell
> - 🐙 Kairos
> - ⚙️ Metal³ (Cluster API BareMetal Provider)
> - 🧠 Talos (direct bare-metal install)
> - 🧩 Custom PXE / iPXE setup
> - 🪙 Other (please specify)

---

### Workflow Execution

- Worker boots via **iPXE**
- Loads **HookOS** (minimal container runtime environment)
- HookOS connects to **Tink server**
- Registers itself as available worker

---

### Workflow Execution
- Tink server starts workflow
- Assigns **Tasks** to appropriate worker
- HookOS pulls and runs **action container images sequentially**
- Each action runs in container with:
  - Environment variables
  - Mounted volumes
  - Defined in Task configuration

---

## 🔹 Component Roles

| Component | Role |
|-----------|------|
| **Tinkerbell Cluster** | Orchestrates and monitors workflows |
| **HookOS on Worker** | Executes each action container |
| **Action Image** (e.g., `image2disk`) | Runs inside HookOS, performs actual operations |

---

## 🔹 Key Architecture Points

- **HookOS**: Minimal runtime → fast boot, secure execution
- **Container-based**: Each action isolated in containers
- **Sequential Execution**: Actions run in defined order
- **Declarative**: Workflows defined as code

---

## 🔹 Example Actions

```yaml
- name: "disk-wipe"
  image: "disk-wipe:latest"
- name: "os-install"
  image: "image2disk:latest"
- name: "reboot"
  image: "reboot:latest"
```

---

> ### ❓ Audience
>
> **What are you using for BareMetal Provisioning?**
>
> - 🦊 Tinkerbell
> - 🐙 Kairos
> - ⚙️ Metal³ (Cluster API BareMetal Provider)
> - 🧠 Talos (direct bare-metal install)
> - 🧩 Custom PXE / iPXE setup
> - 🪙 Other (please specify)

---

### /PROVISIONING

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/Tinkerbell%2Fprovisioning-logs.gif" alt="Alt Text" width="1800" style="border: 1px; box-shadow: none;" />

---

### 🔍 Kubernetes Log Analysis Toolkit

The Trio: **K9s** + **Stern** + **Gonzo**

| Tool | Purpose |
|------|---------|
| **K9s** | Cluster navigation & pod management |
| **Stern** | Multi-pod log tailing with label selectors |
| **Gonzo** | Log pattern analysis & anomaly detection |

> Don't choose — use all three together! 🚀

---

### K9S + GONZO

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/k9s_gonzo_example.gif" alt="Alt Text" width="1600" style="border: 1px; box-shadow: none;" />

---

### STERN + GONZO

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/stern_gonzo_example-3.gif" alt="Alt Text" width="1600" style="border: 1px; box-shadow: none;" />

---

## /CROSSPLANE

---

### /XRD

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/crossplane-xrd.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /COMPOSITION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/crossplane-composition.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /CLAIM

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/crossplane-claim.png
" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

# /CROSSPLANE + KCL

---

### /KCL FUNCTION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/xplane-kcl-function.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /KCL COMPOSITION INLINE

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl-crossplane-inline.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /KCL MODULE

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kcl-module-tink.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /KCL COMPOSITION OCI

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/xplane-kcl-composition.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

# /TINKERBELL WORKFLOW

---

### /KUBECONFIG SECRET

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/vso.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /CROSSPLANE PROVIDER DEFINITION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/crossplane-k8s-provider.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---


{{% /section %}}
