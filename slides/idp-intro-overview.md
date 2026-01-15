# /INTRODUCTION

---

# /Platform Foundations

---

#### /Platform Foundations

<img src="https://media.licdn.com/dms/image/v2/D4D22AQHolX5UwNFzPg/feedshare-shrink_800/B4DZTyTdDSG8Ag-/0/1739231974056?e=2147483647&v=beta&t=0V2HW-dJHygYyHMp4Kv-TbTgrue10vzZL2TYzzZmv_k" alt="Alt Text" width="400"/>

- platform engineering is a evolution of DevOps
---


### /DEV-EX

<img src="https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fi%2Fbeozmmi208ae3ye2dr3v.jpg" alt="Alt Text" width="500"/>

- Developer Experience = creating an environment in which a developer can do their best work
- Good DevEx = fewer frustrations and more productivity
- leading to faster delivery and better software quality

---

### /DEV-EX

“A means for capturing how developers think and feel about their activities within their working environments.”
F. Fagerholm & J. Münch, 20212

---

### /IDP

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/devops-idp.png" alt="Alt Text" width="700"/>

---

### /IDP

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/idps.png" alt="Alt Text" width="700"/>

( - Amazon Web Services)

---

### /IDP

Why it is a good idea to build an **Internal Developer Platform Portal**:

- 🧩 **A centralized UI for developers**
- 🤖 **A self-service layer over infrastructure**
- 🚀🛡️ **A tool to accelerate delivery with guardrails**

<br>
<br>
<br>
<br>

> Think: “PaaS built by your platform team”

---

### 🚀 DORA Metrics

DORA (DevOps Research and Assessment) metrics measure software delivery performance:

- **Deployment Frequency**
- **Lead Time for Changes**
- **Change Failure Rate**
- **Mean Time to Recovery (MTTR)**

---

# 📈 IDPs Make DORA Metrics Actionable

| Metric | How an IDP Helps |
|--------|------------------|
| 📦 Deployment Frequency | Self-service deploys, GitOps integration |
| ⏱️ Lead Time for Changes | Track from commit → production |
| ❌ Change Failure Rate | Show failed rollouts, incident links |
| 🛠️ MTTR | Connect services to runbooks, SLOs, and ownership |

---

### ⚙️ /Core Features

<img src="https://pradeepl.com/blog/internal-developer-portals-spotify-backstage/images/Backstage-Templates.png" alt="Alt Text" width="1000"/>

- 🛠️ Self-service deployment & environment provisioning
- 🔍 Visibility into logs, metrics, and deployments
- 🚦 Policy enforcement (e.g. security, cost, compliance)
- 📦 Template catalogs for fast onboarding

---

### 🚀 /Key IDP Benefits

➡️ **Developers Focus on Code, Not Infrastructure**

- ⚡️ **Focus on shipping features faster**
  → *"From idea to production in minutes, not days"*

- 🧠 **Focus purely on business logic**
  → *"No more YAML archaeology or cloud config headaches"*

- 🎓 **Self-service resources**
  *"Provision full dev environment with single click"*

- 🧩 **Clear ownership boundaries**
  → *"Devs own code, Platform owns infrastructure"*

---
### 📈 /Measuring Adoption

> Adoption shows whether developers trust, use, and benefit from the platform

- 🔁 **DAU/WAU/MAU**: Daily / Weekly / Monthly active users
- 🚀 **Self-service actions**: Number of created services, environments, deployments
- 🔍 **Time to First Deploy (TTFD)**: How fast a dev goes from repo to running app
- 💬 **Feedback loops**: Surveys, interviews, support tickets

---

<!-- slide -->
<!-- ### /Quick Poll #1

> 🎯 Have you ever worked with an **Internal Developer Portal (IDP)**?

- 🎭 **Yes, with Backstage** — love the plugin ecosystem!
- 🧱 **Yes, with another tool** — like Port, Cortex, or OpsLevel
- 🛠️ **We built our own custom IDP** — DIY all the way
- 🧩 **Heard of IDPs, but not used one yet**
- 🤷 **What’s an IDP?** — sounds fancy! -->

<!--
> ### /Quick Poll #1
>
> Why is it beneficial to build an Internal Developer Platform Portal?
>
> - 👨‍💻 To centralize developer UI and accelerate delivery
> - ⚙️ To make infrastructure more complex
> - ⏳ To increase onboarding time

---

> ### /Quick Poll #2
>
> Which core IDP feature helps developers deploy and provision environments on their own?
>
> - 🔍 Visibility into logs and metrics
> - 🛠️ Self-service deployment & environment provisioning
> - 🚦 Policy enforcement -->


---


### /IDP
#### /PLAN

**Projektplanung (Jira, Confluence, GitHub Projects)**

- **Scorecards / Qualität-Metriken:**
  - Früh zeigen, wie reif bzw. „production-ready“ ein Service oder Modul ist – z. B. technischer Zustand, Wartbarkeit, Sicherheit.
- **Software / Service Katalog:**
  - Abbild aller verfügbaren Services, Bibliotheken, Infrastruktur­module inkl. Ownership, Zustand, Abhängigkeiten. Entwickler können früh sehen, was schon existiert
- **Dokumentations-Hub:**
  - Katalogisierung von Projekten, Teams, Komponenten und Technologien

---

### /IDP
#### /CODE

**Versionskontrolle (GitHub / GitLab, IDEs)**

- **Governance & Policies eingebettet:**
  - Sicherheits- und Architektur-Vorgaben automatisch bei Projekt-Erstellung sichtbar bzw. durchgesetzt.
- **Integration mit Versionsverwaltung/CI Tools:**
  - Das Portal zeigt z. B. Builds, Pull Requests, Test-Status, so dass Entwicklung in den Überblick integriert ist.
- **Self-service Aktionen /Scaffolding:**
  - vordefinierten Templates (Golden Paths) und Automatisierungen

---

### /IDP
#### /BUILD

**CI/CD Pipeline (GitLab CI, GitHub Actions)**

- **Automatisierte Workflows / Golden Paths:**
  - Standardisierte Build-Pipelines als Teil eines Self-service-Workflows im Portal.
- **Integrationen mit Build/CI-Systemen:**
  - Portal kann Build-Ergebnisse/Status visualisieren, macht Builds transparent.

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/build.png" alt="Alt Text" width="700"/>

---

### /IDP
#### /TEST

**Automatisiertes Testen (JUnit, Selenium)**

- **Dashboard / Integrationen mit Test-Tools:**
  - Testergebnisse, Qualität im Kontext von Services sichtbar gemacht.
- **Scorecards / Qualitätsmetriken:**
  - Portal zeigt Test-Coverage, Sicherheitslücken, Wartbarkeit – Entwicklung sieht früh, ob Qualität stimmt.

---

### /IDP
#### /RELEASE

**Release-Management Tools (Spinnaker, Octopus Deploy)**

- **Workflows / Automatisierung:**
  - Automatisierte Genehmigungen, Rollbacks, Canary-Releases integriert im Portal.

---

### /IDP
#### /DEPLOY

**Deployment Automation (Terraform, Ansible, Helm, ArgoCD)**

- **Self Service Deployment:**
  - Deployment Triggern, Umgebungen bereitstellen
- **Deployment Katalog:**
  - Katalog & Ownership: Services, die deployt werden, im Katalog mit Verantwortlichen, sodass Deployment klar zugeordnet ist.

---

### /IDP
#### /OPERATE

**Konfigurationsmanagement (Chef, Puppet)**

- **Scorecards / Service-Reifegrade:**
  - Laufende Bewertung eines Services im Betrieb – z. B. Stabilität, MTTR, Kosten.
- **Governance, Compliance, FinOps:**
  - Zugriffskontrolle, Audit Trails, Kostenübersicht – Betrieb unter Einhaltung von Vorgaben.

---

### /IDP
#### /MONITOR

**Monitoring-Tools (Prometheus, ELK)**

- **Statusüberwachung:**
  - Integrationen mit Observability/Monitoring-Tools: Logs, Metriken, Traces in Portal gebündelt dargestellt.

---

### /MULTICLOUD

<img src="images/multicloud.jpeg" alt="Alt Text" width="700"/>

- ☁️ Balance cost, performance & availability
- 🎛️ Unified control plane across clouds
- 📡 Cloud-agnostic CI/CD and GitOps
-

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

### /Quick Poll

> 🔄 What’s your **go-to GitOps tool** for managing Kubernetes and infrastructure?

- 🚀 **Argo CD** — Declarative, visual, Git-native deployments
- 🌀 **Flux** — GitOps toolkit built for flexibility and composability
- 🔧 **Jenkins X**, **Fleet**, or other custom GitOps solutions
- ❓ Still exploring — curious what all the hype is about?



{{% /section %}}
