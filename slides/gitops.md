# /GitOps
--
### /GitOps
* GitOps is a way to do Kubernetes cluster management and application delivery <!-- .element: class="fragment fade-up" -->
* It works by using Git as a single source of truth for declarative infrastructure and applications <!-- .element: class="fragment fade-up" -->
--
<!-- ### /Flux: The GitOps Kubernetes Operator
* Ensures that the state of a cluster matches the config in Git
* Uses an operator in the cluster
* Monitors image repositories, detects new images, triggers deployments
* No separate CD tool
--
### /Flux: The GitOps Kubernetes Operator
* No access to the cluster for CI tools
* Every change is atomic and transactional
* Git has the audit log
-- -->
### /Argo CD
* Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes <!-- .element: class="fragment fade-up" -->
[<img src="https://argoproj.github.io/static/argo-cd-ui-87dce328a7ab3be2d13f7926831068eb.gif" width="700"/>](https://www.sva.de/index.html)
--
### /Argo CD
* Kubernetes-native continuous deployment (CD) tool <!-- .element: class="fragment fade-up" -->
* Argo CD can pull updated code from Git repositories and deploy it directly to Kubernetes resources <!-- .element: class="fragment fade-up" -->
* It enables developers to manage both infrastructure configuration and application updates in one system <!-- .element: class="fragment fade-up" -->
--
### /key features and capabilities
* Manual or automatic deployment of applications to a Kubernetes cluster <!-- .element: class="fragment fade-up" -->
* Automatic synchronization of application state to the current version of declarative configuration <!-- .element: class="fragment fade-up" -->
* Web user interface and command-line interface (CLI) <!-- .element: class="fragment fade-up" -->
--
### /key features and capabilities
*  Ability to visualize deployment issues, detect and remediate configuration drift <!-- .element: class="fragment fade-up" -->
* Role-based access control (RBAC) enabling multi-cluster management <!-- .element: class="fragment fade-up" -->
* Single sign-on (SSO) with providers such as GitLab, GitHub, Microsoft, OAuth2, OIDC, LinkedIn, LDAP, and SAML 2.0 <!-- .element: class="fragment fade-up" -->
* Support for webhooks triggering actions in GitLab, GitHub, and BitBucket.
This is part of an extensive series of guides about Kubernetes <!-- .element: class="fragment fade-up" -->
--
### /Argo CD process
--
* A developer makes changes to an application <!-- .element: class="fragment fade-up" -->
* pushing a new version of Kubernetes resource definitions to a Git repo <!-- .element: class="fragment fade-up" -->
* Continuous integration is triggered = new container image saved to a registry <!-- .element: class="fragment fade-up" -->
* A developer issues a pull request = changing Kubernetes manifests (manually or automatically) <!-- .element: class="fragment fade-up" -->
--
### /Argo CD process
* The pull request is reviewed and changes are merged to the main branch <!-- .element: class="fragment fade-up" -->
* This triggers a webhook which tells Argo CD a change was made <!-- .element: class="fragment fade-up" -->
* Argo CD clones the repo and compares the application state with the current state of the Kubernetes cluster <!-- .element: class="fragment fade-up" -->
* It applies the required changes to cluster configuration <!-- .element: class="fragment fade-up" -->
--
### /Argo CD process
* Kubernetes uses its controllers to reconcile the changes required to cluster resources, until it achieves the desired configuration <!-- .element: class="fragment fade-up" -->
* Argo CD monitors progress and when the Kubernetes cluster is ready = reports that the application is in sync <!-- .element: class="fragment fade-up" -->
* ArgoCD also works in the other direction, monitoring changes in the Kubernetes cluster and discarding them if they don't match the current configuration in Git <!-- .element: class="fragment fade-up" -->
--