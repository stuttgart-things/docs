## Platform Foundations

<img src="https://media.licdn.com/dms/image/v2/D4D22AQHolX5UwNFzPg/feedshare-shrink_800/B4DZTyTdDSG8Ag-/0/1739231974056?e=2147483647&v=beta&t=0V2HW-dJHygYyHMp4Kv-TbTgrue10vzZL2TYzzZmv_k" alt="Alt Text" width="350"/>

- Platform Engineering is an evolution of DevOps

---

### MULTICLOUD

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/multicloud.jpeg" alt="Alt Text" width="700"/>

- ☁️ Balance cost, performance & availability
- 🎛️ Unified control plane across clouds
- 📡 Cloud-agnostic CI/CD and GitOps

---

### 🔄 GITOPS

<img src="https://cdn.prod.website-files.com/63c8f7191194d2a0cf4f630e/67951e7770966bf72c93aa96_Screenshot%202025-01-25%20at%2018.25.04.png" alt="Alt Text" width="500"/>

- modern way to do **Continuous Deployment**, using **Git as the single source of truth** for infra and apps

---

### 🔄 GITOPS

- 📜 **Declarative Infrastructure** — everything is defined in YAML
- 🔗 **Git as the Source of Truth** — no more config drift
- 🤖 **Automated Sync** — tools like Argo CD & Flux keep clusters aligned
- 🕵️ **Audit & Rollback** — powered by Git history and versioning

> 🚀 **Git push = production change**, with full visibility and control
---

<!-- ### 🛠️ /GitOps Tools

- **Flux** or **Argo CD** for automated syncing
- **Kustomize** or **Helm** for templating
- **Git** for storing desired state

🧠 Changes in Git → Automatically applied to clusters -->
<!--
--- -->

### /Quick Poll

> 🔄 What’s your **go-to GitOps tool** for managing Kubernetes and infrastructure?

- 🚀 **Argo CD** — Declarative, visual, Git-native deployments
- 🌀 **Flux** — GitOps toolkit built for flexibility and composability
- 🔧 **Jenkins X**, **Fleet**, or other custom GitOps solutions
- ❓ Still exploring — curious what all the hype is about?

---

### 🏗️ Platform Engineering

<img src="https://pbs.twimg.com/media/FnabgQxXwAEDZz6.jpg" alt="Alt Text" width="600"/>

---

### 🏗️ Platform Engineering

| Principle | Description |
|-----------|-------------|
| 🧰 **Self-Service Platforms** | Abstract complexity behind easy-to-use interfaces |
| 🚀 **Developer Velocity** | Empower teams to ship faster with less friction |
| 🎯 **Focus on Value** | Remove infrastructure worries from day-to-day work |
| 🔄 **Standardization** | Consistent tooling, patterns, and best practices |

---

### 🏗️ Platform Engineering: The Shift

| Traditional DevOps | Platform Engineering |
|--------------------|----------------------|
| 🎫 Ticket-based requests | 🛒 Self-service portal |
| 🔧 Manual provisioning | ⚡ Automated workflows |
| 📚 Tribal knowledge | 📖 Documented golden paths |
| 🏃 Reactive support | 🎯 Proactive enablement |
| 👤 Individual expertise | 🧩 Productized capabilities |

> **"You build it, you run it"** → **"You build it, we help you run it better"**

---

### 🎯 What is an Internal Developer Platform (IDP)?

<img src="https://i.ytimg.com/vi/U9zoxETp7XY/maxresdefault.jpg" alt="Alt Text" width="600"/>

---

### 🎯 What is an Internal Developer Platform (IDP)?


**An IDP is a self-service layer that abstracts infrastructure complexity**

| Aspect | Description |
|--------|-------------|
| 🎯 **Purpose** | Reduce cognitive load, accelerate delivery, standardize best practices |
| 🧩 **Components** | Service catalog, golden paths, automation workflows, documentation |
| 👥 **Users** | Developers consume platform capabilities without deep infrastructure knowledge |

> **"A PaaS built by your platform team, for your organization's needs"**

---

### 🏢 Popular IDP Solutions

| Solution | Type | Key Features |
|----------|------|--------------|
| 🎭 **Backstage** | Open Source | Service catalog, TechDocs, plugin ecosystem, Spotify-originated |
| 🌊 **Port** | SaaS | Low-code portal builder, scorecards, automations, integrations |
| 🔧 **CLI-based** | Custom | Platform CLI tools (e.g., `platform create service`, `platform deploy`) |

<!-- **Backstage** — Rich plugin ecosystem, highly customizable, self-hosted
**Port** — Quick setup, managed service, visual workflow builder
**CLI Tools** — Scriptable, integrates with existing workflows, developer-friendly -->

---

### 🔌 Crossplane: IAC, the Kubernetes Way

**Crossplane extends Kubernetes to manage cloud infrastructure**

| Concept | Description |
|---------|-------------|
| 🎛️ **Control Plane** | Uses Kubernetes API to provision & manage cloud resources |
| 📦 **Providers** | Support AWS, Azure, GCP, and 80+ cloud services |
| 🧩 **Compositions** | Reusable infrastructure blueprints (like Terraform modules, but declarative) |
| 🔄 **GitOps Native** | Declare infrastructure in Git, let Crossplane reconcile state |

> **"kubectl apply" your entire infrastructure — databases, networks, compute**

---

### 🚀 Crossplane in an IDP Context

**How Crossplane powers self-service infrastructure:**

| Use Case | How It Works |
|----------|--------------|
| 🗄️ **Database Provisioning** | Developer requests PostgreSQL → Crossplane creates RDS instance |
| 🌐 **Environment Creation** | Service template triggers Crossplane composition for full stack |
| 📊 **Resource Discovery** | IDP catalog shows all Crossplane-managed resources with ownership |

**Integration Example:**
- Backstage template → triggers GitHub Action → applies Crossplane manifests → provisions cloud resources

> **Crossplane = Infrastructure API for your IDP**

---

### /Quick Poll

> ⚙️ Have you ever worked with **Crossplane**?

- 🚀 **Yes, using it in production** — managing cloud resources the Kubernetes way!
- 🧪 **Yes, tried it in dev/test** — exploring the possibilities
- 📚 **Heard of it, planning to try** — on the roadmap
- 🤔 **Never heard of Crossplane** — what does it do?
- 🛠️ **Using Terraform/other IaC instead** — sticking with what works

---

<!-- ### 🏗️ Platform Engineering

"...  is the discipline of designing and building toolchains and workflows that enable **self-service** capabilities for software engineering organizations in the cloud-native era. Platform engineers provide an integrated product most often referred to as an “ **Internal Developer Platform**” covering the operational necessities of the entire lifecycle of an application."

(- Humanitec)

--- -->

### WHAT ARE GOLDEN PATHS

<!-- <img src="https://miro.medium.com/v2/resize:fit:1200/0*BEkTUO3XM3kaQFUl" alt="When to introduce" width="450"/> -->

| Aspect | Description |
|--------|-------------|
| 📋 Definition | Opinionated, well-documented, supported end-to-end workflows teams are encouraged to use |
| 🧩 Examples | Standardized CI/CD pipeline templates, service scaffolding, infra provisioning blueprints |
| 🎯 Goal | Let teams ship safely and fast using trusted defaults, keep flexibility via "escape hatches" |

---

### When to Introduce Golden Paths

| Signal | Description |
|--------|-------------|
| 👥 Team Scale | Multiple teams (≈10+) doing similar CI/CD work |
| 🔧 Pipeline Pain | Repeated pipeline maintenance and breakage across teams |
| ⏱️ Slow Onboarding | Onboarding takes weeks, not days |
| 🧠 Cognitive Load | Desire to reduce complexity and increase platform ROI |
| ⚠️ Too Early If | Every service is unique and experimentation speed matters more than consistency |

---
<!--
### Why Golden Paths?

| Principle | Benefit |
|-----------|---------|
| 🧠 Reduce Cognitive Load | Don't overwhelm devs — focus on what matters |
| 🎯 Features over Tooling | Let developers ship, not configure |
| 🤝 Knowledge Sharing | Best practices flow in all directions |
| ✅ Perceived Value | Tools must feel helpful, not imposed |

> **"Love your Developers, not your Tools."**

--- -->

<!-- ### Golden Path Checklist: Build

| Step | Action |
|------|--------|
| 🚀 Service Types | Identify 1–3 common types (web service, job, library) |
| 🧩 Templates | Create minimal, documented pipeline template per type |
| 📦 Scaffolding | Provide repo template (CLI or GitHub template) |
| ⚙️ Onboarding | One command → dev environment + run tests |

--- -->

### Golden Path Checklist: Operate & Improve

| Step | Action |
|------|--------|
| 📊 Observability | Bake in metrics, alerting, tracing by default |
| 🛡️ Security | Add SAST, secrets scanning as default steps |
| 🔧 Flexibility | Offer escape hatches and extension points |
| 📈 Measure | Track TTFD, ticket volume, failure rate, dev satisfaction |

---

<!-- ### PILOT PLAN (3–6 WEEKS)

- Pick 1 service type + 1 friendly team (pilot).
- Build a minimal Golden Path: repo template, CI pipeline, infra blueprint.
- Document “how to” and run live onboarding with the team.
- Measure baseline metrics (time to onboard, tickets, deploy cadence).
- Iterate for 2 sprints, collect feedback, add escape hatches.
- If successful, expand to 3–5 teams and formalize templates.

--- -->

<!--
### PITFALLS & ESCAPE-HATCHES

<img src="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?q=80&w=1400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" alt="Pitfalls" width="700"/>

--- -->


<!-- ## 🚀 What Are Golden Pipelines?

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

--- -->

<!-- ## 🧱 Golden Pipelines in Practice

- **CI/CD:** Automate build, test, security, and deploy
- **IDP:** Exposed as templates or starter kits
- **Platform Engineering:** Encapsulate policies and tooling


--- -->

### Silver Path

> A flexible alternative to the Golden Path — more freedom, less hand-holding

| Aspect | Golden Path | Silver Path |
|--------|-------------|-------------|
| 🛤️ Structure | Full end-to-end workflow | Pick & choose components |
| 🤝 Support | Guaranteed, first-class | Best effort |
| 🎛️ Flexibility | Opinionated defaults | Custom decisions allowed |
| 👥 Use Case | Most teams | Special requirements |

---

### Silver Path Examples

| Example | Description |
|---------|-------------|
| 🧩 Partial Adoption | Use only Terraform modules or logging, skip full template |
| 🔓 Compliance Opt-out | Disable specific policy checks (with approval) |
| 🔀 Custom Pipeline | Own CI/CD with platform observability integration |
| 📝 CODEOWNERS Override | Adjust reference configs via PR approval |

> **Transition path**: Silver Path → Golden Path as needs stabilize

---

<!-- ### EXAMPLE TEAM/COMPANY SIZES

- **Small org ~50 devs** → small platform team (2–4 FTE) focusing on on-boarding & pipeline templates

- **Mid-size ~200 devs** → platform team (6–10 FTE), centralized pipelines, service catalog, self-service infra

- **Enterprise 1000+ devs** → larger platform org (20+ FTE), strong IDP, SLOs, cross-team platform product managers

- **Typical benefits reported:** faster on-board, less duplicated work, measurable dev-hours saved

--- -->

<!-- ### TEAM SIZING

<img src="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?q=80&w=1400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" alt="Team sizing" width="800"/>

---

### TEAM SIZING

- < 30 devs: No dedicated platform org usually — 1–2 infra/DevOps engineers embedded in teams
- ~30–100 devs: 2–6 people focused on platform features + templates (part-time or small team)
- 100–500 devs: 6–20 FTEs running IDP, pipelines, service catalog, observability
- 500+ devs: Platform becomes a full product org (20+), with SLAs, PMs, SREs, UX

--- -->


#### 🏗️ Platform Team Responsibilities

| Area | What They Do |
|------|--------------|
| 🛠️ **Toolchain** | Build and maintain CI/CD, IaC, and observability stack |
| 📋 **Templates** | Create golden paths, starter kits, and scaffolding |
| 🔐 **Guardrails** | Implement security, compliance, and cost policies |
| 📊 **Metrics** | Track DORA, adoption, and developer satisfaction |
| 🤝 **Enablement** | Documentation, training, and developer support |

> Platform teams are **product teams** — developers are their customers

---

### DEV-EX

<img src="https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fi%2Fbeozmmi208ae3ye2dr3v.jpg" alt="Alt Text" width="500"/>

- Developer Experience = creating an environment in which a developer can do their best work
- Good DevEx = fewer frustrations and more productivity
- leading to faster delivery and better software quality

---

### Platform Capabilities: Developer Experience

| Category | Capabilities |
|----------|--------------|
| 🌐 Portals & APIs | Web UI + CLI for provisioning and observing |
| 🛤️ Golden Paths | Templates, docs, and workflows for fast onboarding |
| 🔄 CI/CD | Automation for build, test, deliver, and verify |
| 💻 Dev Environments | Hosted IDEs, remote dev tools |
| 📊 Observability | Metrics, logs, traces, cost dashboards |

---

### Platform Capabilities: Infrastructure

| Category | Examples |
|----------|----------|
| 🖥️ Compute & Network | Runtimes, programmable networks, storage |
| 🗄️ Data Services | Databases, caches, object stores |
| 📨 Messaging | Brokers, queues, event fabrics |
| 🔐 Identity & Secrets | Auth, certificates, secret storage |
| 🛡️ Security | SAST, runtime analysis, policy enforcement |
| 📦 Artifacts | Container images, packages, source code |

> Source: [CNCF Platforms Whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

---
<!--
### CNCF Platform Capabilities: Developer Experience

| Capability | Description | CNCF/CDF Examples |
|------------|-------------|-------------------|
| 🌐 Web Portals | Publish docs, service catalogs, project templates | Backstage, Skooner, Ortelius |
| 🔌 APIs | Auto-create, update, delete, observe capabilities | Kubernetes, Crossplane, Helm |
| 🛤️ Golden Paths | Templated code + capabilities for rapid dev | ArtifactHub |

---

### CNCF Platform Capabilities: Developer Experience

| Capability | Description | CNCF/CDF Examples |
|------------|-------------|-------------------|
| 🔄 Build & Test | Automate build and test of products/services | Tekton, Jenkins, ko |
| 🚀 Delivery | Automate and observe delivery of services | Argo, Flux, Flagger |
| 💻 Dev Environments | Enable R&D of applications and systems | Devfile, Telepresence, DevSpace |
| 📊 Observability | Instrument, gather, analyze telemetry | OpenTelemetry, Prometheus, Grafana | -->

---

### CNCF Platform Capabilities: Infrastructure

| Capability | Description | CNCF/CDF Examples |
|------------|-------------|-------------------|
| 🖥️ Infrastructure | Run code, connect components, persist data | Kubernetes, Kubevirt, Knative, Istio, Cilium, Envoy |
| 🗄️ Data Services | Persist structured data for applications | TiKV, Vitess, SchemaHero |
| 📨 Messaging | Enable async communication between apps | Strimzi, NATS, gRPC, Knative, Dapr |
| 🔐 Identity & Secrets | Locators, secrets, service identity | Keycloak, Dex, External Secrets, SPIFFE/SPIRE, cert-manager |

---

### CNCF Platform Capabilities: Security & Storage

| Capability | Description | CNCF/CDF Examples |
|------------|-------------|-------------------|
| 🛡️ Security | Runtime analysis, vulnerability scanning, policy enforcement | Falco, In-toto, KubeArmor, OPA, Kyverno, Cloud Custodian |
| 📦 Artifact Storage | Store, publish, secure built artifacts | ArtifactHub, Harbor, Distribution, Porter |

> Source: [CNCF Platforms Whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)

---

### CNCF Platform Maturity Model

| Level | Name | Focus |
|-------|------|-------|
| 1️⃣ | Build | Baseline cloud-native in pre-production (not a lab/POC) |
| 2️⃣ | Operate | Foundation established, moving to production |
| 3️⃣ | Scale | Growing competency, defining processes for scale |
| 4️⃣ | Improve | Enhancing security, policy, and governance |
| 5️⃣ | Adapt | Revisiting decisions, optimizing apps and infra |

> Source: [CNCF Maturity Model](https://maturitymodel.cncf.io/)
---
<!--

### CNCF Platform Maturity Model

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/cncf-maturity-model.png" alt="Alt Text" width="1000"/>

> Source: [CNCF Platform Engineering Maturity Model](https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model)

---

### Platform Investment Maturity

| Level | Name | Characteristics | Example |
|-------|------|-----------------|---------|
| 1️⃣ | Provisional | Voluntary "tiger teams", short-lived, no long-term planning | CI/CD improvements as a "side effort" |
| 2️⃣ | Operational- ized | Dedicated generalist team, fills gaps across technologies | Central team reducing build times |

> Source: [CNCF Maturity Model](https://maturitymodel.cncf.io/)

---

### Platform Investment Maturity

| Level | Name | Characteristics | Example |
|-------|------|-----------------|---------|
| 3️⃣ | Scalable | Product mindset: PM, UX, roadmap, end-to-end testing | Decisions driven by platform usage metrics |
| 4️⃣ | Optimizing | Enabled ecosystem, specialists extend the platform | Marketing integrates user tracking via platform |

> Source: [CNCF Maturity Model](https://maturitymodel.cncf.io/)

--- -->

<!--
### /DEV-EX

“A means for capturing how developers think and feel about their activities within their working environments.”

(F. Fagerholm & J. Münch)

--- -->



<!-- ### /IDP

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/idps.png" alt="Alt Text" width="700"/>

( - Amazon Web Services)

--- -->

### IDP

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/abstraction.jpeg" alt="Alt Text" width="700"/>

---

### IDP

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
<!--
### 🚀 DORA Metrics


- **Deployment Frequency**
- **Lead Time for Changes**
- **Change Failure Rate**
- **Mean Time to Recovery (MTTR)**

--- -->

### 📈 IDPs Make DORA Metrics Actionable

DORA (DevOps Research and Assessment) metrics measure software delivery performance:


| Metric | How an IDP Helps |
|--------|------------------|
| 📦 Deployment Frequency | Self-service deploys, GitOps integration |
| ⏱️ Lead Time for Changes | Track from commit → production |
| ❌ Change Failure Rate | Show failed rollouts, incident links |
| 🛠️ MTTR | Connect services to runbooks, SLOs, and ownership |

---

### ⚙️ Core Features

<img src="https://pradeepl.com/blog/internal-developer-portals-spotify-backstage/images/Backstage-Templates.png" alt="Alt Text" width="1000"/>

- 🛠️ Self-service deployment & environment provisioning
- 🔍 Visibility into logs, metrics, and deployments
- 🚦 Policy enforcement (e.g. security, cost, compliance)
- 📦 Template catalogs for fast onboarding

---

### 🚀 Key IDP Benefits

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
### 📈 Measuring Adoption

> Adoption shows whether developers trust, use, and benefit from the platform

- 🔁 **DAU/WAU/MAU**: Daily / Weekly / Monthly active users
- 🚀 **Self-service actions**: Number of created services, environments, deployments
- 🔍 **Time to First Deploy (TTFD)**: How fast a dev goes from repo to running app
- 💬 **Feedback loops**: Surveys, interviews, support tickets

---

### /Quick Poll

> 🎯 Have you ever worked with an **Internal Developer Portal (IDP)**?

- 🎭 **Yes, with Backstage** — love the plugin ecosystem!
- 🧱 **Yes, with another tool** — like Port, Cortex, or OpsLevel
- 🛠️ **We built our own custom IDP** — DIY all the way
- 🧩 **Heard of IDPs, but not used one yet**
- 🤷 **What’s an IDP?** — sounds fancy! -->


---

# DevOps

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/devops-loop.png" alt="Alt Text" width="700"/>

---


### DevOps --> IDP

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/devops-idp.png" alt="Alt Text" width="700"/>


---

#### /PLAN

**Project planning (Jira, Confluence, GitHub Projects)**

- **Scorecards / quality metrics:**
  - Show early on how mature or “production-ready” a service or module is – e.g., technical condition, maintainability, security.
- **Software/service catalog:**
  - Map of all available services, libraries, infrastructure modules, including ownership, status, dependencies. Developers can see early on what already exists.
- **Documentation hub:**
  - Cataloging of projects, teams, components, and technologies.

---

#### /CODE

**Version control (GitHub/GitLab, IDEs)**

- **Embedded governance and policies:**
  - Security and architecture requirements are automatically visible and enforced when a project is created.
- **Integration with version control/CI tools:**
  - The portal displays builds, pull requests, test status, etc., so that development is integrated into the overview.
- **Self-service actions/scaffolding:**
  - Predefined templates (Golden Paths) and automations

---

#### /BUILD

**CI/CD Pipeline (GitLab CI, GitHub Actions)**

- **Automated workflows / Golden Paths:**
  - Standardized build pipelines as part of a self-service workflow in the portal.
- **Integrations with build/CI systems:**
  - Portal can visualize build results/status, making builds transparent.

---

#### /TEST

**Automated testing (JUnit, Selenium)**

- **Dashboard/integrations with testing tools:**
  - Test results and quality made visible in the context of services.
- **Scorecards/quality metrics:**
  - Portal shows test coverage, security gaps, maintainability—development can see early on whether quality is up to standard.

---

#### /RELEASE

**Release-Management Tools (Spinnaker, Octopus Deploy)**

- **Workflows / Automation:**
  - Automated approvals, rollbacks, and canary releases integrated into the portal.

---

#### /DEPLOY

**Deployment Automation (Terraform, Ansible, Helm, ArgoCD)**

- **Self-service deployment:**
  - Triggering deployment, provisioning environments
- **Deployment catalog:**
  - Catalog & ownership: Services that are deployed are listed in the catalog with the responsible parties so that deployment is clearly assigned.

---

#### /OPERATE

**Configuration management (Chef, Puppet)**

- **Scorecards / service maturity levels:**
  - Ongoing evaluation of a service in operation – e.g., stability, MTTR, costs.
- **Governance, compliance, FinOps:**
  - Access control, audit trails, cost overview – operation in compliance with specifications.

---

#### /MONITOR

**Monitoring tools (Prometheus, ELK)**

- **Status monitoring:**
  - Integrations with observability/monitoring tools: logs, metrics, traces displayed together in the portal.

---

### Metrics to Track

| Category | Metrics |
|----------|---------|
| 🚀 DORA | Deployment Frequency, Lead Time, MTTR, Change Failure Rate |
| ⏱️ Onboarding | Time to first green build, Time to first deploy |
| 🎫 Support Load | Infra/platform tickets per sprint |
| 😊 Satisfaction | Developer NPS, platform feedback surveys |
| 💰 Cost | Infra cost per service, CI minutes saved, engineer hours saved |

<!-- # /PORT

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

Use these to **measure value and improve platform fit** -->
