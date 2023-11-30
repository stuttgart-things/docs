# stuttgart-things/docs/crossplane

##  Terminology

| KIND  | DESCRIPTION                                                          |
|----------|----------------------------------------------------------------------|
| Provider       | enable Crossplane to provision infrastructure on an external service |
| ProviderConfig | each Provider package has its own configuration type |
| Composition | Terraform fanboys might think of a Composition as a Terraform module - the HCL code that describes how to take input variables and use them to create resources in some cloud - Helm fanboys might think of a Composition as a Helm chart's templates; the moustache templated YAML files that describe how to take Helm chart values and render Kubernetes resources |
| CompositeResourceDefinition | There isn't a direct analog to XRDs in the Helm ecosystem, but they're a little bit like the variable blocks in a Terraform module that define which variables exist, whether those variables are strings or integers, whether they're required or optional, etc. |
| Composite Resource Claim  | Claims map to the same concepts as described above under the composite resource heading; i.e. tfvars files and Helm values.yaml files. Imagine that some tfvars files and some values.yaml files were only accessible to the platform team while others were offered to application teams; that's the difference between a composite resource and a claim. |


## CLI INSTALLATION

```bash
curl -sL "https://raw.githubusercontent.com/crossplane/crossplane/master/install.sh" | sh
sudo mv crossplane /usr/local/bin
```

## DEPLOYMENT W/ HELM

```bash
kubectl create namespace crossplane-system
helm repo add crossplane-stable https://charts.crossplane.io/stable && helm repo update

helm upgrade --install crossplane --wait \
--namespace crossplane-system \
crossplane-stable/crossplane --version 1.14.3

kubectl api-resources | grep upbound
```

## EXAMPLE HELM PROVIDER

### DEPLOY HELM PROVIDER

```bash
kubectl apply -f - <<EOF
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-helm
spec:
  package: "crossplanecontrib/provider-helm:master"
EOF
```

### IN-CLUSTER PROVIDER CONFIGURATION

DEPLOY HELM RELEASES ON THE SAME CLUSTER CROSSPLANE IS RUNNING ON

```bash
SA=$(kubectl -n crossplane-system get sa -o name | grep provider-helm | sed -e 's|serviceaccount\/|crossplane-system:|g')
kubectl create clusterrolebinding provider-helm-admin-binding --clusterrole cluster-admin --serviceaccount="${SA}"

kubectl apply -f - <<EOF
apiVersion: helm.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: helm-provider
spec:
  credentials:
    source: InjectedIdentity
EOF
```

### DEPLOY RELEASE

```bash
kubectl apply -f - <<EOF
apiVersion: helm.crossplane.io/v1beta1
kind: Release
metadata:
  name: wordpress-example
spec:
  forProvider:
    chart:
      name: wordpress
      repository: https://charts.bitnami.com/bitnami
      version: 15.2.5 ## To use devlopment versions, set ">0.0.0-0"
#     url: "https://charts.bitnami.com/bitnami/wordpress-9.3.19.tgz"
    namespace: wordpress
    insecureSkipTLSVerify: true
    skipCreateNamespace: true
    wait: true
    skipCRDs: true
    values:
      service:
        type: ClusterIP
  providerConfigRef:
    name: helm-provider
EOF
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
