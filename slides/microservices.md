# /Microservices
--
### /Microservices
* Eine auf Microservices basierende Software-Architektur unterteilt ein System in eine Vielzahl eigenständiger Dienste bzw. Module <!-- .element: class="fragment fade-up" -->
* Diese möglichst kleingeschnittenen Dienste können in unterschiedlichen Programmiersprachen bzw. Technologien entwickelt werden und kommunizieren untereinander über standardisierte Schnittstellen <!-- .element: class="fragment fade-up" -->
--
### /Microservices
[<img src="https://artifacts.tiab.labda.sva.de/images/devops/microservices.png" width="400"/>](https://www.metaltoad.com/sites/default/files/inline-images/22605665.jpg)
--
### /Microservices
* Ein System, z.B. eine Webapplikation oder eine mobile App, kann von menschlichen Usern oder weiteren IT-Systemen über ein API-Gateway erreicht werden <!-- .element: class="fragment fade-up" -->
* Das API-Gateway stellt den zentralen Einstiegspunkt des Systems dar und vermittelt Anfragen entsprechend an die einzelnen Microservices weiter <!-- .element: class="fragment fade-up" -->
--
### /Grundlegende Prinzipen von Microservices sind
* Module eines Gesamtsystems dürfen nicht direkt von den Implementierungsdetails eines anderen Moduls abhängen <!-- .element: class="fragment fade-up" -->
* Der Zugriff von einem Modul auf ein anderes ist nur über definierte Schnittstellen möglich <!-- .element: class="fragment fade-up" -->
--
### /Microservice-Prinzipen
* Microservices müssen über virtuelle Maschinen oder containerisiert bereitgestellt werden, um ihre Unabhängigkeit zu gewährleisten <!-- .element: class="fragment fade-up" -->
* Microservice-Architekturentscheidungen werden auf zwei Ebenen getroffen: Der Makro-Ebene, welche alle Module betrifft, und die Mikro-Ebene, welche sich auf einen einzelnen Dienst bezieht <!-- .element: class="fragment fade-up" -->
--
### /Microservice-Prinzipen
* Die Wahl der Kommunikationswege muss auf wenige Technologien wie REST oder Messagingprotokolle standardisiert und begrenzt sein <!-- .element: class="fragment fade-up" -->
* Das Testen von Microservices ist Teil einer dedizierten Continuous-Delivery-Pipeline pro Modul <!-- .element: class="fragment fade-up" -->
--
### /Microservice-Prinzipen
* Microservices dürfen nicht ausfallen, wenn Kommunikationsprobleme auftreten oder andere Microservices nicht zur Verfügung stehen <!-- .element: class="fragment fade-up" -->
* Es muss möglich sein, einzelne Module herunterzufahren ohne Daten zu verlieren <!-- .element: class="fragment fade-up" -->
* Es muss möglich sein Microservices zwischen unterschiedlichen Betriebsumgebungen verschieben zu können <!-- .element: class="fragment fade-up" -->
--
### /Architektur-Design
* Eine Komposition aus Microservices stellt nicht für jede Applikation ein passendes Architektur-Design dar <!-- .element: class="fragment fade-up" -->
* Monolithische Software bzw. deren (Teil-)Funktionen sind in vielen Fällen einfacher nachzuvollziehen und technisch bereitzustellen, weil sie "'aus einem großen Ganzen"' bestehen <!-- .element: class="fragment fade-up" -->
--
### /Architektur-Design
* Die Skalierbarkeit einer monolithischen Anwendung stellt ab einer bestimmten Größe sowohl in Bezug auf die Komplexität der Programmierung/Quellcode als auch auf die Einbindung weiterer Entwicklern eine Herausforderung dar <!-- .element: class="fragment fade-up" -->