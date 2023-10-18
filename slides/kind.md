# /KIND
--
### /What is Kind?
[<img src="https://miro.medium.com/v2/resize:fit:720/format:webp/0*TnRE3e_38kjdBz1j.png" width="400"/>](https://www.metaltoad.com/sites/default/files/inline-images/22605665.jpg)

* Kind that allows to generate clusters on Docker, even multi-node and/or simulating high availability
--
### /Create a Cluster

* CLI commands  <!-- .element: class="fragment fade-up" -->

```yaml
kind create cluster
kind create cluster --name=[cluster-name]
```
<!-- .element: class="fragment fade-up" -->
--
### Create a cluster with more than one node

* config <!-- .element: class="fragment fade-up" -->

```yaml
# three node (two workers) cluster config
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
```
<!-- .element: class="fragment fade-up" -->

* CLI command  <!-- .element: class="fragment fade-up" -->
```
kind create cluster --name=nodes-test --config=workerNodes.yaml
```
--
### How to load a docker image into cluster node

```bash
kind load docker-image webapp:<username> --name <KIND-CLUSTERNAME>
```
