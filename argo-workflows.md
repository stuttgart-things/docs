# stuttgart-things/docs/argo-workflows

## CREATE ACCESS TOKEN

<details><summary><b>EXAMPLE TOKEN CREATION</b></summary>

```bash
TOKEN_NAME=workflows
kubectl create role ${TOKEN_NAME} --verb=list,update --resource=workflows.argoproj.io
kubectl create sa ${TOKEN_NAME}
kubectl create rolebinding ${TOKEN_NAME} --role=workflows --serviceaccount=argo:workflows

kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: ${TOKEN_NAME}.service-account-token
  annotations:
    kubernetes.io/service-account.name: workflows
type: kubernetes.io/service-account-token
EOF

ARGO_TOKEN="Bearer $(kubectl get secret ${TOKEN_NAME}.service-account-token -o=jsonpath='{.data.token}' | base64 --decode)"
echo ${ARGO_TOKEN}
```

</details>

## INSTALL CLI

<details><summary><b>LINUX</b></summary>

```bash
curl -sLO https://github.com/argoproj/argo-workflows/releases/download/v3.5.2/argo-linux-amd64.gz
gunzip argo-linux-amd64.gz
chmod +x argo-linux-amd64
mv ./argo-linux-amd64 /usr/bin/argo
argo version
```

</details>

## HELM DEPLOYMENT

<details><summary><b>DEPLOYMENT + VALUES</b></summary>

```bash
helm repo add argo https://argoproj.github.io/argo-helm

cat <<EOF > argo-workflows.yaml
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
EOF

helm upgrade --install argo-workflows argo/argo-workflows --version 0.40.1 --values argo-workflows.yaml -n argo-workflows --create-namespace
```

</details>

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

argo list -n argo-workflows
argo logs hello-workflows -n argo-workflows
```

</details>


# WORKFLOW TEMPLATE TRIGGERED BY EVENT


https://argoproj.github.io/argo-workflows/events/

## WORKFLOW-TEMPLATE

```yaml
apiVersion: argoproj.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: my-wf-tmple
  namespace: argo
spec:
  templates:
    - name: main
      inputs:
        parameters:
          - name: message
            value: "{{workflow.parameters.message}}"
      container:
        image: docker/whalesay:latest
        command: [cowsay]
        args: ["{{inputs.parameters.message}}"]
  entrypoint: main
```

## WORKFLOW-EVENT-BINDING

```yaml
apiVersion: argoproj.io/v1alpha1
kind: WorkflowEventBinding
metadata:
  name: event-consumer
spec:
  event:
    # metadata header name must be lowercase to match in selector
    selector: payload.message != "" && metadata["x-argo-e2e"] == ["true"] && discriminator == "my-discriminator"
  submit:
    workflowTemplateRef:
      name: my-wf-tmple
    arguments:
      parameters:
      - name: message
        valueFrom:
          event: payload.message
```
