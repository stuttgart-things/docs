+++
weight = 20
+++

{{< slide id=infra background-color="#D4B9FF" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /Platform Foundations

---

#### /Platform Foundations

<img src="https://media.licdn.com/dms/image/v2/D4D22AQHolX5UwNFzPg/feedshare-shrink_800/B4DZTyTdDSG8Ag-/0/1739231974056?e=2147483647&v=beta&t=0V2HW-dJHygYyHMp4Kv-TbTgrue10vzZL2TYzzZmv_k" alt="Alt Text" width="400"/>

- platform engineering is a evolution of DevOps
---

# 🏗️ Platform Engineering

<img src="https://pbs.twimg.com/media/FnabgQxXwAEDZz6.jpg" alt="Alt Text" width="400"/>

- Platform Engineering is about building **self-service platforms** that abstract complexity.
- Empower developers to ship faster
- Remove infrastructure worries from developers' day-to-day

---

<img src="images/quiz-quiztime.png" alt="KCP" style="width:80%; border: none; box-shadow: none;" />

---

<!-- ✅  The experience developers have when using tools, workflows, and infrastructure Explanation:
Developer Experience (DevEx) refers to how developers perceive and interact with the environment in which they build software — including tools, APIs, documentation, CI/CD pipelines, and team processes. A good DevEx means fewer frustrations and more productivity, leading to faster delivery and better software quality.
 -->

### /DEV-EX

<img src="https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fi%2Fbeozmmi208ae3ye2dr3v.jpg" alt="Alt Text" width="500"/>

- Developer Experience = creating an environment in which a developer can do their best work
- Good DevEx = fewer frustrations and more productivity
- leading to faster delivery and better software quality

---

### /MULTICLOUD

<img src="images/multicloud.jpeg" alt="Alt Text" width="700"/>

- ☁️ Balance cost, performance & availability
- 🎛️ Unified control plane across clouds
- 📡 Cloud-agnostic CI/CD and GitOps

---

### ☸️ /KUBERNETES

<img src="https://pbs.twimg.com/media/FnacgGoXEAAaHV_.jpg" alt="Kubernetes Architecture" style="width: 35%; margin: 2rem 0;" />

Kubernetes provides the **core infrastructure**

- ⚙️ The **execution environment** for containerized workloads
- 📜 A **declarative API** for infra and application resources

---

<img src="images/quiz-quiztime.png" alt="KCP" style="width:80%; border: none; box-shadow: none;" />

---
### 🐙 /GitHub

<img src="https://logos-world.net/wp-content/uploads/2020/11/GitHub-Logo.png" alt="GitHub Logo" style="width: 350px;" style="border: none; box-shadow: none;" />

GitHub provides key building blocks for IDPs:

- 📁 **Source of truth** for code, config, and infra
- ✅ **CI/CD pipelines** with GitHub Actions
- 🔒 **Security & policy checks** (e.g., code scanning, dependabot)
- 🌐 Integrates with platforms like **Backstage** via APIs

> Developers interact with the platform through GitHub, not infrastructure tools.

---

### 🦊 GitLab

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/GitLab_logo.svg/1200px-GitLab_logo.svg.png" alt="GitLab Logo" style="width: 350px;" style="border: none; box-shadow: none;"/>

GitLab offers an **all-in-one DevOps platform** ideal for IDPs:

- 💡 Combines **SCM**, **CI/CD**, **container registry**, and **security** in one tool
- 📦 Provides **Infrastructure-as-Code** and **GitOps** out of the box
- 🔁 Easily integrates with Kubernetes and GitLab Runners
- 🧩 Works well with **Backstage** and other portals as a data source

> GitLab can act as both the **portal interface** and the **engine** behind an IDP.

---

### 🔄 /GITOPS

<img src="https://cdn.prod.website-files.com/63c8f7191194d2a0cf4f630e/67951e7770966bf72c93aa96_Screenshot%202025-01-25%20at%2018.25.04.png" alt="Alt Text" width="500"/>

- modern way to do **Continuous Deployment**, using **Git as the single source of truth** for infra and apps

---

### 🔄 /GITOPS

- 📜 **Declarative Infrastructure** — everything is defined in YAML
- 🔗 **Git as the Source of Truth** — no more config drift
- 🤖 **Automated Sync** — tools like Argo CD & Flux keep clusters aligned
- 🕵️ **Audit & Rollback** — powered by Git history and versioning

> 🚀 **Git push = production change**, with full visibility and control
---

### 🛠️ /GitOps Tools

- **Flux** or **Argo CD** for automated syncing
- **Kustomize** or **Helm** for templating
- **Git** for storing desired state

🧠 Changes in Git → Automatically applied to clusters

---

<!-- ### /Quick Poll #3

> 🔄 What’s your **go-to GitOps tool** for managing Kubernetes and infrastructure?

- 🚀 **Argo CD** — Declarative, visual, Git-native deployments
- 🌀 **Flux** — GitOps toolkit built for flexibility and composability
- 🔧 **Jenkins X**, **Fleet**, or other custom GitOps solutions
- ❓ Still exploring — curious what all the hype is about?
--- -->

<img src="images/quiz-quiztime.png" alt="KCP" style="width:80%; border: none; box-shadow: none;" />

---

### /Crossplane

<div style="display: flex; align-items: center; justify-content: center;">

  <img src="images/vm.png" alt="Left Image" width="600" style="border: none; box-shadow: none;"/>

  <!-- <div style="flex: 3; text-align: center; padding: 0 80px;">
    - <code>kinds: User/Group</code> are types of entity defined in the Software Catalog<br>
    - Representing (a group of) developers, engineers, or operators
  </div> -->

  <img src="images/cluster.png" alt="Right Image" width="600" style="border: none; box-shadow: none;"/>
</div>

- Claims represents a set of managed resources as a single Kubernetes object

---

### /RESOURCE LIFECYCLE

<div style="display: flex; align-items: center; gap: 2rem;">

  <img src="images/proxmox.png" alt="Left Image" width="450" style="border: none; box-shadow: none;" />

  <div>
    <ul>
      <li>Manage infrastructure like K8s resources</li>
    </ul>
  </div>

</div>

---

### /RESOURCE LIFECYCLE

<img src="images/crossplane.gif" alt="Left Image" width="1200" style="border: none; box-shadow: none;"/>

- combination crossplane-terraform-tekton-ansible
---

### /Kro

<div style="display: flex; align-items: center; justify-content: center;">

  <img src="images/kro-claim.png" alt="Left Image" width="600" style="border: none; box-shadow: none;"/>

  <div style="flex: 3; text-align: center; padding: 0 80px;">
    - WebApp is a user request fot a (defined) app
    - App Defintion/Schema is defined in the ResourceGraph
  </div>

  <img src="images/kro-resource.png" alt="Right Image" width="600" style="border: none; box-shadow: none;"/>
</div>


---

## kro 🆚 Crossplane

> 🧩 **kro** excels at grouping Kubernetes resources
> with complex interdependencies into reusable templates.

> ☁️ **Crossplane** is best for provisioning and managing
> cloud infrastructure through Kubernetes.

---
### 🔐 HashiCorp Vault in Platform Engineering

<img src="https://configu.com/wp-content/uploads/2024/07/hashicorp-vault-diagram.png" alt="Right Image" width="600" style="border: none; box-shadow: none;"/>

- Central to **Internal Developer Platforms (IDPs)**:
  - Abstracts secret access away from developers.
  - Standardizes secret injection across environments.
  - Enables automation & policy-driven access.

---

### /KYVERNO

<div style="display: flex; align-items: center; justify-content: center;">

  <img src="images/kyverno-policy.png" alt="Left Image" width="650" style="border: none; box-shadow: none;"/>

  <!-- <div style="flex: 3; text-align: center; padding: 0 80px;">
    - <code>kinds: ClusterPolicy/Claim</code>
    - Claim can be checked against Policy
  </div> -->

  <img src="images/kyverno-claim.png" alt="Right Image" width="550" style="border: none; box-shadow: none;"/>
</div>

- A Kyverno policy defines rules for Kubernetes resources.
- Written in YAML and attached to Kubernetes clusters.

---

### 📜 /Kyverno Overview

| Type    | Purpose                          | Use Case Example                        |
|---------|----------------------------------|-----------------------------------------|
| Validate | Enforce rules & security         | Deny `latest` tag in containers         |
| Mutate   | Modify resources with defaults   | Add missing labels or limits            |
| Generate | Create new resources dynamically | Generate `NetworkPolicy` per namespace  |

---

## 🚀 What Are Golden Pipelines?

- Predefined, opinionated CI/CD workflows
- Built by Platform or IDP teams
- Promote:
  - 🔒 Security
  - ⚙️ Consistency
  - 📈 Efficiency
- Enable:
  - Faster onboarding
  - Compliance by default
  - Self-service for developers

---

## 🧱 Golden Pipelines in Practice

<img src="images/golden-pipeline.png" alt="Alt Text" width="7000" style="border: none; box-shadow: none;" />

- **CI/CD:** Automate build, test, security, and deploy
- **IDP:** Exposed as templates or starter kits
- **Platform Engineering:** Encapsulate policies and tooling
---
<img src="images/quiz-quiztime.png" alt="KCP" style="width:80%; border: none; box-shadow: none;" />

{{% /section %}}