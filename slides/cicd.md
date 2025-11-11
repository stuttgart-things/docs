### /Kontinuierlicher Entwicklungsprozess
[<img src="https://artifacts.tiab.labda.sva.de/images/kubernetes/cicdcd.png" width="700"/>](https://www.sva.de/index.html)
--
### /Continuous Integration
* Änderungen an der gemeinsam genutzten Quellcode-Basis einer Applikation werden i.d.R. von mehreren Softwareentwicklern durchgeführt, welche parallel an verschiedenen Programmteilen bzw. Funktionen (engl. features) arbeiten <!-- .element: class="fragment fade-up" -->
* Durch jede Änderung an der Codebasis wird beim Continuous Integration-Ansatz eine automatische Kompilierung (engl. build) der Software ausgelöst <!-- .element: class="fragment fade-up" -->
--
### /Continuous Integration
* Bei diesem Vorgang werden durch anschließende Tests aufgetretene Fehler zurückgemeldet <!-- .element: class="fragment fade-up" -->
* Die Zusammenführung (engl. merge) der Änderungen und die Integration in die Hauptlinie der Quellcodeverwaltung soll auf täglicher Basis und (weitestgehend) automatisiert stattfinden <!-- .element: class="fragment fade-up" -->
--
### /Continuous Integration
* Das Ziel von CI ist die Schaffung eine stabile Code-Basis, welche Risiken von fehlgeschlagenen und aufwendigen Integrationen zu späteren, unregelmäßigen Zeitpunkten minimieren soll <!-- .element: class="fragment fade-up" -->
--
### /Continuous Delivery
* Software-Releases in die Produktion zu bringen, ist mit grundsätzlichen Risiken verbunden, wie z.B. Programmfehlern, Inkompatibilitäten mit Fremdsystemen oder vorhandener Datenstämme oder unvorhergesehener Zeitverzögerungen bei der Bereitstellung <!-- .element: class="fragment fade-up" -->
* Um den Risiken von Deployments aus dem Weg zu gehen, wird "in der klassischen IT" versucht, diese mit einem maximal möglich großen Programm-Funktionsumfang und möglichst selten durchzuführen <!-- .element: class="fragment fade-up" -->
--
### /Continuous Delivery
* Im Gegensatz dazu steht der Continuous Delivery Ansatz dafür, möglichst häufige Releases mit kleinen Änderungen auf eine Produktionsumgebung zu bringen <!-- .element: class="fragment fade-up" -->
* So soll die Fehler-Wahrscheinlichkeit minimiert werden <!-- .element: class="fragment fade-up" -->
* Die Voraussetzungen dafür sind erprobte und optimierte automatisierte Prozesse von der Quellcode-Zusammenführung, Testing bis hin zur Erstellung von Build-Paketen welche auf Entwicklungs und Integrationsumgebungen (engl. Staging) erprobt wurden <!-- .element: class="fragment fade-up" -->
--
### /Continuous Deployment:
* Auf Basis in der Continuous Delivery-Phase erstellter, produktionsreifer Build-Pakete kann durch Implementierung von Continuous Deployment auch die produktive Freigabe einer Applikation und die entsprechende Bereitstellung automatisiert werden <!-- .element: class="fragment fade-up" -->
--
### /Continuous Deployment:
* Continuous Deployment bedeutet, dass Quellcode-Änderungen der Entwickler innerhalb kürzester Zeit produktiv bereitstehen, sofern alle automatisierten Tests erfolgreich durchlaufen wurden <!-- .element: class="fragment fade-up" -->
--
### /CI-CD Prozess
[<img src="https://artifacts.tiab.labda.sva.de/images/kubernetes/cicdprocess.png" width="700"/>](https://www.sva.de/index.html)
--
### /Pipelining
* CI/CD Pipelines werden eingesetzt um: <!-- .element: class="fragment fade-up" -->
  * schnelles Feedback auf Änderungen an der Codebasis zu erhalten <!-- .element: class="fragment fade-up" -->
  * um einen iterativen, automatisierten und möglichst oft erprobten Weg zu entwickeln in Bezug auf die Überführung von Software in einen produktiven Status <!-- .element: class="fragment fade-up" -->
--
### /Pipelining
* Die detaillierte Umsetzung einer CI/CD Pipeline variieret zwischen Unternehmen bzw. Einsatzszenariio, da sie auch von gegebenen Geschäftsprozessen wie z.B. den Softwarefreigabe-Mechanismen oder Compliance-Richtlinien abhängen können <!-- .element: class="fragment fade-up" -->
* Eine CI/CD-Pipeline ist in unterschiedliche Stufen (engl. stages) untergliedert um einzelne Prozessphase logisch voneinander abzugrenzen zu können <!-- .element: class="fragment fade-up" -->
--
### /Möglicher Prozessablauf einer CI/CD Pipeline
* Die folgende Beschreibung zu einem möglichen Prozessablauf einer CI/CD Pipeline bezieht sich auf einen iterativ entwickelten und containerisierten Microservice für die Zielplattform Kubernetes <!-- .element: class="fragment fade-up" -->
--
### /Code commit
* Die erste Phase des Prozessablaufs wird  durch eine Änderung der Code-Basis (engl. code commit) ausgelöst <!-- .element: class="fragment fade-up" -->
* Jede Änderung am zentralen Quellcode-Bestand resultiert in einer Ausführung (engl. run) der Pipeline-Definition <!-- .element: class="fragment fade-up" -->
--
### /Software-Build
* Im Prozessschritt Build wird aus der vorliegenden Code-Basis eine ausführbare Applikation gebildet und als Software-Artefakt z.B. als ausführbare Binärdatei gespeichert <!-- .element: class="fragment fade-up" -->
* Die Ausführung statischer und dynamischer Codeanalysen und in vielen Fällen spezifische Software-Funktionstests erlaubt es Entwicklern zu bestimmen, welcher Software-Build sich für eine produktive Bereitstellung eignet <!-- .element: class="fragment fade-up" -->
--
### /Artefakte
* Für die Weiterverwendung von erstellten Artefakten, werden diese in einem entsprechenden Repository gespeichert <!-- .element: class="fragment fade-up" -->
* Sollten in diesem Stadium keine Fehler gefunden werden, wird automatisch die nächste Stufe der Pipeline ausgeführt <!-- .element: class="fragment fade-up" -->
--
### /Container-Build
* Um vollumfängliche CI/CD Pipelines mittels des Infrastructure as Code Ansatzes umsetzen zu können, bietet sich beispielsweise die DevOps-Plattformlösung <!-- .element: class="fragment fade-up" --> [GitLab](https://about.gitlab.com/) an.
--
### /Ausschnitt einer möglichen CI/CD-Pipeline in GitLab
```
 stages:
 - build
 build_container:
   stage: build
   image: buildah:1.15.0
   script:
     - buildah bud -t ${IMAGE_NAME}:${CI_COMMIT_SHA} .
     - buildah push ${IMAGE_NAME}:${CI_COMMIT_SHA}
       docker://${IMAGE_NAME}:${CI_COMMIT_SHA}
```
<!-- .element: class="fragment fade-up" -->
--
### /Ausschnitt einer möglichen CI/CD-Pipeline in GitLab
* Container-Images werden im gegebenen Beispiel über das OCI-konforme Werkzeug <!-- .element: class="fragment fade-up" --> [Buildah](https://github.com/) realisiert
* Die zugehörige Pipeline-Definition ist eine Mischung aus deklarativen Angaben zum Status bzw. Konfiguration der Pipeline (Zeile:1-5) und imperativen, nacheinander auszuführenden Befehlen (Z:7-9) <!-- .element: class="fragment fade-up" -->
* Mittels Buildah wird ein neuer Container gebaut und anschließend als Artefakt in eine Container Registry verschoben <!-- .element: class="fragment fade-up" -->
--
### /Staging
* Software wird im Entwicklungsprozess i.d.R. auf verschiedenen Betriebsumgebungen (engl. stage) getestet, um etwaige Programmfehler feststellen zu können und die Kommunikation bzw. Zusammenspiel mit Drittsystemen sicherstellen zu können <!-- .element: class="fragment fade-up" -->
* Die technische Bereitstellung kann mittels Infrastructure-as-Code automatisiert innerhalb einer Pipeline-Definition bis zum finalen Stadium "Produktion" (engl. release stage) nach dem Ansatz Continous Deployment realisiert werden <!-- .element: class="fragment fade-up" -->
