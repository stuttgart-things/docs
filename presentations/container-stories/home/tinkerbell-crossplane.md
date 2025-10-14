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

- **Treats physical servers as cattle, not pets** - fully automated lifecycle management
- **Automates bare metal infrastructure** like VMs automate cloud infrastructure
- **Provisioning as code** - declarative workflows for consistent, repeatable deployments
- **GitOps Ready** - Version control for provisioning workflows
---

### **Why is Tinkerbell Cloud-Native?** 🏗️

| Traditional Provisioning | Tinkerbell (Cloud-Native) |
|-------------------------|---------------------------|
| ❌ Manual/PXE boot scripts | ✅ **Declarative workflows** |
| ❌ Golden images | ✅ **Container-based actions** |
| ❌ Monolithic tools | ✅ **Microservices architecture** |

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

### **Key Cloud-Native Benefits**

- **Containerized Actions**: Every operation runs in containers → portable, versioned
- **Orchestration**: Kubernetes-native workflow engine
- **API-Driven**: REST APIs for all operations
- **Declarative**: Infrastructure-as-Code approach
- **Extensible**: Custom actions via container images
- **GitOps Ready**: Version control for provisioning workflows

---

### Hardware

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/Tinkerbell%2FBilder%2Ftinkerbell-hw.png" alt="Alt Text" width="450" style="border: 1px; box-shadow: none;" />

---

### TEMPLATE

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/Tinkerbell%2FBilder%2Ftinkerbell-template2.png" alt="Alt Text" width="1600" style="border: 1px; box-shadow: none;" />

---

### PXE BOOT

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/Tinkerbell%2FBilder%2Fpxe-provisioning.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

- Worker boots via **iPXE**
- Loads **HookOS** (minimal container runtime environment)
- HookOS connects to **Tink server** / Registers itself as available worker

---

### WORKFLOW

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/Tinkerbell%2FBilder%2Factions.png
" alt="Alt Text" width="1600" style="border: 1px; box-shadow: none;" />

---

### Workflow/Actions

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/Tinkerbell%2FBilder%2Fpxe-provisioning.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

- Tink server starts workflow
- Assigns **Tasks** to appropriate worker
- HookOS pulls and runs **action container images sequentially**

---

## 🔹 Component Roles

| Component | Role |
|-----------|------|
| **Tinkerbell Cluster** | Orchestrates and monitors workflows |
| **HookOS on Worker** | Executes each action container |
| **Action Image** (e.g., `image2disk`) | Runs inside HookOS, performs actual operations |

---

### /PROVISIONING

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/Tinkerbell%2Fprovisioning-logs.gif" alt="Alt Text" width="1800" style="border: 1px; box-shadow: none;" />

---

## /CROSSPLANE

---

+++
title = "Crossplane: Cloud Native Control Plane"
+++

## 🎯 What is Crossplane?

### **The Cloud Native Control Plane**
- **Extends Kubernetes API** to manage anything
- **Universal API for cloud resources** - infrastructure as Kubernetes objects
- **GitOps for everything** - apps, databases, clusters, buckets, etc.

---

### **Key Concepts**

| Component | Purpose | Analogy |
|-----------|---------|----------|
| **XRD** | Defines new API types | Custom Resource Definition |
| **Composition** | Templates resource creation | Blueprint |
| **Claim** | User request for resources | Order form |
| **Composite Resource** | Actual provisioned resources | Fulfilled order |

---

### /XRD

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/crossplane-xrd.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

- Defines new API types
---

### /COMPOSITION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/crossplane-composition.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

-  Templates resource creation

---

### /CLAIM

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/crossplane-claim.png
" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

- User request for resources

---

### /CONFIGURATION

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

### /TINKERBELL WORKFLOW

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/tink-xplane.png" alt="Alt Text" width="1200" style="border: 1px; box-shadow: none;" />

---

### /KUBECONFIG SECRET

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/vso.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### /CROSSPLANE PROVIDER DEFINITION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/crossplane-k8s-provider.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---


{{% /section %}}
