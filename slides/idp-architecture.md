## Architecture Vision

**Backstage is not the platform — it is the control plane of the platform.**

* Enables self-service
* Enforces policy
* Orchestrates automation
* Provides visibility & governance

---

#### High-level Goals of the Dev Architecture

| Goal | Description |
|------|-------------|
| 🔌 Fast Local Development | Hot-reload, instant feedback, minimal setup time |
| 🧪 Automated Testing | Unit, integration, e2e tests + ephemeral preview environments per PR |
| 🚀 Safe Promotion | Staged rollouts: Preview → Staging → Production with gates |
| 🔐 Secure Secrets | No secrets in code, runtime injection via Vault/K8s secrets |
| 📦 Repeatable Builds | Deterministic builds, pinned dependencies, immutable artifacts |

---

## OpenShift Developer Hub vs. Backstage

| | Backstage | RHDH |
|---|-----------|------|
| **Origin** | CNCF project (Spotify) | Red Hat enterprise distribution |
| **Relationship** | Upstream OSS framework | Built directly on Backstage |
| **Model** | Community-driven | Commercially supported |

{{% note %}}
RHDH is not a fork — it's built directly on Backstage with additional enterprise features and support.
{{% /note %}}

---

### RHDH: Pre-Integrated Ecosystem

RHDH ships with ready-to-use integrations optimized for the OpenShift/Red Hat ecosystem:

| Category | Integration |
|----------|-------------|
| 🔍 **Visualization** | Application Topology for Kubernetes |
| 🔧 **CI/CD** | Tekton Pipelines |
| 🚀 **GitOps** | Argo CD (OpenShift GitOps) |
| 📦 **Registry** | Quay container registry |
| 🌐 **Multi-Cluster** | Open Cluster Manager |
| 🔐 **Auth** | Keycloak authentication |

---

### Installation & Management

| Aspect | Backstage | RHDH |
|--------|-----------|------|
| **Deployment** | Manual setup | Kubernetes Operator / Helm |
| **Build Process** | Complex, DIY | Simplified, pre-built |
| **Dependencies** | Self-managed | Bundled & validated |
| **Updates** | Manual maintenance | Automated |
| **Plugin Loading** | Static (rebuild required) | Dynamic (hot-reload) |

{{% note %}}
RHDH eliminates the "undifferentiated heavy lifting" of deploying Backstage on Kubernetes.
{{% /note %}}

---
<!--

### Plugin Architecture Comparison

| | Backstage (Static) | RHDH (Dynamic) |
|---|-------------------|----------------|
| **Adding Plugins** | Rebuild app | Configure & reload |
| **Updates** | Redeploy required | Hot-reload capability |
| **Downtime** | Yes, for changes | Zero-downtime updates |
| **Flexibility** | Full control | Curated plugin set |

--- -->

### Decision Guide

| Choose **Backstage** when... | Choose **RHDH** when... |
|------------------------------|-------------------------|
| 🔧 Maximum flexibility | ⚡ Faster time-to-value |
| 👥 Resources to build/maintain | 🏢 OpenShift/Red Hat ecosystem |
| 🧩 Custom plugins needed | 🛡️ Enterprise support required |
| 🌐 Community-driven | 📦 Pre-integrated components |
| 🎯 Full platform control | 🔒 RBAC & compliance built-in |
| | 🚀 Lower operational overhead |

---

### IDP Team Collaboration Model

| Team | Responsibility |
|------|----------------|
| **Developer Teams** | Consume patterns, build applications & infrastructure |
| **Platform Teams** | Provide golden paths, centralized infra & collaboration tools |
| **Governance** | Enforce guard rails, compliance, reporting & contracts |

---
<!--
### Platform Teams Overview

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/platform-teams.png" alt="Platform Teams" width="1200"/>

--- -->

### Platform Team Sizing Guide

| Org Size | Platform Team | Focus |
|----------|---------------|-------|
| < 30 devs | 1–2 embedded engineers | Basic automation, shared tooling |
| 30–100 devs | 2–6 people (part-time/small team) | Templates, CI/CD standardization |
| 100–500 devs | 6–20 FTEs | Full IDP, pipelines, catalog, observability |
| 500+ devs | 20+ (full product org) | SLAs, PMs, SREs, UX, dedicated support |

---

## Target Architecture Overview

**Backstage** → **Automation** → **Infrastructure**

| Layer | What it does |
|-------|--------------|
| Control Plane | Backstage (UI, catalog, templates) |
| Execution | GitLab, Ansible, Terraform |
| Infrastructure | OpenShift, Azure |

---

#### Organizing Backstage as a Dev Project

| Aspect | Recommendation |
|--------|----------------|
| **Repository Structure** | Monorepo with `packages/app`, `packages/backend`, and `plugins/` directories |
| **Plugins** | Keep custom plugins in `plugins/` folder; publish shared ones to private registry |
| **Configuration** | Environment-specific configs: `app-config.yaml`, `app-config.production.yaml` |
| **Secrets** | Never commit secrets; use env vars or external secret management (Vault, K8s Secrets) |
| **Dependencies** | Pin versions in `package.json`; use lockfiles; update regularly |

---

### Build & Deploy Backstage

| Stage | Details |
|-------|---------|
| **Local Dev** | `yarn dev` for hot-reload; use `app-config.local.yaml` for overrides |
| **Build** | `yarn build` creates production bundle; `yarn build:backend --config ../../app-config.production.yaml` |
| **Container Image** | Multi-stage Dockerfile; separate build and runtime stages; minimize image size |
| **CI/CD Pipeline** | Lint → Test → Build → Push Image → Deploy to staging → Promote to prod |
| **Deployment** | Helm chart or Kubernetes manifests; GitOps with ArgoCD recommended |

---

### Plugins & Authentication Setup

| Topic | Approach |
|-------|----------|
| **Plugin Installation** | `yarn add @backstage/plugin-xyz` then register in `App.tsx` / `plugins.ts` |
| **Custom Plugins** | `yarn new --select plugin` to scaffold; develop in `plugins/` directory |
| **Plugin Versioning** | Match plugin versions to your Backstage version; check compatibility matrix |
| **Auth Providers** | Configure in `app-config.yaml` under `auth.providers` (GitHub, GitLab, Okta, Keycloak, etc.) |
| **Auth Flow** | Sign-in page → Provider OAuth → Token exchange → Session cookie |
| **RBAC** | Use permission framework; define policies in backend; integrate with identity provider groups |

---

### Backstage Runtime on OpenShift

| Component | Configuration |
|-----------|---------------|
| **Deployment** | `Deployment` or `DeploymentConfig`; 2+ replicas for HA |
| **Service** | ClusterIP service exposing port 7007 (backend) |
| **Route / Ingress** | OpenShift Route with TLS termination; configure `app.baseUrl` accordingly |
| **Database** | External PostgreSQL (recommended) or in-cluster; use `StatefulSet` for persistence |
| **ConfigMaps** | Mount `app-config.production.yaml`; use for non-sensitive configuration |
| **Secrets** | Store auth tokens, DB credentials, API keys; inject as env vars or volume mounts |
| **ServiceAccount** | Custom SA with RBAC for Kubernetes plugin to read cluster resources |
| **Resource Limits** | Set CPU/memory requests and limits; backend is memory-intensive |
| **Health Probes** | Liveness: `/healthcheck`, Readiness: `/healthcheck`; adjust timeouts for startup |

---

## Start With These Questions

| Question | Why It Matters |
|----------|----------------|
| Can you reduce feedback loops? | Faster iteration = happier developers |
| Where is cognitive load highest? | Target your platform investment |
| Which teams need the most support? | Prioritize high-impact improvements |
| What would great DX look like? | Define your north star |

---

### When to Invest in Platform Engineering

| Signal | Description |
|--------|-------------|
| 👥 Team Size | ~50 engineers OR rapid growth toward that number |
| 🔧 Infra Friction | Long onboarding, many infra tickets, inconsistent CI/CD |
| 🔁 Duplication | Many similar services (microservices) with duplicated build/deploy logic |
| 🛡️ Governance | Need for self-service and audited defaults (security, compliance) |

---

### Pitfalls to Avoid

| Pitfall | How to Prevent |
|---------|----------------|
| 🔒 "Golden Cage" | Don't be too rigid — allow escape hatches |
| 🏗️ Over-engineering | Start with real needs, not hypothetical ones |
| 📚 Poor Docs | No docs = no adoption — invest in onboarding |
| 🎯 Big Bang | Start small, measure, iterate based on usage |


---

### Architecture Evolution Overview

| Phase | Name | Focus |
|-------|------|-------|
| 1 | Initial Adoption | Get started |
| 2 | Controlled Self-Service | Automate |
| 3 | Policy-Driven | Govern |
| 4 | Platform at Scale | Optimize |

---

### Phase 1 — Initial Adoption

| Aspect | Details |
|--------|---------|
| **Goal** | Get Backstage running as UI & catalog |
| **Characteristics** | Manual approvals, direct API calls |
| **Tools** | Backstage, GitLab, OpenShift |
| **Risks** | Tight coupling, limited governance |

---

### Phase 2 — Controlled Self-Service

| Aspect | Details |
|--------|---------|
| **Goal** | Enable repeatable, automated workflows |
| **Characteristics** | Software Templates, CI/CD-driven, centralized identity |
| **Tools** | Backstage Templates, GitLab CI/CD, Keycloak |
| **Outcome** | Repeatability, reduced manual work |

---

### Phase 3 — Policy-Driven Platform

| Aspect | Details |
|--------|---------|
| **Goal** | Enforce governance without blocking teams |
| **Characteristics** | Policy as Code, async workflows, clear ownership |
| **Tools** | OPA / Gatekeeper, Kyverno, Event Bus |
| **Outcome** | Safe autonomy, compliance by default |

---

### Phase 4 — Platform at Scale

| Aspect | Details |
|--------|---------|
| **Goal** | Sustainable, cost-aware platform operations |
| **Characteristics** | Observability-first, FinOps, plugin lifecycle |
| **Tools** | Prometheus / Grafana, Cost Management APIs, Feature Flags |
| **Outcome** | Predictable, scalable platform |

---


### Tactics - How to promote Backstage internally:

- **"Lunch & Learns" & seminars**
  - show, for example, how to build a plugin from scratch
- **Hack days**
  - fun way to get people into plugin development
- **Show & tell meetings**
  - quarterly meetings where anyone working on Backstage is invited to present their work
- **Pro-actively identify new plugins**
  - reach out to teams that own internal user interfaces or platforms that you think would make sense to consolidate into Backstage

---

## Lessons Learned

- **Provide Templates for Documentation**
  - Ensure consistent documentation and clear documentation structures
  - Reduce effort for developers and faster documentation creation
  - Increase completeness and clarity
- **Support Linting**
  - Increase the quality
  - Catch errors early
  - Provide a reusable jobs for CI/CD
- **Provide Silver Path**
  - Offer alternative paths when golden path doesn't fit
  - Document trade-offs and when to deviate
  - Enable flexibility without chaos

---

## Key Takeaways

* Backstage is a **control plane**, not a workflow engine
* Policies, events, and observability are mandatory at scale
* Architecture must evolve incrementally
* Governance enables, not blocks, self-service

<!-- ---

## Final Message

**A successful internal developer platform is:
Self-service by default, governed by design, and observable end-to-end.** -->
