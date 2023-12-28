# stuttgart-things/docs/elastic

## ECK + VSPHERE MON

### ECK

<details><summary><b>HELM DEPLOYMENT</b></summary>

```bash
helm repo add elastic https://helm.elastic.co
helm repo update
helm upgrade --install eck elastic/eck-operator --version 2.9.0 --create-namespace -n elastic-system
```

</details>

### ELASTICSEARCH

<details><summary><b>CR ELASTICSEARCH</b></summary>

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-cluster
  namespace: elastic-system
spec:
  version: 7.17.7
  transport:
    service:
      spec:
        type: ClusterIP
  nodeSets:
  - name: default
    count: 1
    config:
      node.store.allow_mmap: false
    podTemplate:
      spec:
        initContainers:
        - name: sysctl
            securityContext:
            privileged: true
            runAsUser: 0
            command: ['sh', '-c', 'sysctl -w vm.max_map_count=262144']
```

</details>

### KIBANA

<details><summary><b>CR KIBANA</b></summary>

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana
  namespace: elastic-system
spec:
  version: 7.17.7
  count: 1
  elasticsearchRef:
    name: elasticsearch-cluster
  podTemplate:
    spec:
      containers:
      - name: kibana
        resources:
          requests:
            memory: 512Mi
            cpu: 500m
          limits:
            memory: 2Gi
            cpu: 1500m
  http:
    tls:
      selfSignedCertificate:
      disabled: true
    service:
      spec:
        type: LoadBalancer
```

</details>

### METRICBEAT

<details><summary><b>CR METRICBEAT</b></summary>

```yaml
---
kind: Secret
apiVersion: v1
metadata:
  name: vsphere-credentials
  namespace: elastic-system
stringData:
  VSPHERE_USER: <REPLACE-ME>
  VSPHERE_PASSWORD: <REPLACE-ME>
---
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: metricbeat
  namespace: elastic-system
spec:
  type: metricbeat
  version: 7.17.7
  elasticsearchRef:
    name: elasticsearch-cluster
  kibanaRef:
    name: kibana
  config:
    metricbeat:
      setup.dashboards.enabled: true
      modules:
        - module: vsphere
          enabled: true
          metricsets: ["datastore", "host", "virtualmachine"]
          period: 10s
          hosts: ["https://ul-vc01.labul.sva.de/sdk"]
          username: "${VSPHERE_USER}"
          password: "${VSPHERE_PASSWORD}"
          insecure: true
          get_custom_fields: true
  deployment:
    podTemplate:
      spec:
        dnsPolicy: ClusterFirstWithHostNet
        securityContext:
          runAsUser: 0
        containers:
          - name: metricbeat
            envFrom:
              - secretRef:
                  name: vsphere-credentials
```

</details>

### CONNECT TO ELASTICSEARCH FROM EXTERNAL

<details><summary><b>CONNECT W/ CURL</b></summary>

```bash
# SHELL1
kubectl -n elastic-system port-forward service/elasticsearch-cluster-es-http 9200

# SHELL2
ELASTIC_PASSWORD=$(kubectl get secret elasticsearch-cluster-es-elastic-user -n elastic-system -o=jsonpath='{.data.elastic}' | base64 --decode)

# SMOKETEST
curl -u "elastic:${ELASTIC_PASSWORD}" -k "https://localhost:9200"
```

</details>

### CREATE (EXAMPLE) INDEX LIFECYCLE POLICY

<details><summary><b>CREATE W/ CURL</b></summary>

```json
curl --insecure -u "elastic:${ELASTIC_PASSWORD}" -X PUT "https://localhost:9200/_ilm/policy/rollover-metricbeat?pretty" -H 'Content-Type: application/json' -d'
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_age": "14d",
            "max_primary_shard_size": "50gb",
            "max_size": "3gb"
          },
          "set_priority": {
            "priority": 100
          }
        },
        "min_age": "0ms"
      },
      "cold": {
        "min_age": "14d",
        "actions": {
          "set_priority": {
            "priority": 0
          },
          "freeze": {}
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}'
```

</details>

## EXPORT/IMPORT DASHBOARDS FROM/TO KIBANA

### EXPORT

```bash
curl http://10.31.103.144:32241/s/sthings/api/kibana/dashboards/export?dashboard=314b4030-d936-11ed-9bb1-4bda85068abe > export.json
```

### IMPORT

```bash
curl -k -H "Content-Type: application/json" \
-H "kbn-xsrf: true" https://kibana.dev2.sthings-pve.labul.sva.de/s/sthings/api/kibana/dashboards/import 20 \
--data-binary @export.json
```

### FILEBEAT

[filebeat-kubernetes](https://stackoverflow.com/questions/60566173/how-we-can-filter-namespace-in-filebeat-kubernetes)
[filebeat-kubernetes](https://faun.pub/eck-logging-11017202cb19)
