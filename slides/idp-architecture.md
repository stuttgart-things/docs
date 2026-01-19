### Backstage Platform Architecture

---

## 1. Architecture Vision

**Backstage is not the platform — it is the control plane of the platform.**

* Enables self-service
* Enforces policy
* Orchestrates automation
* Provides visibility & governance

Everything else **executes**, **enforces**, **observes**, or **audits**.

---

## 2. Target Architecture Overview

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

### 3. Architecture Evolution Overview

| Phase | Name | Focus |
|-------|------|-------|
| 1 | Initial Adoption | Get started |
| 2 | Controlled Self-Service | Automate |
| 3 | Policy-Driven | Govern |
| 4 | Platform at Scale | Optimize |

---

### 4. Phase 1 — Initial Adoption

| Aspect | Details |
|--------|---------|
| **Goal** | Get Backstage running as UI & catalog |
| **Characteristics** | Manual approvals, direct API calls |
| **Tools** | Backstage, GitLab, OpenShift |
| **Risks** | Tight coupling, limited governance |

---

### 5. Phase 2 — Controlled Self-Service

| Aspect | Details |
|--------|---------|
| **Goal** | Enable repeatable, automated workflows |
| **Characteristics** | Software Templates, CI/CD-driven, centralized identity |
| **Tools** | Backstage Templates, GitLab CI/CD, Keycloak |
| **Outcome** | Repeatability, reduced manual work |

---

### 6. Phase 3 — Policy-Driven Platform

| Aspect | Details |
|--------|---------|
| **Goal** | Enforce governance without blocking teams |
| **Characteristics** | Policy as Code, async workflows, clear ownership |
| **Tools** | OPA / Gatekeeper, Kyverno, Event Bus |
| **Outcome** | Safe autonomy, compliance by default |

---

### 7. Phase 4 — Platform at Scale

| Aspect | Details |
|--------|---------|
| **Goal** | Sustainable, cost-aware platform operations |
| **Characteristics** | Observability-first, FinOps, plugin lifecycle |
| **Tools** | Prometheus / Grafana, Cost Management APIs, Feature Flags |
| **Outcome** | Predictable, scalable platform |

---

## 8. Layer-to-Tool Mapping

| Layer | Tools |
|-------|-------|
| Control | Backstage |
| Identity | Keycloak, OPA |
| Execution | GitLab, Ansible, Terraform |
| Infrastructure | OpenShift, Azure |
| Observability | Prometheus, Loki |
| Secrets | Vault |

---

## 9. Anti-Patterns

| Area | Don't | Do |
|------|-------|-----|
| **Control Plane** | Direct infra changes, logic in plugins | Orchestrate, never execute |
| **Identity** | Hardcoded permissions, no audit | Central identity + policy as code |
| **Eventing** | Sync long-running tasks, tight coupling | Async, event-driven workflows |
| **Observability** | No plugin metrics, no SLOs | Full-stack observability |
| **Secrets** | Secrets in Git, no rotation | Runtime-only injection |
| **Catalog** | No owners, stale services | Ownership & lifecycle validation |
| **FinOps** | No quotas, no accountability | Cost tied to ownership

---

## 10. Lessons Learned

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

## 11. Helpful Questions

- Can you reduce feedback loops? (pair /peer programming)
- Where is cognitive load highest?
- Which teams need support?
- What would great DX look like?

---

## 12. Key Takeaways

* Backstage is a **control plane**, not a workflow engine
* Policies, events, and observability are mandatory at scale
* Architecture must evolve incrementally
* Governance enables, not blocks, self-service

---

## 13. Final Message

**A successful internal developer platform is:
Self-service by default, governed by design, and observable end-to-end.**
