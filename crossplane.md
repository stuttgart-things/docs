# stuttgart-things/docs/crossplane

##  Terminology

| CONCEPT  | DESCRIPTION                                                          |
|----------|----------------------------------------------------------------------|
| provider | enable Crossplane to provision infrastructure on an external service |


## DEPLOYMENT W/ HELM

```bash
kubectl create namespace crossplane-system
helm repo add crossplane-stable https://charts.crossplane.io/stable && helm repo update

helm upgrade --install crossplane --wait \
--namespace crossplane-system \
crossplane-stable/crossplane --version 1.14.1

kubectl api-resources | grep upbound
```

## EXAMPLE TERRAFORM PROVIDER (KUBERNETES EXAMPLE)

### DEPLOY TERRAFORM PROVIDER

```bash
kubectl apply -f - <<EOF
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-terraform
spec:
  package: xpkg.upbound.io/upbound/provider-terraform:v0.11.0
EOF

kubectl apply -f - <<EOF
apiVersion: tf.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: terraform-default
spec:
  configuration: |
    terraform {
      backend "kubernetes" {
        secret_suffix     = "providerconfig-default"
        namespace         = "crossplane-system"
        in_cluster_config = true
      }
    }
EOF

TERRAFORM_SERVICE_ACCOUNT=$(kubectl -n crossplane-system get sa -ojson | jq -r '.items | map(.metadata.name | select(startswith("provider-terraform"))) | .[0]')

kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: crossplane:provider:provider-terraform
rules:
- apiGroups:
  - ""
  - "apps"
  - "extensions"
  - "networking.k8s.io"
  resources:
  - "namespaces"
  - "ingresses"
  - "services"
  - "deployments"
  verbs:
  - "*"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: crossplane:provider:provider-terraform
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: crossplane:provider:provider-terraform
subjects:
- kind: ServiceAccount
  name: ${TERRAFORM_SERVICE_ACCOUNT}
  namespace: crossplane-system
EOF
```

### CREATE SAMPLE CRD

```bash
kubectl apply -f - <<EOF
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xnginxapps.examples.stuttgart-things.com
spec:
  group: examples.stuttgart-things.com
  names:
    kind: XNginxApp
    plural: xnginxapps
  claimNames:
    kind: NginxApp
    plural: nginxapps
  versions:
  - name: v1alpha1
    served: true
    referenceable: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              env:
                type: string
EOF
```

### CREATE SAMPLE COMPOSITION

```bash
kubectl apply -f - <<EOF
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: nginx-app
  labels:
    crossplane.io/xrd: xnginxapps.examples.stuttgart-things.com
spec:
  compositeTypeRef:
    apiVersion: examples.stuttgart-things.com/v1alpha1
    kind: XNginxApp
  resources:
  - name: nginx-app
    base:
      kind: Workspace
      apiVersion: tf.upbound.io/v1beta1
      metadata:
        annotations:
          crossplane.io/external-name: default
      spec:
        providerConfigRef:
          name: terraform-default
        forProvider:
          source: Remote
          module: git::https://github.com/stuttgart-things/stuttgart-things.git//terraform/nginx-k8s-app?ref=main
          vars:
          - key: environment
    patches:
    - type: FromCompositeFieldPath
      fromFieldPath: spec.env
      toFieldPath: spec.forProvider.vars[0].value
EOF
```

### CREATE SAMPLE CLAIM

```bash
kubectl apply -f - <<EOF
apiVersion: examples.stuttgart-things.com/v1alpha1
kind: NginxApp
metadata:
  name: nginx-app-staging
spec:
  env: stag1
  compositionRef:
    name: nginx-app
EOF
```

### VERIFY

```bash
kubectl get NginxApp
```
