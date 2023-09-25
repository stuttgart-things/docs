# /K9s
--
### /What is K9s?
* K9s is a command-line based utility for managing and monitoring Kubernetes clusters <!-- .element: class="fragment fade-up" -->
* It provides a visual interface allowing users to view and manage their Kubernetes resources <!-- .element: class="fragment fade-up" -->
* pods, deployments, and services, in a more intuitive and user-friendly way than using the kubectl command-line tool <!-- .element: class="fragment fade-up" -->
* K9s also offer features such as resource filtering, inline editing, and resource management and deployment tools <!-- .element: class="fragment fade-up" -->
* It is designed to be lightweight, making it a useful tool for developers and administrators who work with Kubernetes clusters on a daily basis <!-- .element: class="fragment fade-up" -->
--
### /Key features
* Resource filtering: Easily filter and find specific resources within your Kubernetes cluster <!-- .element: class="fragment fade-up" -->
* Inline editing: Modify resources directly within K9s, streamlining your workflow <!-- .element: class="fragment fade-up" -->
* Comprehensive resource management and deployment tools: Efficiently manage and deploy resources with an extensive set of tools <!-- .element: class="fragment fade-up" -->
--
### /Key features
* Lightweight design: K9s is designed to be fast and easy to use, making it an ideal choice for daily Kubernetes cluster interactions <!-- .element: class="fragment fade-up" -->
* User-friendly: K9s offers a straightforward and intuitive interface, simplifying Kubernetes management for developers and administrators <!-- .element: class="fragment fade-up" -->
--
### /Viewing resources
* If you are familiar with vim commands, you will be right at home with K9s <!-- .element: class="fragment fade-up" -->
* The way to change what you are seeing is by prefixing the type of resource with a colon <!-- .element: class="fragment fade-up" -->
* in order to view pods in your cluster once you are running K9s, you would type :pods and press enter <!-- .element: class="fragment fade-up" -->
* To switch to viewing nodes, type in :node and press enter <!-- .element: class="fragment fade-up" -->
--
### /USAGE

* CLI:

```
# List all available CLI options
k9s help
# Get info about K9s runtime (logs, configs, etc..)
k9s info
# Run K9s in a given namespace
k9s -n mynamespace
# Run K9s and launch in pod view via the pod command
k9s -c pod
# Start K9s in readonly mode - with all modification commands disable
k9s --readonly
```
<!-- .element: class="fragment fade-up" -->
--
### /Viewing resources
* The way to change what you are seeing is by prefixing the type of resource with a colon <!-- .element: class="fragment fade-up"
* to view pods in your cluster once you are running K9s, you would type :pods and press enter <!-- .element: class="fragment fade-up"
* To switch to viewing nodes, type in :node and press enter <!-- .element: class="fragment fade-up" -->
--
### /Searching
* If you have a lot of resources of a particular type in a cluster, you can quickly search through them using the / command <!-- .element: class="fragment fade-up" -->
* If, for example, you wanted to filter all namespaces you retrieved in the previous section down to just the ones that contain kube in their name, you would type:

```
/kube <enter>
```
<!-- .element: class="fragment fade-up" -->
--
### / ENCODE SECRETS
* SEARCH FOR SECRETS AND ENCODE: <!-- .element: class="fragment fade-up" -->

```
k9s # start
:secrets [NAMESPACE] # show secrets
/mongodb # filter for mongo db
# select secret and encode by pressing x
```
<!-- .element: class="fragment fade-up" -->
--