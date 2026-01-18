# /BACKSTAGE

---

### /THE Backstage Platform

**Backstage** is an open platform for building Internal Developer Portals, originally created by Spotify.

<img src="https://backstage-spotify-com.spotifycdn.com/_next/static/media/twitter-summary-default.e17fd878.png" alt="Backstage Logo" style="width: 30%; margin: 1rem 0;" />

- 🧩 **Plugin-based architecture** — tailor it to your platform
- 📚 **Software Catalog** — track ownership, metadata & lifecycle
- 🚀 **Scaffolder** — bootstrap new services with templates
- 📊 **TechDocs** — docs-as-code, surfaced directly in the UI
- 🔌 **Ecosystem integrations** — GitHub, Argo CD, Kubernetes

---

### /USE OR BUILD?

<img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F89c0df9e-a35b-40c9-bbd1-ade37c3f792e_500x626.jpeg" alt="Alt Text" width="500"/>

---

### Backstage Concept

- Core: Base functionalities built by open-source project
- App: An instance deployed (Customized & Glues core with plugins
- Plugins: Extends core functionalities

---

### / GITLAB AUTHENTICATION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/gl-auth.png" alt="Alt Text" width="7000" style="border: none; box-shadow: none;" />

- No need to manage a separate user database for Backstage
- Fine-grained access control based on GitLab org structure

---

<!-- ### / GITLAB USER CONFIG

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/gl-user.png" alt="Alt Text" width="600" style="border: none; box-shadow: none;" />

- kind: User is a type of entity defined in the Software Catalog
- representing an developer, engineer, or operator

--- -->

### / GITLAB USER CONFIG

<div style="display: flex; align-items: center; justify-content: center;">

  <img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/gl-group.png" alt="Left Image" width="600" style="border: none; box-shadow: none;"/>

  <div style="flex: 3; text-align: center; padding: 0 80px;">
    - <code>kinds: User/Group</code> are types of entity defined in the Software Catalog<br>
    - Representing (a group of) developers, engineers, or operators
  </div>

  <img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/gl-user.png" alt="Right Image" width="600" style="border: none; box-shadow: none;"/>
</div>

---

### / SOFTWARE CATALOG

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/backstage3.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

---

### /SOFTWARE CATALOG

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/components-overview.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Central place to manage all your software
- Supports components like services, libraries, APIs, resources
- YAML-based definitions (`catalog-info.yaml`)

---
### /LOCATION+COMPONENT

<div style="display: flex; align-items: center; justify-content: center;">

  <img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/location.png" alt="Left Image" width="600" style="border: none; box-shadow: none;"/>

  <div style="flex: 3; text-align: center; padding: 0 80px;">
    - <code>kind: Location</code> reference to catalog configuration files <br>
    - <code>kind: Component</code> describes metadata about the service <br>
  </div>

  <img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/component.png" alt="Right Image" width="600" style="border: none; box-shadow: none;"/>
</div>


---

### /SOFTWARE CATALOG

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/components-example.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Detailed view of component

---


### /SOFTWARE CATALOG

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/createcomponent.png" alt="Backstage" style="width:200%; border: none; box-shadow: none;" />

- Creating a new component

---

### /SOFTWARE CATALOG

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/enterurl.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Enter Repository URL of catalog-info.yaml file

---
### /CATALOG

<!-- slide title: Component, Catalog, and Location -->

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/catlog.png" alt="Alt Text" width="7000" style="border: none; box-shadow: none;" />

---

### / SOFTWARE TEMPLATES

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/backstage4.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

---

### /SOFTWARE TEMPLATE OVERVIEW

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/software-templates.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- see all available sw-templates

---

### /SOFTWARE TEMPLATE DIALOG (CROSSPLANE RESOURCE)

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/software-templates2.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Create a new component using templates

---

### /TEMPLATE DEFINITION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/sw-tpl.png" alt="Right Image" width="600" style="border: none; box-shadow: none;"/>

- Presents input parameters to the user (via Backstage UI)
- Uses those parameters to generate code from a template repo

---

### /NAMESPACE TEMPLATE

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/ns-tpl.png" alt="Right Image" width="1200" style="border: none; box-shadow: none;"/>

- Namespace Creation w/ Crossplane
- Nunjucks is a templating language created by Mozilla

---

### /CATALOG TEMPLATE

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/cat-info.png" alt="Right Image" width="700" style="border: none; box-shadow: none;"/>

- 🔁 From input → templated code → Git repo → deployment = self-service, production-ready infrastructure.

---

### /MERGE REQUEST ACTION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/sw-tpl-mr.png" alt="Right Image" width="2000" style="border: none; box-shadow: none;"/>

- Backstage can create a merge/pull request
— allowing teams to review changes before merging

---

### /Crossplane Lifecycle Process

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/xplane-process2.png" alt="Alt Text" width="400" style="border: none; box-shadow: none;" />

---


### /SOFTWARE TEMPLATES

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/backstage6.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

---

### /KRO DB-CLAIM

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kro-db.png" alt="Alt Text" width="700" style="border: none; box-shadow: none;" />

- Kro will render a Kubernetes Deployment, Secret, Service, and PVC based on this claim

---

### / SOFTWARE TEMPLATES

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/backstage5.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

---

### / SOFTWARE TEMPLATES - CUSTOMER GROUPS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/cust-tpl.png" alt="Alt Text" width="1200" style="border: none; box-shadow: none;" />

---

### / SOFTWARE TEMPLATES - CUSTOMER GROUPS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/cust.png" alt="Alt Text" width="1200" style="border: none; box-shadow: none;" />

---

### /SOFTWARE TEMPLATES - CUSTOMER GROUPS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/createcustomergroups1.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Create a new Customer Group

---

### /SOFTWARE TEMPLATES - CUSTOMER GROUPS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/createcustomergroups2.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Choose the onboarding repo

---

### /SOFTWARE TEMPLATES - CUSTOMER GROUPS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/createcustomergroups3.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Fill in the fields

---

### /SOFTWARE TEMPLATES - CUSTOMER GROUPS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/customergroups1.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Review

---

### /SOFTWARE TEMPLATES - CUSTOMER GROUPS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/customergroups2.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Create

---

### /SOFTWARE TEMPLATES - CUSTOMER GROUPS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/customergroups3.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Merge Request

---

### CI/CD GITLAB PIPELINES

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/backstage7.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

---

### CI/CD GITLAB PIPELINES

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/gitlab-pipeline.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Detailed view of the Components GitLab Pipelines

---
### /KUBERNETES

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kubernetes.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Detailed view of Kubernetes Clusters


---

### /TECHDOCS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/backstage8.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

---

### /TECHDOCS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/techdocs.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- TechDocs View in Backstage
---
<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/quiz-quiztime.png" alt="KCP" style="width:80%; border: none; box-shadow: none;" />

--

# UPDATED SLIDES

---

## Why Plugins Matter

- Backstage is a **framework**, not a product
- Plugins turn it into a real **Internal Developer Portal**
- Good plugin choices:
  - Improve developer experience
  - Reduce cognitive load
  - Enable self-service

---

### GitHub / GitLab Plugins 🧑‍💻

- GitHub Actions / GitLab CI
- Pull Requests
- Repo insights

**➡️ Pick what matches your SCM**

---

### CI/CD Plugins ⚙️

- GitHub Actions
- GitLab Pipelines
- CircleCI
- Argo / Flux (GitOps)

**➡️ Visibility without leaving Backstage**

---

## 📊 Observability & Quality

Turn Backstage into a **single pane of glass**.

--

## 📊 Observability & Quality

Turn Backstage into a **single pane of glass**.

--

## 💰 Cost & FinOps

Optional but powerful:

- Cost Insights
- Infracost
- OpenCost

**➡️ Useful for cloud-native platforms**

---

## 🧠 Discoverability Plugins

Helps understand complex landscapes:

- Catalog Graph (entity relationships)
- Tech Radar
- Linguist (language detection)

---

## 🛎️ Best Practices

- Start small, grow over time
- Prefer **core plugins** first
- Avoid plugin overload
- Treat Backstage as a **product**
- Align plugins with real developer needs

---

# Backstage Software Templates

How Templates, Rendering & Catalog Work Together

---

## Template Languages

Backstage uses **two templating languages**:

| Location | Language | Syntax |
|----------|----------|--------|
| template.yaml | Nunjucks | `${{ parameters.name }}` |
| Template files | Nunjucks/Jinja2 | `${{ values.name }}` |

---

## The Rendering Flow

```
User Input → template.yaml → Template Files → GitLab Repo
     ↓              ↓               ↓              ↓
  (Form)      (Parameters)    (Nunjucks)     (Published)
```

---

## template.yaml Structure

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:     # Template metadata
spec:
  parameters: # User input form definition
  steps:      # Actions to execute
  output:     # Links and messages
```

---

## Parameters → User Form

Parameters define the **input form** users see:

```yaml
parameters:
  - title: Repository Information
    properties:
      project_name:
        type: string
      provider:
        type: string
        enum: [aws, azure, gcp]
```

Backstage renders this as an interactive form.

---

## Steps: The Action Pipeline

Steps define **what happens** after form submission:

1. **fetch:template** - Render template files
2. **publish:gitlab** - Create repository
3. **catalog:register** - Add to Backstage catalog

---

## fetch:template Action

```yaml
- id: fetch-base
  action: fetch:template
  input:
    url: ./template
    values:
      project_name: ${{ parameters.project_name }}
      provider: ${{ parameters.provider }}
```

Maps **parameters** → **values** for template rendering.

---

## Template File Rendering

Files in `./template/` use Nunjucks syntax:

```hcl
# In template/versions.tf
{%- if values.provider == "aws" %}
    aws = {
      source  = "hashicorp/aws"
    }
{%- elif values.provider == "azure" %}
    azurerm = {
      source  = "hashicorp/azurerm"
    }
{%- endif %}
```

---

## Nunjucks Features Used

| Feature | Syntax | Purpose |
|---------|--------|---------|
| Variable | `${{ values.name }}` | Insert value |
| Condition | `{%- if %}` | Conditional content |
| Filter | `{{ name \| upper }}` | Transform value |
| Loop | `{%- for item in list %}` | Iterate |

---

## publish:gitlab Action

After rendering, files are pushed to GitLab:

```yaml
- id: publish
  action: publish:gitlab
  input:
    repoUrl: ${{ parameters.repoUrl }}
    defaultBranch: main
```

Creates the repository with rendered content.

---

## catalog:register Action

Registers the new repo in Backstage:

```yaml
- id: register
  action: catalog:register
  input:
    repoContentsUrl: ${{ steps['publish'].output.repoContentsUrl }}
    catalogInfoPath: '/catalog-info.yaml'
```

---

## The catalog-info.yaml

Every component needs this file for Backstage:

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: ${{ values.project_name }}
spec:
  type: infrastructure
  owner: group:default/engineering
```

Also rendered with Nunjucks!

---

## Complete Flow Diagram

```
┌─────────────┐
│  User Form  │  ← parameters defined in template.yaml
└──────┬──────┘
       ↓
┌─────────────┐
│fetch:template│ ← renders ./template/* files
└──────┬──────┘
       ↓
┌─────────────┐
│publish:gitlab│ ← creates repo with rendered files
└──────┬──────┘
       ↓
┌─────────────┐
│catalog:register│ ← adds to Backstage catalog
└─────────────┘
```

---

## Step Outputs & Chaining

Steps can reference **previous step outputs**:

```yaml
# publish step produces output.repoContentsUrl
# register step consumes it:
repoContentsUrl: ${{ steps['publish'].output.repoContentsUrl }}
```

---

## Key Takeaways

1. **template.yaml** defines form + actions
2. **Nunjucks** renders all template files
3. **parameters** → user input
4. **values** → available in template files
5. **Steps chain** via outputs

---



