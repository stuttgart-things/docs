# /BACKSTAGE

---

### /GETTING STARTED

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/backstage1.png" alt="Backstage" style="width:80%; border: none; box-shadow: none;" />

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

### / AUTHENTICATION

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/backstage2.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

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
