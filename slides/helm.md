# /Helm
--

### /OVERVIEW

* Helm is a package manager for Kubernetes applications that includes templating and lifecycle management functionality <!-- .element: class="fragment fade-up" -->
* It is essentially a package manager for Kubernetes manifests (such as Deployments, ConfigMaps, Services, etc.) that are grouped into charts <!-- .element: class="fragment fade-up" -->
* A chart is just a template for creating and deploying applications on Kubernetes using Helm <!-- .element: class="fragment fade-up" -->

--

### /OVERVIEW

* Charts are written in YAML and contain metadata about each resource in your app (e.g., labels, values, etc.) <!-- .element: class="fragment fade-up" -->
* A chart can be used by itself or combined with other charts into composite charts which can be used as templates for creating new applications or modifying existing ones <!-- .element: class="fragment fade-up" -->
* Helm essentially allows you to manage one chart for your environment <!-- .element: class="fragment fade-up" -->

--

### /Architecture

* Helm Client: The client is the user interface to Helm <!-- .element: class="fragment fade-up" -->
* It is used to create new charts, manage repositories, and release packages <!-- .element: class="fragment fade-up" -->
* The Helm client can be installed on both macOS and Linux <!-- .element: class="fragment fade-up" -->
* Developers also use help to test upgrades before releasing them into production <!-- .element: class="fragment fade-up" -->

--

### /Architecture

* Helm Library: Helm library is a set of client libraries that are used by the clients to interact with the Kubernetes API server to install, upgrade, or roll back charts <!-- .element: class="fragment fade-up" -->
* The tool is installed on every node in the cluster and is a required component for installing any chart <!-- .element: class="fragment fade-up" -->

--

### /What Are Helm Charts?

Chart is the packaging format used by Helm: <!-- .element: class="fragment fade-up" -->
 * it contains the specs that define the Kubernetes objects that the application consists of, such as YAML files and templates, which convert into Kubernetes manifest files <!-- .element: class="fragment fade-up" -->
 * Charts are reusable across environments <!-- .element: class="fragment fade-up" -->
 * This reduces complexity and minimizes duplicates across configurations <!-- .element: class="fragment fade-up" -->

--

### /There are three basic concepts to Helm charts

* Chart: A Helm chart is a pre-configured template for provisioning Kubernetes resources <!-- .element: class="fragment fade-up" -->
* Release: A release represents a chart that has been deployed <!-- .element: class="fragment fade-up" -->
* Repository: A repository is a public or private location for storing charts <!-- .element: class="fragment fade-up" -->

--

### /EXAMPLES

* INSTALL CHARTS:

```
helm repo add loki https://grafana.github.io/loki/charts
helm search repo loki
helm show values loki/loki-stack > loki_values.yaml
helm install loki-stack loki/loki-stack \
-f loki_values.yaml --namespace loki-stack
```
<!-- .element: class="fragment fade-up" -->
--

### /CUSTOM HELM CHARTS

* CREATE CHARTS:

```
helm create mychart
helm install --dry-run --debug ./mychart
helm install --dry-run --debug ./mychart
\--set service.internalPort=8080
helm install example ./mychart --set service.type=NodePort
```
<!-- .element: class="fragment fade-up" -->
---
