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


{{% /section %}}
