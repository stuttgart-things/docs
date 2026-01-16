# /Platform Foundations

---

#### /Platform Foundations

<img src="https://media.licdn.com/dms/image/v2/D4D22AQHolX5UwNFzPg/feedshare-shrink_800/B4DZTyTdDSG8Ag-/0/1739231974056?e=2147483647&v=beta&t=0V2HW-dJHygYyHMp4Kv-TbTgrue10vzZL2TYzzZmv_k" alt="Alt Text" width="400"/>

- Platform Engineering is an evolution of DevOps


---

# /Platform-Engineering

---

### 🏗️ Platform Engineering

<img src="https://pbs.twimg.com/media/FnabgQxXwAEDZz6.jpg" alt="Alt Text" width="400"/>

- Platform Engineering is about building **self-service platforms** that abstract complexity.
- Empower developers to ship faster
- Remove infrastructure worries from developers' day-to-day

---

### 🏗️ Platform Engineering

"...  is the discipline of designing and building toolchains and workflows that enable **self-service** capabilities for software engineering organizations in the cloud-native era. Platform engineers provide an integrated product most often referred to as an “ **Internal Developer Platform**” covering the operational necessities of the entire lifecycle of an application."

(- Humanitec)

---

### WHEN PLATFORM ENGINEERING PAYS
<img src="https://images.unsplash.com/photo-1504384308090-c894fdcc538d?q=80&w=1400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" alt="When it pays" width="700"/>

---

### Signals it’s worth investing

- ~50 engineers OR rapid growth toward that number

- Repeated infra friction: long onboarding, many infra tickets, inconsistent CI/CD

- Many similar services (microservices) with duplicated build/deploy logic

- Need for self-service and audited defaults (security, compliance)

---

### PLATFORM TEAMS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/platform-teams.png" alt="Alt Text" width="750"/>


---

### EXAMPLE TEAM/COMPANY SIZES

- **Small org ~50 devs** → small platform team (2–4 FTE) focusing on on-boarding & pipeline templates

- **Mid-size ~200 devs** → platform team (6–10 FTE), centralized pipelines, service catalog, self-service infra

- **Enterprise 1000+ devs** → larger platform org (20+ FTE), strong IDP, SLOs, cross-team platform product managers

- **Typical benefits reported:** faster on-board, less duplicated work, measurable dev-hours saved

---

### WHAT ARE GOLDEN PATHS

<img src="https://miro.medium.com/v2/resize:fit:1200/0*BEkTUO3XM3kaQFUl" alt="When to introduce" width="450"/>

- Opinionated, well-documented, supported end-to-end workflows teams are encouraged to use
- Examples: standardized CI/CD pipeline templates, service scaffolding, infra provisioning blueprints
- Goal: let teams ship safely and fast using trusted defaults, keep flexibility via “escape hatches”

---

### WHEN TO INTRODUCE GOLDEN PATHS

<img src="https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=1400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" alt="When to introduce" width="700"/>

---

### Good time to start:

- Multiple teams (≈10+) doing similar CI/CD work

- Repeated pipeline maintenance and breakage across teams

- Onboarding takes weeks, not days

- Desire to reduce cognitive load and increase platform ROI

- Too early if every service is unique and experimentation speed matters more than consistency

---

### Golden Paths Motivation

- Golden Paths help reduce the number of topics and prevent developers from being confronted with everything at once (Cognitive Load Theory)
- Exchange increases knowledge and awareness - in all directions
- Features are more important
- Tools must be perceived as helpful
- Lack of interest/relevance → Self-efficacy

**Love your Developers, not your Tools.**

---

### GOLDEN PATH CHECKLIST
<img src="https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=1400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" alt="Checklist" width="700"/>

---

### GOLDEN PATH CHECKLIST

- 🚀 Identify 1–3 common service types (web service, job, library)
- 🧩 Create a minimal, documented pipeline template for each type
- 📦 Provide scaffolding + repo template (CLI or GitHub template)
- ⚙️ Automate onboarding (one command to get dev environment + run tests)

---

### GOLDEN PATH CHECKLIST

- 📊 Provide observability & defaults (metrics, alerting, tracing) baked into templates
- 🛡️ Add security & compliance hooks (SAST, secrets scanning) as default steps
- 🔧 Offer escape hatches and extension points (custom steps, opt-out)
- 📈 Measure: time-to-first-deploy, infra ticket volume, pipeline failure rate, dev satisfaction

---

### PILOT PLAN (3–6 WEEKS)

- Pick 1 service type + 1 friendly team (pilot).
- Build a minimal Golden Path: repo template, CI pipeline, infra blueprint.
- Document “how to” and run live onboarding with the team.
- Measure baseline metrics (time to onboard, tickets, deploy cadence).
- Iterate for 2 sprints, collect feedback, add escape hatches.
- If successful, expand to 3–5 teams and formalize templates.

---

### METRICS TO TRACK

- DORA metrics: Deployment Frequency, Lead Time for Changes, MTTR, Change Failure Rate
- Time to first green build / Time to first deploy for new devs
- Number of infra/platform tickets per sprint (support load)
- Developer satisfaction / NPS for platform (qualitative)
- Cost metrics: infra cost per service, CI minutes saved, engineer hours saved

---

### PITFALLS & ESCAPE-HATCHES

<img src="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?q=80&w=1400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" alt="Pitfalls" width="700"/>

---

### Pitfalls

- Building a “Golden Cage”: too rigid, blocks innovation
- Over-engineering before real needs exist
- Poor documentation / lack of support → low adoption
- Start small, measure, iterate based on real usage
- Treat platform as product: product manager + developer support rota

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

- **CI/CD:** Automate build, test, security, and deploy
- **IDP:** Exposed as templates or starter kits
- **Platform Engineering:** Encapsulate policies and tooling


---

### Trail mix for the silver path

tbc

---

### TEAM SIZING

<img src="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?q=80&w=1400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" alt="Team sizing" width="800"/>

---

### TEAM SIZING

- < 30 devs: No dedicated platform org usually — 1–2 infra/DevOps engineers embedded in teams
- ~30–100 devs: 2–6 people focused on platform features + templates (part-time or small team)
- 100–500 devs: 6–20 FTEs running IDP, pipelines, service catalog, observability
- 500+ devs: Platform becomes a full product org (20+), with SLAs, PMs, SREs, UX

---

### Platform Capabilities

Capability domains to consider when building platforms for cloud-native computing:

- Web portals for observing and provisioning products and capabilities
- APIs (and CLIs) for automatically provisioning products and capabilities
- “Golden path” templates and docs enabling optimal use of capabilities in products
- Automation for building and testing services and products
- Automation for delivering and verifying services and products
- Development environments such as hosted IDEs and remote connection tools
- Observability for services and products using instrumentation and dashboards, including observation of functionality, performance and costs

(https://tag-app-delivery.cncf.io/whitepapers/platforms/)

---

### Platform Capabilities

Capability domains to consider when building platforms for cloud-native computing:

- Infrastructure services including compute runtimes, programmable networks, and block and volume storage
- Data services including databases, caches, and object stores
- Messaging and event services including brokers, queues, and event fabrics
- Identity and secret management services such as service and user identity and authorization, certificate and key issuance, and static secret storage
- Security services including static analysis of code and artifacts, runtime analysis, and policy enforcement
- Artifact storage including storage of container image and language-specific packages, custom binaries and libraries, and source code

(https://tag-app-delivery.cncf.io/whitepapers/platforms/)

---


### PLATFORM CAPABILITIES

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/platform-capabilities.png" alt="Alt Text" width="700"/>

(https://tag-app-delivery.cncf.io/whitepapers/platforms/)

---

### CNCF Platform Maturity Model

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/cncf-maturity-model.png" alt="Alt Text" width="700"/>                                                                    |

---

#### EXAMPLE: CNCF Platform Maturity Model: Investment

**Level 1, Provisional** — Voluntary or temporary Characteristics “Hit” or “tiger” teams short lived and not assigned nor granted the time to provide long term planning and support. 
Example: Improvements to a CI/CD considered only a ”side effort”

**Level 2, Operationalized** — Dedicated team Characteristics team is made up of generalists backlog ranges several technologies first to fill the gap 
Example: Central team tasked with reducing the build time of applications

**Level 3, Scalable** — As product Characteristics staff includes product management and UX Designer has a roadmap features are tested end-to-end
Example: Data derived from platform usage metrics is used to make informed decisions

**Level 4, Optimizing** — Enabled ecosystem Characteristics priority to enable specialists to extend the platform centralized specialists act through the platform
Example: Marketing works with platform builders to introduce consistent user tracking in order to attribute marketing efforts to product outcomes


---

### /DEV-EX

<img src="https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fi%2Fbeozmmi208ae3ye2dr3v.jpg" alt="Alt Text" width="500"/>

- Developer Experience = creating an environment in which a developer can do their best work
- Good DevEx = fewer frustrations and more productivity
- leading to faster delivery and better software quality

---

### /DEV-EX

“A means for capturing how developers think and feel about their activities within their working environments.”

(F. Fagerholm & J. Münch)

---



### /MULTICLOUD

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/multicloud.jpeg" alt="Alt Text" width="700"/>

- ☁️ Balance cost, performance & availability
- 🎛️ Unified control plane across clouds
- 📡 Cloud-agnostic CI/CD and GitOps

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

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/devops-idp.png" alt="Alt Text" width="700"/>


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
#### /BUILD

**CI/CD Pipeline (GitLab CI, GitHub Actions)**

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

# /PORT

---

### / PORT

<img src="https://qconsf.com/sites/qcon_sf/files/SPONSOR_LOGOS/port%20logo%20no%20bg.png" alt="Alt Text" width="700"/>

- SaaS platform for building Internal Developer Portals (IDPs)
- Connect GitOps, CI/CD, K8s, Terraform, and more
- A low-code, metadata-driven platform
- Designed for building customizable Internal Developer Portals (IDPs)

---

### /Use Cases

- Spin up new microservices with golden templates
- Automate environment provisioning
- Enforce compliance with scorecards
- Visualize K8s deployments and ownership
- Centralize developer onboarding

---

### /GITHUBS IDP?


---

### 🚀 /WHY GITHUB IS USING PORT

> One platform to answer key operational questions:

- 📍 **Where is my service running?**
- 🔁 **Which services will be impacted by my features?**
- ⚠️ **Which SLOs are not being met by my team?**
- 👤 **Who owns a service?**
- 🧾 **Who made the last change in production?**

Port centralizes this data — giving teams **clarity, ownership, and impact awareness** across the software lifecycle.

---

### /GITHUB INTEGRATION


- 🧭 Build a catalog of services from GitHub repos automatically
- 🔁 Create golden paths that use GitHub Actions to scaffold new services


---

### 📦 /Central Source of Truth

- ✅ No more switching between tools
- 🗂️ Consolidated software catalog
- 🔗 Easy access to dependencies & metadata

---

### 📦 /Graph View

- provides an interactive, visual map of all your software catalog entities and their relationships.
- It's like a live architectural diagram — automatically generated from the catalog.

---

### /Core Concepts in Port

- **Blueprints**: Define schemas (e.g., service, environment)
- **Software Catalog**: Metadata-rich inventory of resources
- **Scorecards**: Maturity, reliability & security evaluations
- **Automations**: Self-service workflows triggered by events

---

### /Example: Create a New Service

- 🧩 Blueprint: `service`
-  🖥 Form: Choose language, repo, infra
- ⚙️ Automation: Scaffold code, set up CI, register in catalog

- 🎯 Developer gets a ready-to-use repo and pipeline in minutes

---
### /Tracking Developer Adoption

- ✔️ Service creation events
- ✔️ Workflow usage metrics
- ✔️ Scorecard completion
- ✔️ Catalog contribution

Use these to **measure value and improve platform fit**


{{% /section %}}
