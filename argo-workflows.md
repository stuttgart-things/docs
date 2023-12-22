# ARGO-WORKFLOWS

## INSTALL CLI

<details><summary><b>CLI INSTALLATION LINUX</b></summary>

```bash
curl -sLO https://github.com/argoproj/argo-workflows/releases/download/v3.5.2/argo-linux-amd64.gz
gunzip argo-linux-amd64.gz
chmod +x argo-linux-amd64
mv ./argo-linux-amd64 /usr/bin/argo
argo version
```

</details>

## HELM DEPLOYMENT

```bash
workflow:
  serviceAccount:
    create: true
    name: argo-workflows
controller:
  workflowNamespaces:
    - default
    - argo-workflows
  workflowDefaults:
    spec:
      serviceAccountName: argo-workflows
```


## WORKFLOW EXAMPLES

<details><summary><b>EXAMPLE WORKFLOW</b></summary>

```bash
kubectl -n argo-workflows apply -f - <<EOF
---
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: hello-workflows
spec:
  entrypoint: hello-workflows
  serviceAccountName: argo-workflows
  templates:
    - name: hello-workflows
      container:
        image: alpine:3.15
        command: ["echo", "Hello, workflows!"]
        resources:
          limits:
            memory: 32Mi
            cpu: 100m
  steps:
    - - name: hello-world
EOF
```

</details>
