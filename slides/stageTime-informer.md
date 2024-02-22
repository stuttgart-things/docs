# STAGETIME-INFORMER
--
### /SERVICE
* INFORMS ABOUT PIPELINERUN EVENTS: <span style="color:orange">ADD, UPDATE & DELETE</span> <!-- .element: class="fragment fade-up" -->
* STORES RESULTS (SUCCESSFUL/FAILED STAGES) IN REDIS (JSON) <!-- .element: class="fragment fade-up" -->
* TRIGGERS NEW STAGE(-RUNS) (STREAMS) <!-- .element: class="fragment fade-up" -->
--
### /INFORMING KINDS
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/informer-kinds.png" width="1800"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /INFORMER CODE
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/informer-code.png" width="1100"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /INFORMER LOGS
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/informer-logs.png" width="2000"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /SEQUENCE
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/informer.png" width="1500"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /HELMFILE
* Compose several charts together to create a comprehensive deployment artifact <!-- .element: class="fragment fade-up" -->
* Separating Environment specific information from charts <!-- .element: class="fragment fade-up" -->
* Helmfile templates helm templates <!-- .element: class="fragment fade-up" -->
--
### /HELMFILE RELEASES
* DEFINE MULTIPLE RELEASES <!-- .element: class="fragment fade-up" -->

```
releases:
  - name: redis-stack
    installed: false
    namespace: stagetime-informer-redis
    chart: redis/redis
    version: 17.1.4
    values:
      - "env/redis-stack.yaml.gotmpl"
  - name: stagetime-informer
    installed: true
    # ...
```
<!-- .element: class="fragment fade-up" -->
--
### /HELMFILE ENVIRONMENTS
```
environments:
  labul-pve-dev:
    values:
      - env/defaults.yaml
      - env/{{ .Environment.Name }}.yaml
  vcluster:
    values:
      - env/defaults.yaml
      - env/{{ .Environment.Name }}.yaml
```
<!-- .element: class="fragment fade-up" -->
--
### /HELM VALUES
```
namespace: {{ .Release.Namespace }}
secrets:
  redis-connection:
    name: redis-connection
    labels:
      app: stagetime-server
    dataType: stringData
    secretKVs:
      REDIS_SERVER: {{ .Values.redisStack.serviceName }}
      REDIS_PORT: {{ .Values.redisStack.port }}
      REDIS_PASSWORD: {{ .Values.redisStack.password }}
```
<!-- .element: class="fragment fade-up" -->
--
### / HELMFILE VALUES
```
ingressDomain: cd43.sthings-pve.labul.sva.de
redisPassword: ref+vault://stagetime/redis/password
redisServer: redis-stack-headless.\
stagetime-redis.svc.cluster.local
```
<!-- .element: class="fragment fade-up" -->
