+++
weight = 30
+++

{{< slide id=infra background-color="#e7b8ddff" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /Platform-Engineering

---

### 🏗️ Platform Engineering

<img src="https://pbs.twimg.com/media/FnabgQxXwAEDZz6.jpg" alt="Alt Text" width="400"/>

- Platform Engineering is about building **self-service platforms** that abstract complexity.
- Empower developers to ship faster
- Remove infrastructure worries from developers' day-to-day

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
### EXAMPLE TEAM/COMPANY SIZES

- Small org ~50 devs → small platform team (2–4 FTE) focusing on on-boarding & pipeline templates

- Mid-size ~200 devs → platform team (6–10 FTE), centralized pipelines, service catalog, self-service infra

- Enterprise 1000+ devs → larger platform org (20+ FTE), strong IDP, SLOs, cross-team platform product managers

- Typical benefits reported: faster on-board, less duplicated work, measurable dev-hours saved

---

### WHAT ARE GOLDEN PATHS

<img src="https://miro.medium.com/v2/resize:fit:1200/0*BEkTUO3XM3kaQFUl" alt="When to introduce" width="500"/>

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

### TEAM SIZING

<img src="https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?q=80&w=1400&auto=format&fit=crop&ixlib=rb-4.0.3&s=placeholder" alt="Team sizing" width="800"/>

---

### TEAM SIZING

- < 30 devs: No dedicated platform org usually — 1–2 infra/DevOps engineers embedded in teams
- ~30–100 devs: 2–6 people focused on platform features + templates (part-time or small team)
- 100–500 devs: 6–20 FTEs running IDP, pipelines, service catalog, observability
- 500+ devs: Platform becomes a full product org (20+), with SLAs, PMs, SREs, UX

{{% /section %}}
