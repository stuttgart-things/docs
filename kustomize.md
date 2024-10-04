# stuttgart-things/docs/kustomize

## SNIPPETS

<details><summary><b>ADD OBJECT TO AN ARRAY</b></summary>

```bash
BASE_DIR=./kustomize/crb
mkdir -p ${BASE_DIR}

cat <<EOF > ${BASE_DIR}/crb.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects: []
EOF

cat <<EOF > ${BASE_DIR}/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - crb.yaml
patches:
  - target:
      kind: ClusterRoleBinding
      name: binding
    patch: |
      - op: add
        path: /subjects/0
        value:
          kind: ServiceAccount
          name: name
          namespace: test1
  - target:
      kind: ClusterRoleBinding
      name: binding
    patch: |
      - op: add
        path: /subjects/1
        value:
          kind: ServiceAccount
          name: name
          namespace: test2
EOF

kubectl kustomize ${BASE_DIR}
```

</details>

<details><summary><b>CONFIGMAP GENERATOR W/ POD-MOUNT</b></summary>

```bash
BASE_DIR=./kustomize/config
mkdir -p ${BASE_DIR}

cat <<EOF > ${BASE_DIR}/kustomization.yaml
---
resources:
  - importer-job.yaml
configMapGenerator:
  - name: revisionruns
    files:
      - prime.json
patches:
  - target:
      kind: Pod
    patch: |-
      - op: replace
        path: /metadata/name
        value: revisionrun-importer
EOF

cat <<EOF > ${BASE_DIR}/importer-job.yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: stagetime-grpc-call
spec:
  containers:
    - name: grpc-call-incluster
      image: scr.cd43.sthings-pve.labul.sva.de/stagetime-server/stagetime-server:24.0124.0744-v0.4.41
      volumeMounts:
        - name: revisionruns
          mountPath: /revisionruns
      command: ['grpcCall']
      env:
        - name: STAGETIME_SERVER
          value: "stagetime-server-service.stagetime.svc.cluster.local:80"
          #value: "stagetime.cd43.sthings-pve.labul.sva.de:443"
        - name: STAGETIME_TEST_FILES
          value: "/revisionruns/prime.json"
  volumes:
    - name: revisionruns
      configMap:
        name: revisionruns
  restartPolicy: Never
EOF

cat <<EOF > ${BASE_DIR}/prime.json
{
    "repo_name": "stuttgart-things",
    "pushed_at": "2024-01-13T13:40:36Z",
    "author": "patrick-hermann-sva",
    "repo_url": "https://codehub.sva.de/Lab/stuttgart-things/stuttgart-things.git",
    "commit_id": "000000005",
    "pipelineruns": [
      {
        "name": "simulate-stagetime",
        "canfail": true,
        "stage": 0,
        "resolverParams": "url=https://github.com/stuttgart-things/stuttgart-things.git, revision=main, pathInRepo=stageTime/pipelines/simulate-stagetime-pipelineruns.yaml",
        "params": "gitRevision=main, gitRepoUrl=https://github.com/stuttgart-things/stageTime-server.git, gitWorkspaceSubdirectory=stageTime, scriptPath=tests/prime.sh, scriptTimeout=25s",
        "listparams": "",
        "volumeClaimTemplates": "source=openebs-hostpath;ReadWriteOnce;20Mi"
      }
   ]
}
EOF
```

</details>

<details><summary><b>PATCH INGRESS W/ REPLACE</b></summary>

```bash
BASE_DIR=./kustomize/ingress
mkdir -p ${BASE_DIR}

cat <<EOF > ${BASE_DIR}/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ingress.yaml

patches:
  - target:
      kind: Ingress
      name: ingress
    patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: stuttgart-things.com
EOF

cat <<EOF > ${BASE_DIR}/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress
spec:
  ingressClassName: alb
  rules:
    - host: app.whatever.com
      http:
        paths:
        - backend:
            service:
             name: web
             port:
              number: 80
          pathType: ImplementationSpecific
EOF
```

</details>

<details><summary><b>RENDER/APPLY</b></summary>

```bash
# RENDER TO STDOUT
kubectl kustomize ${BASE_DIR}

# APPLY TO K8S
kubectl apply -k .
```

</details>
