# stuttgart-things/docs/crossplane

## KOMOPLANE

<details><summary><b>DEPLOYMENT</b></summary>

```bash
helm repo add komodorio https://helm-charts.komodor.io && helm repo update
helm upgrade --install komoplane komodorio/komoplane -n komoplane --create-namespace
```

</details>

<details><summary><b>UI ACCESS</b></summary>

```bash
export POD_NAME=$(kubectl get pods --namespace komoplane -l "app.kubernetes.io/name=komoplane,app.kubernetes.io/instance=komoplane" -o jsonpath="{.items[0].metadata.name}")
export CONTAINER_PORT=$(kubectl get pod --namespace komoplane $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
kubectl --namespace komoplane port-forward $POD_NAME 8090:$CONTAINER_PORT
```

</details>

## FUNCTIONS

<details><summary><b>REQUIREMENTS</b></summary>

```bash
curl -sL "https://raw.githubusercontent.com/crossplane/crossplane/master/install.sh" | sh
sudo mv crossplane /usr/local/bin
# Docker also needs to be installed
```

</details>

<details><summary><b>PATCH-AND-TRANSFORM</b></summary>

```bash
cat <<EOF > ./functions.yaml
---
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-patch-and-transform
spec:
  package: xpkg.upbound.io/crossplane-contrib/function-patch-and-transform:v0.1.4
EOF
```

```bash
cat <<EOF > ./composition.yaml
---
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: function-patch-and-transform
spec:
  compositeTypeRef:
    apiVersion: example.crossplane.io/v1
    kind: XR
  mode: Pipeline
  pipeline:
  - step: patch-and-transform
    functionRef:
      name: function-patch-and-transform
    input:
      apiVersion: pt.fn.crossplane.io/v1beta1
      kind: Resources
      resources:
      - name: bucket
        base:
          apiVersion: s3.aws.upbound.io/v1beta1
          kind: Bucket
        patches:
        - type: FromCompositeFieldPath
          fromFieldPath: "spec.location"
          toFieldPath: "spec.forProvider.region"
          transforms:
          - type: map
            map:
              DE: "frankfurt"
EOF
```

```bash
cat <<EOF > ./composition.yaml
---
apiVersion: example.crossplane.io/v1
kind: XR
metadata:
  name: example-xr1
specd :
  location: US
```

```bash
crossplane beta render xr.yaml composition.yaml function.yaml
```

</details>

## TERMINOLOGY

<details><summary><b>OVERVIEW</b></summary>

| KIND                        | DESCRIPTION                                                                                                                                                                                                                                                                                                                                                           |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Provider                    | enable Crossplane to provision infrastructure on an external service                                                                                                                                                                                                                                                                                                  |
| ProviderConfig              | each Provider package has its own configuration type                                                                                                                                                                                                                                                                                                                  |
| Composition                 | Terraform fanboys might think of a Composition as a Terraform module - the HCL code that describes how to take input variables and use them to create resources in some cloud - Helm fanboys might think of a Composition as a Helm chart's templates; the moustache templated YAML files that describe how to take Helm chart values and render Kubernetes resources |
| CompositeResourceDefinition | There isn't a direct analog to XRDs in the Helm ecosystem, but they're a little bit like the variable blocks in a Terraform module that define which variables exist, whether those variables are strings or integers, whether they're required or optional, etc.                                                                                                     |
| Composite Resource Claim    | Claims map to the same concepts as described above under the composite resource heading; i.e. tfvars files and Helm values.yaml files. Imagine that some tfvars files and some values.yaml files were only accessible to the platform team while others were offered to application teams; that's the difference between a composite resource and a claim.            |

</details>

## DEPLOYMENT

<details><summary><b>CLI INSTALLATION</b></summary>

```bash
curl -sL "https://raw.githubusercontent.com/crossplane/crossplane/master/install.sh" | sh
sudo mv crossplane /usr/local/bin
```

</details>

<details><summary><b>DEPLOYMENT W/ HELM</b></summary>

[provider-helm](https://github.com/crossplane-contrib/provider-helm/tree/master)

```bash
kubectl create namespace crossplane-system
helm repo add crossplane-stable https://charts.crossplane.io/stable && helm repo update

helm upgrade --install crossplane --wait \
--namespace crossplane-system \
crossplane-stable/crossplane --version 1.14.5

kubectl api-resources | grep upbound
```

</details>

<details><summary><b>TROUBLESHOOTING</b></summary>

```bash
# DEBUG PROVIDER RELATED ISSUES
kubectl describe providerrevisions

# GET PACKAGE REVISION
kubectl get pkgrev

# LIST PROVIDERS
kubectl get providers.pkg.crossplane.io -A

# DEBUG/TRACE XRD W/ CROSSPLANE CLI
crossplane beta trace metallbconfig labda-test -n crossplane-system -o wide # EXAMPLE
```

</details>

<details><summary><b>ADD CUSTOM-CA</b></summary>

```yaml
# CABUNDLE AS CM
apiVersion: v1
kind: ConfigMap
metadata:
  name: cert-bundle
  namespace: crossplane-system
data:
  ca-certificates.crt: |-
    -----BEGIN CERTIFICATE-----
    MIIFijCCA3KgAwIBA #..
```

```yaml
# CONTROLLER CONFIG
apiVersion: pkg.crossplane.io/v1alpha1
kind: ControllerConfig
metadata:
  name: cert-bundle
spec:
  volumeMounts:
    - name: cert-bundle
      mountPath: /etc/ssl/certs
  volumes:
    - name: cert-bundle
      configMap:
        name: cert-bundle
  envFrom:
    - secretRef:
        name: s3
```

```yaml
# CONTROLLER REF
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-terraform
spec:
  package: xpkg.upbound.io/upbound/provider-terraform:v0.13.0
  controllerConfigRef:
    name: cert-bundle
```

</details>

## GENERAL

<details><summary>COMPOSITION PATCHES</summary>

```yaml
# FROMCOMPOSITEFIELDPATH
- type: FromCompositeFieldPath
  fromFieldPath: spec.tfvars.secretNamespace
  toFieldPath: spec.forProvider.varFiles[0].secretKeyRef.namespace
```

```yaml
# COMBINEFROMCOMPOSITE
- type: CombineFromComposite
  combine:
    variables:
      - fromFieldPath: spec.group
      - fromFieldPath: spec.repository
    strategy: string
    string:
      fmt: "https://github.com/%s/%s"
  toFieldPath: spec.forProvider.values.githubConfigUrl
```

</details>

<details><summary>PATCHES</summary>

```bash
https://github.com/crossplane/crossplane/issues/2072
https://vrelevant.net/crossplane-composition-patches-combine-patches/
https://vrelevant.net/crossplane-composition-patches-fromcompositefieldpath/
```

</details>

<details><summary>ATPROVIDER STATUS BETWEEN RESOURCES + TRANSFORMATION PATCH</summary>

```yaml
resources:
  - name: vsphere-vm
    base:
# ..
output "ip" {
  value = [module.vsphere-vm.ip]
}
# ..
patches:
  - type: ToCompositeFieldPath
    fromFieldPath: status.atProvider.outputs.ip
    toFieldPath: status.share.vmIP
    policy:
      fromFieldPath: Required
# ..
- name: test-config
  base:
# ..
data:
  database_host: "192.168.0.1"
# ..
patches:
  - fromFieldPath: status.share.vmIP
    toFieldPath: spec.forProvider.manifest.data.database_host
    policy:
      fromFieldPath: Required
    transforms:
      - type: string
        string:
          type: Join
          join:
            separator: ","
```

</details>

## KUBERNETES PROVIDER

<details><summary>KUBERNETES PROVIDER INSTALLATION</summary>

```bash
kubectl apply -f - <<EOF
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-kubernetes
spec:
  package: "crossplanecontrib/provider-kubernetes:v0.11.2" # main for latest
EOF
```

</details>

<details><summary>PROVIDER CONFIG (KUBECONFIG)</summary>

```bash
# CREATE KUBECONFIG SECRET FROM LOCAL FILE
kubectl -n crossplane-system create secret generic kubeconfig-dev43 --from-file=/home/sthings/.kube/pve-dev43
```

```bash
kubectl apply -f - <<EOF
apiVersion: kubernetes.crossplane.io/v1alpha1
kind: ProviderConfig
metadata:
  name: kubernetes-dev43
spec:
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: kubeconfig-dev43
      key: pve-dev43
EOF
```

</details>

<details><summary>PROVIDER CONFIG (INCLUSTER)</summary>

```bash
kubectl apply -f - <<EOF
apiVersion: kubernetes.crossplane.io/v1alpha1
kind: ProviderConfig
metadata:
  name: kubernetes-incluster
spec:
  credentials:
    source: InjectedIdentity
EOF
```

```bash
# ADDC SERVICE ACCOUNT CLUSTERROLEBINDING
SA=$(kubectl -n crossplane-system get sa -o name | grep provider-kubernetes | sed -e 's|serviceaccount\/|crossplane-system:|g')
kubectl create clusterrolebinding provider-kubernetes-admin-binding --clusterrole cluster-admin --serviceaccount="${SA}"
```

</details>

<details><summary>OBJECT EXAMPLES</summary>

```bash
kubectl apply -f - <<EOF
apiVersion: kubernetes.crossplane.io/v1alpha2
kind: Object
metadata:
  name: sample-namespace
spec:
  forProvider:
    manifest:
      apiVersion: v1
      kind: Namespace
      metadata:
        labels:
          example: "true"
  providerConfigRef:
    name: kubernetes-dev43
EOF
```

```bash
kubectl apply -f - <<EOF
apiVersion: kubernetes.crossplane.io/v1alpha2
kind: Object
metadata:
  name: sandiego-rke2
spec:
  providerConfigRef:
    name: kubernetes-labul-bootstrap
  forProvider:
    manifest:
      apiVersion: tekton.dev/v1
      kind: PipelineRun
      metadata:
        namespace: tektoncd
      spec:
        pipelineRef:
          resolver: git
          params:
            - name: url
              value: https://github.com/stuttgart-things/stuttgart-things.git
            - name: revision
              value: rancher-280
            - name: pathInRepo
              value: stageTime/pipelines/execute-ansible-playbooks.yaml
        workspaces:
          - name: shared-workspace
            volumeClaimTemplate:
              spec:
                storageClassName: openebs-hostpath
                accessModes:
                  - ReadWriteOnce
                resources:
                  requests:
                    storage: 20Mi
        params:
          - name: ansibleWorkingImage
            value: "eu.gcr.io/stuttgart-things/sthings-ansible:9.1.0"
          - name: createInventory
            value: "true"
          - name: gitRepoUrl
            value: https://github.com/stuttgart-things/stuttgart-things.git
          - name: gitRevision
            value: "rancher-280"
          - name: gitWorkspaceSubdirectory
            value: "/ansible/rke2"
          - name: vaultSecretName
            value: vault
          - name: installExtraRoles
            value: "true"
          - name: ansibleExtraRoles
            value:
              - "https://github.com/stuttgart-things/install-requirements.git"
              - "https://github.com/stuttgart-things/manage-filesystem.git"
              - "https://github.com/stuttgart-things/install-configure-vault.git"
              - "https://github.com/stuttgart-things/deploy-configure-rke"
          - name: ansiblePlaybooks
            value:
              - "ansible/playbooks/prepare-env.yaml"
              - "ansible/playbooks/base-os.yaml"
              - "ansible/playbooks/deploy-rke2.yaml"
              - "ansible/playbooks/upload-kubeconfig-vault.yaml"
          - name: ansibleVarsFile
            value:
              - "manage_filesystem+-true"
              - "update_packages+-true"
              - "install_requirements+-true"
              - "install_motd+-true"
              - "username+-sthings"
              - "lvm_home_sizing+-'15%'"
              - "lvm_root_sizing+-'35%'"
              - "lvm_var_sizing+-'50%'"
              - "send_to_msteams+-true"
              - "reboot_all+-false"
              - "cluster_name+-sandiego"
              - "rke2_k8s_version+-1.27.7"
              - "rke2_release_kind+-rke2r2"
              - "cluster_setup+-singleode"
              - "target_host+-sandiego.labul.sva.de"
              - "kubeconfig_path+-/etc/rancher/rke2/rke2.yaml"
              - "secret_path_kubeconfig+-kubeconfigs"
              # - "pause_time+-10"
          - name: ansibleVarsInventory
            value:
              - "initial_master_node+[\"sandiego.labul.sva.de\"]"
              - "additional_master_nodes+[\"\"]"
EOF
```

</details>

<details><summary>CRD-EXAMPLES</summary>

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xbaseosruns.resources.stuttgart-things.com
spec:
  connectionSecretKeys:
    - kubeconfig
  group: resources.stuttgart-things.com
  names:
    kind: XBaseOsRun
    plural: xbaseosruns
  claimNames:
    kind: BaseOsRun
    plural: baseosruns
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          description: A BaseOsRun is a composite resource that represents a Tekton PipelineRun provisioning a base setup on a given set of virual machines
          type: object
          properties:
            spec:
              type: object
              properties:
                pipelineRunName:
                  type: string
                  description: Name of pipelineRun resource
                pipelineNamespace:
                  type: string
                  default: tektoncd
                  description: Namespace of pipelineRun resource
              required:
                - pipelineRunName
            status:
              description: A Status represents the observed state
              properties:
                share:
                  description: Freeform field containing status information
                  type: object
                  x-kubernetes-preserve-unknown-fields: true
              type: object
```

<details><summary>STRING-DEFINITION</summary>

```yaml
# STRING
properties:
  spec:
    type: object
    properties:
      pipelineRunName:
        type: string
        description: Name of pipelineRun resource
```

</details>

<details><summary>STRING-ARRAY-DEFINITION</summary>

```yaml
# STRING ARRAY
playbooks:
  type: array
  description: Ansible playbooks
  items:
    type: string
  default:
    - "ansible/playbooks/prepare-env.yaml"
    - "ansible/playbooks/base-os.yaml"
```

</details>

</details>

<details><summary>COMPOSITION EXAMPLES</summary>

```yaml
---
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: baseos-run
  labels:
    crossplane.io/xrd: xbaseosruns.resources.stuttgart-things.com
spec:
  writeConnectionSecretsToNamespace: crossplane-system
  compositeTypeRef:
    apiVersion: resources.stuttgart-things.com/v1alpha1
    kind: XBaseOsRun
  resources:
    - base:
        apiVersion: kubernetes.crossplane.io/v1alpha2
        kind: Object
        spec:
          providerConfigRef:
            name: kubernetes-labul-bootstrap
          forProvider:
            manifest:
              apiVersion: tekton.dev/v1
              kind: PipelineRun
              metadata:
                name: guestbook
                namespace: tektoncd
              spec:
                pipelineRef:
                  resolver: git
                  params:
                    - name: url
                      value: https://github.com/stuttgart-things/stuttgart-things.git
                    - name: revision
                      value: rancher-280
                    - name: pathInRepo
                      value: stageTime/pipelines/execute-ansible-playbooks.yaml
                workspaces:
                  - name: shared-workspace
                    volumeClaimTemplate:
                      spec:
                        storageClassName: openebs-hostpath
                        accessModes:
                          - ReadWriteOnce
                        resources:
                          requests:
                            storage: 20Mi
                params:
                  - name: ansibleWorkingImage
                    value: "eu.gcr.io/stuttgart-things/sthings-ansible:9.1.0"
                  - name: createInventory
                    value: "true"
                  - name: gitRepoUrl
                    value: https://github.com/stuttgart-things/stuttgart-things.git
                  - name: gitRevision
                    value: "rancher-280"
                  - name: gitWorkspaceSubdirectory
                    value: "/ansible/rke2"
                  - name: vaultSecretName
                    value: vault
                  - name: installExtraRoles
                    value: "true"
                  - name: ansibleExtraRoles
                    value:
                      - "https://github.com/stuttgart-things/install-requirements.git"
                      - "https://github.com/stuttgart-things/manage-filesystem.git"
                      - "https://github.com/stuttgart-things/install-configure-vault.git"
                      - "https://github.com/stuttgart-things/deploy-configure-rke"
                  - name: ansiblePlaybooks
                    value:
                      - "ansible/playbooks/prepare-env.yaml"
                      - "ansible/playbooks/base-os.yaml"
                      - "ansible/playbooks/deploy-rke2.yaml"
                      - "ansible/playbooks/upload-kubeconfig-vault.yaml"
                  - name: ansibleVarsFile
                    value:
                      - "manage_filesystem+-true"
                      - "update_packages+-true"
                      - "install_requirements+-true"
                      - "install_motd+-true"
                      - "username+-sthings"
                      - "lvm_home_sizing+-'15%'"
                      - "lvm_root_sizing+-'35%'"
                      - "lvm_var_sizing+-'50%'"
                      - "send_to_msteams+-true"
                      - "reboot_all+-false"
                      - "cluster_name+-sandiego"
                      - "rke2_k8s_version+-1.27.7"
                      - "rke2_release_kind+-rke2r2"
                      - "cluster_setup+-singleode"
                      - "target_host+-sandiego.labul.sva.de"
                      - "kubeconfig_path+-/etc/rancher/rke2/rke2.yaml"
                      - "secret_path_kubeconfig+-kubeconfigs"
                      # - "pause_time+-10"
                  - name: ansibleVarsInventory
                    value:
                      - 'initial_master_node+["sandiego.labul.sva.de"]'
                      - 'additional_master_nodes+[""]'
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.pipelineRunName
          toFieldPath: spec.forProvider.manifest.metadata.name
```

</details>

<details><summary>COMMANDS</summary>

```bash
kubectl get crossplane # GET ALL
kubectl get object -A # GET ALL OBJECTS IN CLUSTER
kubectl get providerconfigusage.kubernetes.crossplane.io # GET PROVIDERUSAGE
kubectl get compositionrevision.apiextensions.crossplane.io -A
kubectl describe compositionrevision.apiextensions.crossplane.io/

# RENDERING PROBLEMS
kubectl get composite
kubectl describe xbaseosrun.resources.stuttgart-things.com/<COMPOSITE-NAME>
```

</details>

## GCP PROVIDER

<details><summary>AZURE PROVIDER INSTALLATION</summary>

```bash
kubectl apply -f - <<EOF
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-gcp-storage
spec:
  package: xpkg.upbound.io/upbound/provider-gcp-storage:v1.2.0
EOF
```

```bash
# https://cloud.google.com/iam/docs/keys-create-delete?hl=de#creating
kubectl create secret generic gcp-secret -n crossplane-system --from-file=creds=../gcp-credentials.json
EOF
```

```bash
cat ../gcp-credentials.json | grep project_id # USE THIS AS PROJECT ID

kubectl apply -f - <<EOF
apiVersion: gcp.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
spec:
  projectID: stuttgart-things
  credentials:
    source: Secret
    secretRef:
      namespace: crossplane-system
      name: gcp-secret
      key: creds
EOF
```

</details>


<details><summary>AZURE PROVIDER INSTALLATION</summary>

```bash
RANDOM_NAME=$(echo "sthings-bucket-"$(head -n 4096 /dev/urandom | openssl sha1 | tail -c 10))

kubectl apply -f - <<EOF
apiVersion: storage.gcp.upbound.io/v1beta1
kind: Bucket
metadata:
  name: example
  labels:
  annotations:
    crossplane.io/external-name: ${RANDOM_NAME}
spec:
  forProvider:
    location: US
    storageClass: MULTI_REGIONAL
  providerConfigRef:
    name: default
  deletionPolicy: Delete
EOF
kubectl get managed
```

## AZURE PROVIDER

<details><summary>AZURE PROVIDER INSTALLATION</summary>

```bash
kubectl apply -f - <<EOF
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-azure-management
spec:
  package: xpkg.upbound.io/upbound/provider-azure-management:v1.2.0
EOF
```
# https://marketplace.upbound.io/providers/upbound/provider-family-azure/v1.2.0/docs/quickstart

# https://github.com/DexterPOSH/crossplane-getting-started/tree/main
</details>

<details><summary>AZURE PROVIDER CONFIGURATION</summary>

```bash
az login --use-device-code

Subscription_ID=28042244-bb51-4cd6-8034-7776fa3703e8
az ad sp create-for-rbac --sdk-auth --role Owner --scopes /subscriptions/${Subscription_ID}


```

</details>



## HELM PROVIDER

<details><summary>HELM PROVIDER INSTALLATION</summary>

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

</details>

<details><summary><b>IN-CLUSTER PROVIDER CONFIGURATION</b></summary>

```bash
# DEPLOY HELM RELEASES ON THE SAME CLUSTER CROSSPLANE IS RUNNING ON
SA=$(kubectl -n crossplane-system get sa -o name | grep provider-helm | sed -e 's|serviceaccount\/|crossplane-system:|g')
kubectl create clusterrolebinding provider-helm-admin-binding --clusterrole cluster-admin --serviceaccount="${SA}"

kubectl apply -f - <<EOF
apiVersion: helm.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: helm-provider-incluster
spec:
  credentials:
    source: InjectedIdentity
EOF
```

</details>

<details><summary><b>EXTERNAL CLUSTER PROVIDER CONFIGURATION</b></summary>

```bash
apiVersion: v1
kind: Secret
metadata:
  name: kubeconfig-cicd
  namespace: crossplane-system
data:
  sthings-cicd: <KUBECONFIG-BASE64>
type: Opaque
```

```bash
kubectl apply -f - <<EOF
apiVersion: helm.crossplane.io/v1beta1
kind: ProviderConfig
metadata:
  name: cicd
spec:
  credentials:
    source: Secret
    secretRef:
      name: kubeconfig-cicd
      namespace: crossplane-system
      key: sthings-cicd
EOF
```

</details>

<details><summary><b>DEPLOY HELM RELEASE FROM HELM REPO</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: helm.crossplane.io/v1beta1
kind: Release
metadata:
  name: goldilocks-example
spec:
  forProvider:
    chart:
      name: goldilocks
      repository: https://charts.fairwinds.com/stable
      version: 8.0.0
    namespace: goldilocks
    insecureSkipTLSVerify: true
    skipCreateNamespace: false
    wait: true
    skipCRDs: true
    values:
      service:
        type: ClusterIP
  providerConfigRef:
    name: helm-provider-incluster
EOF
```

</details>

<details><summary><b>CREATE OCI REGISTRY SECRET</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: ghcr
  namespace: crossplane-system
type: Opaque
stringData:
  username: <USERNAME>
  password: <PASSWORD>
EOF
```

</details>

<details><summary><b>DEPLOY OCI HELM RELEASE W/ REGISTRY SECRET</b></summary>

```bash
kubectl apply -f - <<EOF
---
apiVersion: helm.crossplane.io/v1beta1
kind: Release
metadata:
  name: ghr-deploy-configure-rke-cicd
  namespace: crossplane-system
spec:
  forProvider:
    chart:
      name: gha-runner-scale-set
      repository: oci://ghcr.io/actions/actions-runner-controller-charts
      version: 0.8.0
      pullSecretRef:
        name: ghcr
        namespace: crossplane-system
    namespace: arc-systems
    insecureSkipTLSVerify: false
    skipCreateNamespace: false
    wait: true
    skipCRDs: true
    set:
      - name: githubConfigSecret.github_token
        valueFrom:
          secretKeyRef:
            key: GITHUB_TOKEN
            name: github-flux-secrets
            namespace: flux-system
    values:
      githubConfigUrl: https://github.com/stuttgart-things/deploy-configure-rke
      containerMode:
        type: kubernetes
        kubernetesModeWorkVolumeClaim:
          accessModes: ["ReadWriteOnce"]
          storageClassName: openebs-hostpath
          resources:
            requests:
              storage: 50Mi
      template:
        spec:
          containers:
          - name: runner
            image: ghcr.io/actions/actions-runner:2.314.1
            command: ["/home/runner/run.sh"]
            env:
              - name: ACTIONS_RUNNER_REQUIRE_JOB_CONTAINER
                value: "false"
              - name: ACTIONS_RUNNER_POD_NAME
                valueFrom:
                  fieldRef:
                    fieldPath: metadata.name
          initContainers:
            - name: kube-init
              image: ghcr.io/actions/actions-runner:2.314.1
              command: ["/bin/sh", "-c"]
              args:
                - |
                  whoami
              volumeMounts:
                - name: work
                  mountPath: /home/runner/_work
  providerConfigRef:
    name: cicd
EOF
```

</details>

<details><summary><b>VERIFY RELEASE</b></summary>

```bash
kubectl get Release
```

</details>

## TERRAFORM PROVIDER

<details><summary><b>PROVIDER DEPLOYMENT</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: pkg.crossplane.io/v1
kind: Provider
metadata:
  name: provider-terraform
spec:
  package: xpkg.upbound.io/upbound/provider-terraform:v0.13.0
EOF
```

</details>

<details><summary><b>PROVIDER CONFIG (K8S STATE)</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: tf.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: default
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
```

</details>

<details><summary><b>PROVIDER CONFIG (S3 MINIO STATE)</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: s3
  namespace: crossplane-system
type: Opaque
stringData:
  AWS_ACCESS_KEY_ID: <ACCESS-KEY>
  AWS_SECRET_ACCESS_KEY: <SECRET-ACCESS-KEY>
EOF
```

```bash
kubectl apply -f - <<EOF
apiVersion: tf.upbound.io/v1beta1
kind: ProviderConfig
metadata:
  name: artifacts-labul-vsphere
  namespace: default
spec:
  configuration: |
    terraform {
      backend "s3" {
        endpoint = "https://artifacts.automation.sthings-vsphere.labul.sva.de"
        key = "terraform2.tfstate"
        region = "main"
        bucket = "terraform"
        skip_credentials_validation = true
        skip_metadata_api_check = true
        skip_region_validation = true
        force_path_style = true
      }
    }
EOF
```

</details>

<details><summary><b>INLINE WORKSPACE EXAMPLE</b></summary>

```bash
kubectl apply -f - <<EOF
apiVersion: tf.upbound.io/v1beta1
kind: Workspace
metadata:
  name: example-inline
  annotations:
    crossplane.io/external-name: hello
spec:
  forProvider:
    source: Inline
    module: |
      output "hello_world" {
        value = "Hello, World!"
      }
  writeConnectionSecretToRef:
    namespace: default
    name: terraform-workspace-example-inline
EOF
```

</details>

<details><summary><b>CREATE TFVARS AS SECRET</b></summary>

```bash
# CREATE terraform.tfvars
cat <<EOF > terraform.tfvars
vsphere_user = "<USER>"
vsphere_password = "<PASSWORD>"
vm_ssh_user = "<SSH_USER>"
vm_ssh_password = "<SSH_PASSWORD>"
EOF
```

```bash
# CREATE SECRET
kubectl create secret generic vsphere-tfvars --from-file=terraform.tfvars
```

</details>

<details><summary><b>MODULE WORKSPACE EXAMPLE</b></summary>

```yaml
---
apiVersion: tf.upbound.io/v1beta1
kind: Workspace
metadata:
  name: appserver
  annotations:
    crossplane.io/external-name: pve-vm
spec:
  providerConfigRef:
    name: terraform-default
  forProvider:
    source: Remote
    module: git::https://github.com/stuttgart-things/proxmox-vm.git?ref=v2.9.14-1.5.5
    vars:
      - key: vm_count
        value: "1"
      - key: vm_num_cpus
        value: "4"
      - key: vm_memory
        value: "4096"
      - key: vm_name
        value: appserver
      - key: vm_template
        value: ubuntu22
      - key: pve_network
        value: vmbr103
      - key: pve_datastore
        value: v3700
      - key: vm_disk_size
        value: 128G
      - key: pve_folder_path
        value: stuttgart-things
      - key: pve_cluster_node
        value: sthings-pve1
    varFiles:
      - source: SecretKey
        secretKeyRef:
          namespace: default
          name: pve-tfvars
          key: terraform.tfvars
  writeConnectionSecretToRef:
    namespace: default
    name: terraform-workspace-appserver
```

```hcl
# tfvars
pve_api_url="<API-URL>"
pve_api_user="<API-USER>"
pve_api_password="<API-PASSWORD>"
vm_ssh_user="<SSH-USER>"
vm_ssh_password="<SSH-PASSWORD>"
```

</details>

### EXAMPLE1: VSPHERE-VM

<details><summary><b>DEFINE INLINE WORKSPACE W/ MODULE CALL</b></summary>

```yaml
apiVersion: tf.upbound.io/v1beta1
kind: Workspace
metadata:
  name: vsphere-vm-labda-1
  annotations:
    crossplane.io/external-name: vsphere-vm-labda-1
spec:
  forProvider:
    source: Inline
    module: |
      module "labda-vm" {
        source = "github.com/stuttgart-things/vsphere-vm"
        vm_count               = 1
        vsphere_vm_name        = "michigan3"
        vm_memory              = 6144
        vm_disk_size           = "64"
        vm_num_cpus            = 6
        firmware               = "bios"
        vsphere_vm_folder_path = "stuttgart-things/testing"
        vsphere_datacenter     = "/NetApp-HCI-Datacenter"
        vsphere_datastore      = "/NetApp-HCI-Datacenter/datastore/DatastoreCluster/NetApp-HCI-Datastore-02"
        vsphere_resource_pool  = "Resources"
        vsphere_network        = "/NetApp-HCI-Datacenter/network/tiab-prod"
        vsphere_vm_template    = "/NetApp-HCI-Datacenter/vm/stuttgart-things/vm-templates/ubuntu23"
        vm_ssh_user            = var.vm_ssh_user
        vm_ssh_password        = var.vm_ssh_password
        bootstrap              = ["echo STUTTGART-THINGS"]
        annotation             = "VSPHERE-VM BUILD w/ TERRAFORM CROSSPLANE PROVIDER FOR STUTTGART-THINGS"
      }

      provider "vsphere" {
        user                 = var.vsphere_user
        password             = var.vsphere_password
        vsphere_server       = var.vsphere_server
        allow_unverified_ssl = true
      }

      variable "vsphere_server" {
        type        = string
        default     = false
        description = "vsphere server"
      }

      variable "vsphere_user" {
        type        = string
        default     = false
        description = "password of vsphere user"
      }

      variable "vsphere_password" {
        type        = string
        default     = false
        description = "password of vsphere user"
      }

      variable "vm_ssh_user" {
        type        = string
        default     = false
        description = "username of ssh user for vm"
      }

      variable "vm_ssh_password" {
        type        = string
        default     = false
        description = "password of ssh user for vm"
      }

    varFiles:
      - source: SecretKey
        secretKeyRef:
          namespace: default
          name: vsphere-tfvars
          key: terraform.tfvars
  writeConnectionSecretToRef:
    namespace: default
    name: terraform-workspace-vsphere-vm-labda-1
```

</details>

<details><summary><b>BETTER AS INLINE: DEFINE WORKSPACE W/ MODULE CALL</b></summary>

```yaml
---
apiVersion: tf.upbound.io/v1beta1
kind: Workspace
metadata:
  name: dallas52
  annotations:
    crossplane.io/external-name: vsphere-vm
spec:
  providerConfigRef:
    name: terraform-default
  forProvider:
    source: Remote
    module: git::https://github.com/stuttgart-things/vsphere-vm.git?ref=v1.6.6-2.6.1
    vars:
      - key: vm_count
        value: "1"
      - key: vsphere_vm_name
        value: dallas52
      - key: vm_memory
        value: "6144"
      - key: vm_disk_size
        value: "64"
      - key: vm_num_cpus
        value: "6"
      - key: firmware
        value: bios
      - key: vsphere_vm_folder_path
        value: phermann/testing
      - key: vsphere_datacenter
        value: /LabUL
      - key: vsphere_datastore
        value: /LabUL/datastore/UL-ESX-SAS-02
      - key: vsphere_resource_pool
        value: /LabUL/host/Cluster01/Resources
      - key: vsphere_network
        value: /LabUL/network/LAB-10.31.103
      - key: vsphere_vm_template
        value: /LabUL/vm/phermann/vm-templates/ubuntu22
      - key: bootstrap
        value: '["echo STUTTGART-THINGS"]'
      - key: annotation
        value: VSPHERE-VM BUILD w/ CROSSPLANE FOR STUTTGART-THINGS
      - key: unverified_ssl
        value: "true"
    varFiles:
      - source: SecretKey
        secretKeyRef:
          namespace: default
          name: vsphere-labul-tfvars
          key: vsphere-labul.tfvars
  writeConnectionSecretToRef:
    namespace: default
    name: terraform-workspace-dallas52
```

</details>

<details><summary><b>APPLY/STATUS/DESTORY</b></summary>

```bash
kubectl apply -f <WORKSPACE-DEFINITION>.yaml
kubectl describe workspace <WORKSPACE_NAME> | grep Status -A10
kubectl delete workspace <WORKSPACE_NAME>
```

</details>

<details><summary><b>COMPOSITE-RESOURCE-DEFINITION</b></summary>

```yaml
---
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xvspherevms.resources.stuttgart-things.com
spec:
  group: resources.stuttgart-things.com
  names:
    kind: XVsphereVM
    plural: xvspherevms
  claimNames:
    kind: VsphereVM
    plural: vspherevms
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
                vm:
                  type: object
                  properties:
                    count:
                      type: string
                      default: "1"
                    name:
                      type: string
                    ram:
                      type: string
                      default: "4096"
                    disk:
                      type: string
                      default: "64"
                    cpu:
                      type: string
                      default: "4"
                    firmware:
                      type: string
                      default: "bios"
                    folderPath:
                      type: string
                    datacenter:
                      type: string
                    datastore:
                      type: string
                    resourcePool:
                      type: string
                    network:
                      type: string
                    template:
                      type: string
                    bootstrap:
                      type: string
                      default: '["echo STUTTGART-THINGS"]'
                    annotation:
                      type: string
                      default: VSPHERE-VM BUILD w/ CROSSPLANE FOR STUTTGART-THINGS
                    unverifiedSsl:
                      type: string
                      default: "true"
                  required:
                    - name
                    - ram
                    - disk
                    - cpu
                    - folderPath
                    - datacenter
                    - datastore
                    - resourcePool
                    - network
                    - template
                tfvars:
                  type: object
                  properties:
                    secretName:
                      type: string
                    secretNamespace:
                      type: string
                      default: default
                    secretKey:
                      type: string
                      default: terraform.tfvars
                  required:
                    - secretName
                connectionSecret:
                  type: object
                  properties:
                    name:
                      type: string
                    namespace:
                      type: string
                      default: default
                  required:
                    - name
                providerRef:
                  type: object
                  properties:
                    name:
                      type: string
                  required:
                    - name
              required:
                - vm
                - tfvars
                - connectionSecret
                - providerRef
```

</details>

<details><summary><b>COMPOSITION</b></summary>

```yaml
---
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: vsphere-vm
  labels:
    crossplane.io/xrd: xvspherevms.resources.stuttgart-things.com
spec:
  compositeTypeRef:
    apiVersion: resources.stuttgart-things.com/v1alpha1
    kind: XVsphereVM
  resources:
    - name: vsphere-vm
      base:
        kind: Workspace
        apiVersion: tf.upbound.io/v1beta1
        metadata:
          annotations:
            crossplane.io/external-name: vsphere-vm
        spec:
          providerConfigRef:
            name: terraform-default
          writeConnectionSecretToRef:
            name: vsphere-vm-test
            namespace: crossplane-system
          forProvider:
            source: Remote
            module: git::https://github.com/stuttgart-things/vsphere-vm.git?ref=v1.6.6-2.6.1
            vars:
              - key: vm_count
                type: integer
                value: "1"
              - key: vsphere_vm_name
                type: string
              - key: vm_memory
                type: integer
                value: "4096"
              - key: vm_disk_size
                type: integer
                value: "64"
              - key: vm_num_cpus
                type: integer
                value: "4"
              - key: firmware
                type: string
                value: bios
              - key: vsphere_vm_folder_path
                type: string
              - key: vsphere_datacenter
                type: string
              - key: vsphere_datastore
                type: string
              - key: vsphere_resource_pool
                type: string
              - key: vsphere_network
                type: string
              - key: vsphere_vm_template
                type: string
              - key: bootstrap
                type: string
                value: '["echo STUTTGART-THINGS"]'
              - key: annotation
                type: string
                value: VSPHERE-VM BUILD w/ CROSSPLANE FOR STUTTGART-THINGS
              - key: unverified_ssl
                type: string
                value: "true"
            varFiles:
              - source: SecretKey
                secretKeyRef:
                  namespace: default
                  name: vsphere-tfvars
                  key: terraform.tfvars
      patches:
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.count
          toFieldPath: spec.forProvider.vars[0].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.name
          toFieldPath: spec.forProvider.vars[1].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.ram
          toFieldPath: spec.forProvider.vars[2].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.disk
          toFieldPath: spec.forProvider.vars[3].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.cpu
          toFieldPath: spec.forProvider.vars[4].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.firmware
          toFieldPath: spec.forProvider.vars[5].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.folderPath
          toFieldPath: spec.forProvider.vars[6].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.datacenter
          toFieldPath: spec.forProvider.vars[7].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.datastore
          toFieldPath: spec.forProvider.vars[8].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.resourcePool
          toFieldPath: spec.forProvider.vars[9].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.network
          toFieldPath: spec.forProvider.vars[10].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.template
          toFieldPath: spec.forProvider.vars[11].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.bootstrap
          toFieldPath: spec.forProvider.vars[12].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.annotation
          toFieldPath: spec.forProvider.vars[13].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.vm.unverifiedSsl
          toFieldPath: spec.forProvider.vars[14].value
        - type: FromCompositeFieldPath
          fromFieldPath: spec.tfvars.secretName
          toFieldPath: spec.forProvider.varFiles[0].secretKeyRef.name
        - type: FromCompositeFieldPath
          fromFieldPath: spec.tfvars.secretNamespace
          toFieldPath: spec.forProvider.varFiles[0].secretKeyRef.namespace
        - type: FromCompositeFieldPath
          fromFieldPath: spec.tfvars.secretKey
          toFieldPath: spec.forProvider.varFiles[0].secretKeyRef.key
        - type: FromCompositeFieldPath
          fromFieldPath: spec.connectionSecret.name
          toFieldPath: spec.writeConnectionSecretToRef.name
        - type: FromCompositeFieldPath
          fromFieldPath: spec.connectionSecret.namespace
          toFieldPath: spec.writeConnectionSecretToRef.namespace
        - type: FromCompositeFieldPath
          fromFieldPath: spec.providerRef.name
          toFieldPath: spec.providerConfigRef.name
```

</details>

<details><summary><b>CLAIM</b></summary>

```yaml
---
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: VsphereVM
metadata:
  name: torronto
  namespace: default
spec:
  providerRef:
    name: terraform-default
  vm:
    count: "1"
    name: torronto
    ram: "4096"
    disk: "32"
    cpu: "8"
    firmware: bios
    folderPath: phermann/testing
    datacenter: /LabUL
    datastore: /LabUL/datastore/UL-ESX-SAS-02
    resourcePool: /LabUL/host/Cluster01/Resources
    network: /LabUL/network/LAB-10.31.103
    template: /LabUL/vm/phermann/vm-templates/ubuntu22
    bootstrap: '["echo STUTTGART-THINGS"]'
    annotation: VSPHERE-VM BUILD w/ CROSSPLANE FOR STUTTGART-THINGS
    unverifiedSsl: "true"
  tfvars:
    secretName: vsphere-labul-tfvars
    secretNamespace: default
    secretKey: vsphere-labul.tfvars
  connectionSecret:
    name: torronto
    namespace: default
  compositionRef:
    name: vsphere-vm
```

</details>

<details><summary><b>VERIFY CLAIM/COMPOSITE/WORKSPACE</b></summary>

```bash
kubectl get crossplane # get all crossplane resources
kubectl get claim # get claims
kubectl get composite # get composite
kubectl get workspace # get workspace
kubectl describe workspace # describe workspace <WORKSPACE-NAME>
```

</details>

### EXAMPLE2: K8S-RESOURCE

<details><summary><b>CREATE CLUSTER ROLE FOR TERRAFORM SERVICE ACCOUNT</b></summary>

```bash
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

</details>

<details><summary><b>CREATE COMPOSITE-RESOURCE-DEFINITION</b></summary>

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

</details>

<details><summary><b>CREATE SAMPLE COMPOSITION</b></summary>

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

</details>

<details><summary><b>CREATE SAMPLE CLAIM</b></summary>

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

</details>

<details><summary><b>VERIFY CLAIM</b></summary>

```bash
kubectl get NginxApp
```

</details>
