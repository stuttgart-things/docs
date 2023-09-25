# /Operator
--
### /Definition
* Methode zur Paketierung, Bereitstellung und Verwaltung einer Kubernetes-Anwendung <!-- .element: class="fragment fade-up" -->
* Ein Kubernetes Operator ist ein anwendungsspezifischer Controller, der die Funktionalität der Kubernetes-API erweitert, um Instanzen komplexer Anwendungen für einen Kubernetes-Nutzer zu erstellen, zu konfigurieren und zu verwalten <!-- .element: class="fragment fade-up" -->
--
### /Custom Resources (CR)
* Allgemeine Konfiguration und Einstellungen werden vom Nutzer in einer CR bereitgestellt <!-- .element: class="fragment fade-up" -->
* Der Kubernetes Operator übersetzt die allgemeinen Anweisungen basierend auf den in seiner Logik eingebetteten Best Practices in einzelne Aktionen <!-- .element: class="fragment fade-up" -->
--
### /Custom Resources (CR)
```
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx-demo
spec:
  service_type: ingress
```
--
### /Custom Resources (CR)
```
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: example-build-task
spec:
  params:
    - name: pathToDockerFile
      type: string
```
### /Operator Framework
* Open Source-Projekt mit Entwickler- und Runtime-Tools <!-- .element: class="fragment fade-up" -->
* Entwicklung eines Operators beschleunigen <!-- .element: class="fragment fade-up" -->
--
### /Operator-SDK
[<img src="https://artifacts.tiab.labda.sva.de/images/kubernetes/operator.png" width="1200"/>](https://www.sva.de/index.html)
--
### /Operator-SDK
* Ermöglicht Entwicklern die Erstellung von Operators basierend auf ihrem Fachwissen, ohne dass sie sich mit der Komplexität der Kubernetes-API auskennen müssen <!-- .element: class="fragment fade-up" -->
--
### /Operator Lifecycle Management
* Überwacht Installation, Updates und Verwaltung des Lifecycles aller in einem Kubernetes-Cluster ausgeführten Operators <!-- .element: class="fragment fade-up" -->
--
### /Operator-Messung
* Ermöglicht Nutzungsberichte für Operators, die spezielle Services bereitstellen <!-- .element: class="fragment fade-up" -->
--
