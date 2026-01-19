
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

---

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

---
title: TechDocs in Backstage
theme: black
revealOptions:
  transition: slide
  controls: true
  progress: true
  center: true
  hash: true
---

# TechDocs in Backstage

### Beautiful Documentation for Your Infrastructure

---

## How It Works

When a user creates a new repository using this template...

---

### Step 1

## Backstage Generates the Repo

📦 All documentation is included automatically

---

### Step 2

## TechDocs Annotation

```yaml
annotations:
  backstage.io/techdocs-ref: dir:.
```

Tells Backstage where to find docs

---

### Step 3

## MkDocs Builds & Renders

🔨 Backstage's TechDocs plugin processes the MkDocs site

---

### Step 4

## Users See the "Docs" Tab

📚 Beautiful documentation right in Backstage!

---

## Viewing TechDocs in Backstage

---

### 1️⃣ Create a Repo

Use the template in Backstage to scaffold your project

---

### 2️⃣ Navigate to Component

Find your component in the Backstage catalog

---

### 3️⃣ Click "Docs" Tab

✨ The beautiful documentation renders there!

---

## TechDocs Build Modes

---

### Local Mode

| | |
|---|---|
| **Mode** | `local` |
| **How** | Backstage builds docs on-demand |
| **Best for** | Development, small teams |

---

### External Mode

| | |
|---|---|
| **Mode** | `external` |
| **How** | CI/CD builds & publishes to storage |
| **Best for** | Production, large teams |

---

## External Mode Setup

Add to your `.gitlab-ci.yml`:

```yaml
build-docs:
  image: spotify/techdocs
  script:
    - techdocs-cli generate --no-docker
    - techdocs-cli publish \
        --publisher-type awsS3 \
        --storage-name $BUCKET
```

---

## Preview Locally

---

### Install TechDocs CLI

```bash
npm install -g @techdocs/cli
```

---

### Generate & Serve

```bash
cd template
techdocs-cli serve
```

---

### View Preview

🌐 Opens at `http://localhost:3000`

---

## Documentation Structure

```
docs/
├── index.md
├── getting-started/
├── architecture/
├── operations/
├── development/
└── reference/
```

---

## What's Included

- 📖 **14 documentation pages**
- 📊 **Mermaid diagrams**
- 🎨 **Material theme**
- 🔧 **Provider-specific content**

---

## Questions?

### Happy Documenting! 📚

---

## Resources

- [Backstage TechDocs](https://backstage.io/docs/features/techdocs/)
- [MkDocs](https://www.mkdocs.org/)
- [TechDocs CLI](https://github.com/backstage/techdocs-cli)
