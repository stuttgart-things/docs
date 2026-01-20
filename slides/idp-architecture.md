### Backstage Platform Architecture

---

## Architecture Vision

**Backstage is not the platform — it is the control plane of the platform.**

* Enables self-service
* Enforces policy
* Orchestrates automation
* Provides visibility & governance

Everything else **executes**, **enforces**, **observes**, or **audits**.

---

### When to Invest in Platform Engineering

<!-- <img src="https://images.unsplash.com/photo-1504384308090-c894fdcc538d?q=80&w=1400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" alt="When it pays" width="400"/> -->

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

> **Mindset shift:** Treat platform as a product — assign a PM + support rota

---

### PLATFORM TEAMS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/platform-teams.png" alt="Alt Text" width="1200"/>

---

### TEAM SIZING

- < 30 devs: No dedicated platform org usually — 1–2 infra/DevOps engineers embedded in teams
- ~30–100 devs: 2–6 people focused on platform features + templates (part-time or small team)
- 100–500 devs: 6–20 FTEs running IDP, pipelines, service catalog, observability
- 500+ devs: Platform becomes a full product org (20+), with SLAs, PMs, SREs, UX

---

## Helpful Questions

- Can you reduce feedback loops? (pair /peer programming)
- Where is cognitive load highest?
- Which teams need support?
- What would great DX look like?

---

## High-level Goals of the Dev Architecture

| Goal | Description |
|------|-------------|
| 🔌 Fast Local Development | Hot-reload, instant feedback, minimal setup time |
| 🔁 App/Plugin Separation | Independent versioning, clear boundaries, pluggable architecture |
| 🧪 Automated Testing | Unit, integration, e2e tests + ephemeral preview environments per PR |
| 🚀 Safe Promotion | Staged rollouts: Preview → Staging → Production with gates |
| 🔐 Secure Secrets | No secrets in code, runtime injection via Vault/K8s secrets |
| 📦 Repeatable Builds | Deterministic builds, pinned dependencies, immutable artifacts |

---

## OpenShift Developer Hub vs. Backstage

---

### What's the Relationship?

| | Backstage | RHDH |
|---|-----------|------|
| **Origin** | CNCF project (Spotify) | Red Hat enterprise distribution |
| **Relationship** | Upstream OSS framework | Built directly on Backstage |
| **Model** | Community-driven | Commercially supported |

> **Think of it like:**
> - Kubernetes → OpenShift
> - Linux Kernel → RHEL

{{% note %}}
RHDH is not a fork — it's built directly on Backstage with additional enterprise features and support.
{{% /note %}}

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

### Plugin Architecture Comparison

| | Backstage (Static) | RHDH (Dynamic) |
|---|-------------------|----------------|
| **Adding Plugins** | Rebuild app | Configure & reload |
| **Updates** | Redeploy required | Hot-reload capability |
| **Downtime** | Yes, for changes | Zero-downtime updates |
| **Flexibility** | Full control | Curated plugin set |

---

### Golden Path Templates

RHDH provides **pre-defined, Red Hat-validated templates** that accelerate adoption:

| Benefit | Description |
|---------|-------------|
| 📐 **Pre-architected** | Proven patterns out of the box |
| ⚡ **Optimized** | OpenShift-native workflows |
| 🔒 **Secure** | Security best practices built-in |
| 🚀 **Fast** | Reduced time-to-production |

---

### Decision Guide

| Choose **Backstage** when... | Choose **RHDH** when... |
|------------------------------|-------------------------|
| ✅ Maximum flexibility needed | ✅ Faster time-to-value required |
| ✅ Resources to build & maintain | ✅ Already invested in OpenShift/Red Hat |
| ✅ Plugins outside Red Hat ecosystem | ✅ Enterprise support & SLAs needed |
| ✅ Community-driven development | ✅ Want curated, validated plugins |
| ✅ Full control over the platform | ✅ Simplified RBAC & compliance |
| | ✅ Less operational overhead |

---

## Logical Architecture Overview

```
┌────────────────────────────────────────────────────────────┐
│                       DEVELOPERS                           │
│                                                            │
│  ┌─────────────────┐      ┌─────────────────────────────┐  │
│  │   Local Dev     │      │   IDE (VSCode)              │  │
│  │   (yarn dev)    │◄────►│   - Backstage monorepo      │  │
│  │                 │      │   - Plugin development      │  │
│  └────────┬────────┘      │   - API contracts           │  │
│           │               └─────────────────────────────┘  │
└───────────┼────────────────────────────────────────────────┘
            │ git push
            ▼
┌────────────────────────────────────────────────────────────┐
│                    SOURCE CONTROL                          │
│                                                            │
│   GitHub / GitLab                                          │
│   ├── backstage-app repo                                   │
│   ├── plugins (monorepo or multi-repo)                     │
│   └── catalog-info.yaml                                    │
└───────────┬────────────────────────────────────────────────┘
            │ webhook trigger
            ▼
┌────────────────────────────────────────────────────────────┐
│                   CI/CD PIPELINE                           │
│                                                            │
│   GitHub Actions / GitLab CI                               │
│   ├── Lint & Test                                          │
│   ├── Build Backstage app                                  │
│   ├── Build container image                                │
│   ├── Publish artifacts (registry)                         │
│   └── Deploy to preview / staging                          │
└───────────┬────────────────────────────────────────────────┘
            │ deploy
            ▼
┌────────────────────────────────────────────────────────────┐
│                RUNTIME ENVIRONMENTS (K8s)                  │
│                                                            │
│   ┌────────────┐   ┌────────────┐   ┌────────────────┐     │
│   │  Preview   │   │  Staging   │   │  Production    │     │
│   │  (per PR)  │──►│            │──►│                │     │
│   └────────────┘   └────────────┘   └────────────────┘     │
│                                                            │
│   Components:                                              │
│   ├── Backstage backend + frontend                         │
│   ├── PostgreSQL                                           │
│   ├── Auth (Keycloak / GitHub OAuth)                       │
│   └── Ingress / TLS                                        │
└────────────────────────────────────────────────────────────┘
```

---

## Target Architecture Overview

**Backstage** → **Automation** → **Infrastructure**

| Layer | What it does |
|-------|--------------|
| Control Plane | Backstage (UI, catalog, templates) |
| Execution | GitLab, Ansible, Terraform |
| Infrastructure | OpenShift, Azure |

```mermaid
graph LR
    subgraph IDP[Internal Developer Platform]
        Backstage
    end

    subgraph Auth[Identity]
        Keycloak
    end

    subgraph CI[Automation]
        GitLab
    end

    subgraph Runtime[Infrastructure]
        OpenShift
    end

    subgraph Ops[Observability]
        Prometheus
        Vault
    end

    Keycloak --> Backstage
    Backstage --> GitLab
    GitLab --> OpenShift
    OpenShift --> Prometheus
    Vault --> OpenShift
```

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

## Layer-to-Tool Mapping

| Layer | Tools |
|-------|-------|
| Control | Backstage |
| Identity | Keycloak, OPA |
| Execution | GitLab, Ansible, Terraform |
| Infrastructure | OpenShift, Azure |
| Observability | Prometheus, Loki |
| Secrets | Vault |

---
<!--
## Anti-Patterns

| Area | Don't | Do |
|------|-------|-----|
| **Control Plane** | Direct infra changes, logic in plugins | Orchestrate, never execute |
| **Identity** | Hardcoded permissions, no audit | Central identity + policy as code |
| **Eventing** | Sync long-running tasks, tight coupling | Async, event-driven workflows |
| **Observability** | No plugin metrics, no SLOs | Full-stack observability |
| **Secrets** | Secrets in Git, no rotation | Runtime-only injection |
| **Catalog** | No owners, stale services | Ownership & lifecycle validation |
| **FinOps** | No quotas, no accountability | Cost tied to ownership

--- -->

## Lessons Learned

- **Provide Templates for Documentation**
  - Ensure consistent documentation and clear documentation structures
  - Reduce effort for developers and faster documentation creation
  - Increase completeness and clarity
- **Support Linting**
  - Increase the quality
  - Catch errors early
  - Provide a reusable jobs for CI/CD
  - Provide documentation
- **Provide Silver Path**


---

## Key Takeaways

* Backstage is a **control plane**, not a workflow engine
* Policies, events, and observability are mandatory at scale
* Architecture must evolve incrementally
* Governance enables, not blocks, self-service

---

## Final Message

**A successful internal developer platform is:
Self-service by default, governed by design, and observable end-to-end.**
