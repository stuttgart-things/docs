# stuttgart-things/docs/elastic

## SNIPPETS

<details><summary><b>FILEBEAT TO LOGSTASH TEST CONFIG</b></summary>

```yaml
filebeat.inputs:
  - type: log
    paths:
      - /home/sthings/projects/stuttgart-things/helm/eck/logstash-tutorial.log

output.logstash:
  hosts: ["10.31.103.22:5044"]
```

</details>

<details><summary><b>TEST FILEBEAT OUTPUT</b></summary>

```yaml
sudo cp filebeat.yml /etc/filebeat/filebeat.yml
sudo filebeat test output
```

</details>

<details><summary><b>TEST FILEBEAT OUTPUT</b></summary>

```yaml
sudo cp filebeat.yml /etc/filebeat/filebeat.yml
sudo filebeat test output
```

</details>

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

<details><summary><b>CR METRICBEAT - VSPHERE MON</b></summary>

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

<details><summary><b>CR METRICBEAT - CLUSTER MONITORING</b></summary>

```yaml
---
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: metricbeat
  namespace: elastic-system
spec:
  type: metricbeat
  version: 8.9.2
  elasticsearchRef:
    name: elasticsearch-cluster
  kibanaRef:
    name: kibana
  config:
    metricbeat:
      autodiscover:
        providers:
          - hints:
              default_config: {}
              enabled: "true"
            node: ${NODE_NAME}
            type: kubernetes
      modules:
        - module: system
          period: 10s
          metricsets:
            - cpu
            - load
            - memory
            - network
            - process
            - process_summary
          process:
            include_top_n:
              by_cpu: 5
              by_memory: 5
          processes:
            - .*
        - module: system
          period: 1m
          metricsets:
            - filesystem
            - fsstat
          processors:
            - drop_event:
                when:
                  regexp:
                    system:
                      filesystem:
                        mount_point: ^/(sys|cgroup|proc|dev|etc|host|lib)($|/)
        - module: kubernetes
          period: 10s
          node: ${NODE_NAME}
          hosts:
            - https://${NODE_NAME}:10250
          bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
          ssl:
            verification_mode: none
          metricsets:
            - node
            - system
            - pod
            - container
            - volume
        - module: prometheus
          period: 10s
          hosts:
            - http://tekton-pipelines-controller.tekton-pipelines:9090
          metrics_path: /metrics
    processors:
      - add_cloud_metadata: {}
      - add_host_metadata: {}
  daemonSet:
    podTemplate:
      spec:
        serviceAccountName: metricbeat
        automountServiceAccountToken: true # some older Beat versions are depending on this settings presence in k8s context
        containers:
          - args:
              - -e
              - -c
              - /etc/beat.yml
              - -system.hostfs=/hostfs
            name: metricbeat
            volumeMounts:
              - mountPath: /hostfs/sys/fs/cgroup
                name: cgroup
              - mountPath: /var/run/docker.sock
                name: dockersock
              - mountPath: /hostfs/proc
                name: proc
            env:
              - name: NODE_NAME
                valueFrom:
                  fieldRef:
                    fieldPath: spec.nodeName
        dnsPolicy: ClusterFirstWithHostNet
        hostNetwork: true # Allows to provide richer host metadata
        securityContext:
          runAsUser: 0
        terminationGracePeriodSeconds: 30
        volumes:
          - hostPath:
              path: /sys/fs/cgroup
            name: cgroup
          - hostPath:
              path: /var/run/docker.sock
            name: dockersock
          - hostPath:
              path: /proc
            name: proc
---
# permissions needed for metricbeat
# source: https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-module-kubernetes.html
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: metricbeat
rules:
  - apiGroups:
      - ""
    resources:
      - nodes
      - namespaces
      - events
      - pods
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - "extensions"
    resources:
      - replicasets
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - apps
    resources:
      - statefulsets
      - deployments
      - replicasets
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - nodes/stats
    verbs:
      - get
  - nonResourceURLs:
      - /metrics
    verbs:
      - get
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: metricbeat
  namespace: elastic-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: metricbeat
subjects:
  - kind: ServiceAccount
    name: metricbeat
    namespace: elastic-system
roleRef:
  kind: ClusterRole
  name: metricbeat
  apiGroup: rbac.authorization.k8s.io
```

</details>

<details><summary><b>CR FILEBEAT - CLUSTER LOGGING</b></summary>

[filebeat-kubernetes](https://stackoverflow.com/questions/60566173/how-we-can-filter-namespace-in-filebeat-kubernetes)
[filebeat-kubernetes](https://faun.pub/eck-logging-11017202cb19)

```yaml
---
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: filebeat
  namespace: elastic-system
spec:
  type: filebeat
  version: 8.9.2
  elasticsearchRef:
    name: elasticsearch-cluster
  kibanaRef:
    name: kibana
  config:
    filebeat:
      autodiscover:
        providers:
          - type: kubernetes
            node: ${HOSTNAME}
            hints:
              enabled: true
              default_config:
                type: container
                paths:
                  - /var/log/containers/*${data.kubernetes.container.id}.log
    processors:
      - add_cloud_metadata: {}
      - add_host_metadata: {}
  daemonSet:
    podTemplate:
      spec:
        serviceAccountName: filebeat
        automountServiceAccountToken: true
        terminationGracePeriodSeconds: 30
        dnsPolicy: ClusterFirstWithHostNet
        hostNetwork: true # Allows to provide richer host metadata
        containers:
          - name: filebeat
            ports:
              - containerPort: 5066
                name: monitoring
                protocol: TCP
            securityContext:
              runAsUser: 0
              # If using Red Hat OpenShift uncomment this:
              #privileged: true
            volumeMounts:
              - name: varlogcontainers
                mountPath: /var/log/containers
              - name: varlogpods
                mountPath: /var/log/pods
              - name: varlibdockercontainers
                mountPath: /var/lib/docker/containers
            env:
              - name: NODE_NAME
                valueFrom:
                  fieldRef:
                    fieldPath: spec.nodeName
        volumes:
          - name: varlogcontainers
            hostPath:
              path: /var/log/containers
          - name: varlogpods
            hostPath:
              path: /var/log/pods
          - name: varlibdockercontainers
            hostPath:
              path: /var/lib/docker/containers
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: filebeat
rules:
  - apiGroups: [""] # "" indicates the core API group
    resources:
      - namespaces
      - pods
      - nodes
    verbs:
      - get
      - watch
      - list
  - apiGroups: ["apps"]
    resources:
      - replicasets
    verbs:
      - get
      - list
      - watch
  - apiGroups: ["batch"]
    resources:
      - jobs
    verbs:
      - get
      - list
      - watch
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: filebeat
  namespace: elastic-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: filebeat
subjects:
  - kind: ServiceAccount
    name: filebeat
    namespace: elastic-system
roleRef:
  kind: ClusterRole
  name: filebeat
  apiGroup: rbac.authorization.k8s.io
```

</details>

### ELK DOCKER-COMPOSE + PYTHON BULK INGEST (TEST DATA)

<details><summary><b>ELK</b></summary>

```bash
git clone https://github.com/deviantony/docker-elk.git
nerdctl/docker-compose up
# FOR NERDCTL CHANGE: restart: always IN WHOLE
```

</details>

<details><summary><b>BULK INGEST</b></summary>

```python
#!/usr/bin/env python
# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

"""Script that downloads a public dataset and streams it to an Elasticsearch cluster"""

import csv
from os.path import abspath, join, dirname, exists
import tqdm
import urllib3
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk


NYC_RESTAURANTS = (
    "https://data.cityofnewyork.us/api/views/43nn-pn8j/rows.csv?accessType=DOWNLOAD"
)
DATASET_PATH = join(dirname(abspath(__file__)), "nyc-restaurants.csv")
CHUNK_SIZE = 16384


def download_dataset():
    """Downloads the public dataset if not locally downlaoded
    and returns the number of rows are in the .csv file.
    """
    if not exists(DATASET_PATH):
        http = urllib3.PoolManager()
        resp = http.request("GET", NYC_RESTAURANTS, preload_content=False)

        if resp.status != 200:
            raise RuntimeError("Could not download dataset")

        with open(DATASET_PATH, mode="wb") as f:
            chunk = resp.read(CHUNK_SIZE)
            while chunk:
                f.write(chunk)
                chunk = resp.read(CHUNK_SIZE)

    with open(DATASET_PATH) as f:
        return sum([1 for _ in f]) - 1


def create_index(client):
    """Creates an index in Elasticsearch if one isn't already there."""
    client.indices.create(
        index="nyc-restaurants",
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "borough": {"type": "keyword"},
                    "cuisine": {"type": "keyword"},
                    "grade": {"type": "keyword"},
                    "location": {"type": "geo_point"},
                }
            },
        },
        ignore=400,
    )


def generate_actions():
    """Reads the file through csv.DictReader() and for each row
    yields a single document. This function is passed into the bulk()
    helper to create many documents in sequence.
    """
    with open(DATASET_PATH, mode="r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            doc = {
                "_id": row["CAMIS"],
                "name": row["DBA"],
                "borough": row["BORO"],
                "cuisine": row["CUISINE DESCRIPTION"],
                "grade": row["GRADE"] or None,
            }

            lat = row["Latitude"]
            lon = row["Longitude"]
            if lat not in ("", "0") and lon not in ("", "0"):
                doc["location"] = {"lat": float(lat), "lon": float(lon)}
            yield doc


def main():
    print("Loading dataset...")
    number_of_docs = download_dataset()

    client = Elasticsearch(
              "http://cleveland.labul.sva.de:9200",
              verify_certs=False,
              basic_auth=('elastic', 'changeme')
            )
    client.info()

    print("Creating an index...")
    create_index(client)

    print("Indexing documents...")
    progress = tqdm.tqdm(unit="docs", total=number_of_docs)
    successes = 0
    for ok, action in streaming_bulk(
        client=client, index="nyc-restaurants", actions=generate_actions(),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, number_of_docs))


if __name__ == "__main__":
    main()
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
curl --insecure -u "elastic:${ELASTIC_PASSWORD}" -X PUT "https://localhost:9200/_ilm/policy/metricbeat?pretty" -H 'Content-Type: application/json' -d'
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_age": "2d",
            "max_primary_shard_size": "1gb",
            "max_size": "3gb"
          },
          "set_priority": {
            "priority": 100
          }
        },
        "min_age": "0ms"
      },
      "delete": {
        "min_age": "3d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}'
```

</details>

<details><summary><b>EXPORT/IMPORT DASHBOARDS FROM/TO KIBANA</b></summary>

```bash
# EXPORT
curl http://10.31.103.144:32241/s/sthings/api/kibana/dashboards/export?dashboard=314b4030-d936-11ed-9bb1-4bda85068abe > export.json
```

```bash
# IMPORT
curl -k -H "Content-Type: application/json" \
-H "kbn-xsrf: true" https://kibana.dev2.sthings-pve.labul.sva.de/s/sthings/api/kibana/dashboards/import 20 \
--data-binary @export.json
```
</details>
