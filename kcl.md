# KCL

KCL is an open-source, constraint-based record and functional programming language. It leverages mature programming language technology and practices to facilitate the writing of many complex configurations.

## SNIPPETS

<details><summary><b>IMPORT PACKAGE</b></summary>

```hcl
# main.k
import tekton_pipelines.v1 as tekton
import .vars
import datetime
import crypto

_timestamp = str(datetime.now())
_suffix = crypto.md5(_timestamp)[:8]

tekton.PipelineRun {
    metadata = {
        name = "${vars.pipeline_name_prefix}-${_suffix}"
        }
    spec = {
        pipelineRef = {
            resolver = "git"
            params = [
                {name = k, value = v} for k, v in vars.git_config
            ]
        }
        params = [
            {name = k, value = v} for k, v in vars.pipeline_params
        ]
    }
}
```

```hcl
# defaults.k
# Default pipeline parameters
default_params = {
    ansibleWorkingImage = "ghcr.io/stuttgart-things/sthings-ansible:11.0.0"
    createInventory = "false"
    ansibleTargetHost = "all"
    gitWorkspaceSubdirectory = "/ansible/workdir/"
    vaultSecretName = "vault"
    installExtraRoles = "true"
}
```

```hcl
# values.k
# Environment-specific overrides
override_params = {
    ansibleWorkingImage = "ghcr.io/stuttgart-things/sthings-ansible:12.0.0"
    gitRepoUrl = "https://github.com/stuttgart-things/stage-time.git"
    gitRevision = "main"
    inventory = "MTAuMzEuMTAzLjI3Cg=="
    ansibleExtraRoles = [
        "https://github.com/stuttgart-things/install-requirements.git,2024.05.11"
        "https://github.com/stuttgart-things/manage-filesystem.git,2024.06.07"
        "https://github.com/stuttgart-things/install-configure-vault.git"
        "https://github.com/stuttgart-things/create-send-webhook.git,2024-06-06"
    ]
}
```

```hcl
# vars.k
import .defaults
import .values

# Merge defaults with overrides (overrides take precedence)
pipeline_params = defaults.default_params | values.override_params

# Pipeline reference config
git_config = {
    url = "https://github.com/stuttgart-things/stage-time.git"
    revision = "main"
    pathInRepo = "pipelines/execute-ansible-playbooks.yaml"
}

pipeline_name_prefix = "pr-ansible"
```

```bash
kcl mod init
mod add tekton-pipelines
kcl run main.k
```

</details>


<details><summary><b>CROSSPLANE OCI-KCL COMPOSITIONS</b></summary>

```python
# Get the XR spec fields
id = option("params")?.oxr?.spec.id or ""
name = option("params")?.oxr?.spec.name or ""

# Labels for network identification
network_id_labels = {"networks.meta.fn.crossplane.io/network-id" = id} if id != "" else {}

# ConfigMap with public network configuration
config = {
    apiVersion = "v1"
    kind = "ConfigMap"
    metadata = {
        name = name
        labels = network_id_labels
    }
    data = {
        region = "eu-west-1"
        cidrBlock = "192.168.0.0/16"
        enableDnsSupport = "true"
        enableDnsHostnames = "true"
    }
}
```

```bash
kcl mod init
kcl run -D params='{"oxr": {"spec": {"id": "whateveaa", "name": "network-whateveaa"}}}'
kcl mod push oci://ghcr.io/stuttgart-things/kcl-test1
```

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xexamples.example.com
spec:
  group: example.com
  names:
    kind: XExample
    plural: xexamples
  claimNames:
    kind: ExampleClaim
    plural: exampleclaims
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
              id:
                type: string
              parameters:
                type: object
---
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-kcl
spec:
  package: xpkg.upbound.io/crossplane-contrib/function-kcl:v0.11.5
---
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xplane-tinkerbell-oci
spec:
  compositeTypeRef:
    apiVersion: example.com/v1alpha1
    kind: XExample  # This should match your XRD
  mode: Pipeline
  pipeline:
    - functionRef:
        name: function-kcl
      input:
        apiVersion: krm.kcl.dev/v1alpha1
        kind: KCLInput
        metadata:
          name: basic
        spec:
          params:
            oxr:
              spec:
                id: whateveaa
          source: oci://ghcr.io/stuttgart-things/kcl-test1
      step: render-workflow
---
apiVersion: example.com/v1alpha1
kind: XExample
metadata:
  name: test-xr
spec:
  id: test-566
  name: blink-182
  parameters:
    bla: blupp
    # Add any required parameters here
```

```bash
crossplane render claim.yaml composition.yaml function.yaml
```

</details>

<details><summary><b>CROSSPLANE INLINE KCL COMPOSITIONS</b></summary>

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: xplane-tinkerbell
spec:
  compositeTypeRef:
    apiVersion: tinkerbell.sthings.cloud/v1alpha1
    kind: WorkflowClaim
  mode: Pipeline
  pipeline:
  - functionRef:
      name: function-kcl
    input:
      apiVersion: krm.kcl.dev/v1alpha1
      kind: KCLRun
      metadata:
        name: render-workflow
      spec:
        target: Resources
        params:
          oxr: {}
        source: |
          # Get the XR spec fields from the observed composite resource
          oxr = option("params")?.oxr
          workflowName = oxr?.spec?.workflowName or ""
          workflowNamespace = oxr?.spec?.workflowNamespace or "default"
          templateRef = oxr?.spec?.templateRef or ""
          hardwareRef = oxr?.spec?.hardwareRef or ""
          hardwareMap = oxr?.spec?.hardwareMap or {}
          createWorkflow = oxr?.spec?.createWorkflow or True
          workflowProviderConfigRef = oxr?.spec?.workflowProviderConfigRef or "in-cluster"

          # ConfigMap specific fields
          configMapName = oxr?.spec?.configMapName or "tinkerbell-config"
          configMapData = oxr?.spec?.configMapData or {}
          createConfigMap = oxr?.spec?.createConfigMap or False
          configMapProviderConfigRef = oxr?.spec?.configMapProviderConfigRef or "in-cluster"

          # Create the Kubernetes Object for Tinkerbell Workflow
          workflow = {
              apiVersion = "kubernetes.crossplane.io/v1alpha2"
              kind = "Object"
              metadata = {
                  name = workflowName
                  annotations = {
                      "crossplane.io/external-name" = workflowName
                  }
              }
              spec = {
                  forProvider = {
                      manifest = {
                          apiVersion = "tinkerbell.org/v1alpha1"
                          kind = "Workflow"
                          metadata = {
                              name = workflowName
                              namespace = workflowNamespace
                          }
                          spec = {
                              templateRef = templateRef
                              hardwareRef = hardwareRef
                              hardwareMap = hardwareMap
                          }
                      }
                  }
                  deletionPolicy = "Delete"
                  managementPolicies = ["*"]
                  providerConfigRef = {
                      name = workflowProviderConfigRef
                  }
              }
          }

          # Create the Kubernetes Object for ConfigMap
          config_map = {
              apiVersion = "kubernetes.crossplane.io/v1alpha2"
              kind = "Object"
              metadata = {
                  name = configMapName
                  annotations = {
                      "crossplane.io/external-name" = configMapName
                  }
              }
              spec = {
                  forProvider = {
                      manifest = {
                          apiVersion = "v1"
                          kind = "ConfigMap"
                          metadata = {
                              name = configMapName
                              namespace = workflowNamespace
                          }
                          data = configMapData
                      }
                  }
                  deletionPolicy = "Delete"
                  managementPolicies = ["*"]
                  providerConfigRef = {
                      name = configMapProviderConfigRef
                  }
              }
          }

          # Return the resources to create
          workflow_list = [workflow] if createWorkflow else []
          config_map_list = [config_map] if createConfigMap else []
          items = workflow_list + config_map_list
    step: render-workflow
---
apiVersion: pkg.crossplane.io/v1beta1
kind: Function
metadata:
  name: function-kcl
spec:
  package: xpkg.upbound.io/crossplane-contrib/function-kcl:v0.11.5
---
apiVersion: apiextensions.crossplane.io/v1
kind: CompositeResourceDefinition
metadata:
  name: xworkflows.tinkerbell.sthings.cloud
spec:
  group: tinkerbell.sthings.cloud
  names:
    kind: XWorkflow
    plural: xworkflows
  claimNames:
    kind: WorkflowClaim
    plural: workflowclaims
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
              # Workflow specific fields
              workflowName:
                type: string
                description: "Name of the Tinkerbell workflow"
              workflowNamespace:
                type: string
                description: "Namespace where the workflow will be created"
                default: "default"
              templateRef:
                type: string
                description: "Reference to the Tinkerbell template"
              hardwareRef:
                type: string
                description: "Reference to the Tinkerbell hardware"
              hardwareMap:
                type: object
                description: "Map of device identifiers to MAC addresses"
                additionalProperties:
                  type: string
              createWorkflow:
                type: boolean
                description: "Whether to create the workflow"
                default: true
              workflowProviderConfigRef:
                type: string
                description: "Reference to the Crossplane ProviderConfig for the workflow"
                default: "in-cluster"

              # ConfigMap specific fields
              configMapName:
                type: string
                description: "Name of the ConfigMap"
                default: "tinkerbell-config"
              configMapData:
                type: object
                description: "Data content for the ConfigMap"
                additionalProperties:
                  type: string
              createConfigMap:
                type: boolean
                description: "Whether to create the ConfigMap"
                default: false
              configMapProviderConfigRef:
                type: string
                description: "Reference to the Crossplane ProviderConfig for the ConfigMap"
                default: "in-cluster"
            required:
            - workflowName
            - templateRef
            - hardwareRef
            - hardwareMap
          status:
            type: object
            properties:
              workflowStatus:
                type: string
                description: "Status of the Tinkerbell workflow"
              configMapStatus:
                type: string
                description: "Status of the ConfigMap"
              conditions:
                type: array
                items:
                  type: object
                  properties:
                    type:
                      type: string
                    status:
                      type: string
                    lastTransitionTime:
                      type: string
                      format: date-time
                    reason:
                      type: string
                    message:
                      type: string
---
apiVersion: tinkerbell.sthings.cloud/v1alpha1
kind: WorkflowClaim
metadata:
  name: u22-machine1
  namespace: default
spec:
  # Required fields for workflow
  workflowName: u22-machine1-workflow
  templateRef: ubuntu24
  hardwareRef: machine1
  workflowProviderConfigRef: in-cluster
  hardwareMap:
    device_1: "00:0c:29:aa:bb:cc"

  # Optional ConfigMap configuration
  createConfigMap: true
  configMapName: u22-machine1-config
  configMapProviderConfigRef: demo-infra
  configMapData:
    os_version: "ubuntu-22.04"
    boot_mode: "uefi"
    disk_layout: "/dev/sda"
    user_data: |
      #cloud-config
      package_update: true
      packages:
        - curl
        - wget
```

</details>




<details><summary><b>INIT (KONFIG) KPM MODULE</b></summary>

### INIT ENVIRONMENT (DEV)

```bash
kpm init dev && cd dev
kcl mod add konfig:0.5.0
kcl mod add k8s:1.30
kpm pull k8s:1.30
kpm pull konfig:0.5.0

cat <<EOF > main.k
import konfig.models.kube.frontend
import konfig.models.kube.templates.resource as res_tpl

# The application configuration in stack will overwrite
# the configuration with the same attribute in base.
appConfiguration: frontend.Server {
    schedulingStrategy.resource = res_tpl.tiny
}
EOF

echo '[profile]
entries = ["../base/base.k", "main.k", "${konfig:KCL_MOD}/models/kube/render/render.k"]' >> kcl.mod
```

### CREATE BASE MODULE

```bash
mkdir ../base && cd ../base
cat <<EOF > base.k
import konfig.models.kube.frontend
import konfig.models.kube.frontend.service
import konfig.models.kube.frontend.container

# Application Configuration
appConfiguration: frontend.Server {
    # Main Container Configuration
    mainContainer = container.Main {
        ports = [
            {containerPort = 80}
        ]
        env.MY_ENV: {
            value = "MY_VALUE"
        }
    }
    image = "nginx:1.7.8"
    services = [
        service.Service {
            name = "nginx"
            type = "NodePort"
            ports = [
                {
                    nodePort = 30201
                    port = 80
                    targetPort = 80
                }
            ]
        }
    ]
}
EOF
```

### RENDER ENVIRONMENT

```bash
kpm run dev # folder
```

</details>

<details><summary><b>KUBERNETES MANIFEST w/ VARIABLES</b></summary>

```bash
cat <<EOF > deployment.k
_project="opsat-gitlab-receiver"
_registry = "scr.cd43.sthings-pve.labul.sva.de"
_repository = "opsat"
_image = "opsat-gitlab-receiver-08556b153acb3834815dbeff6e71babf"
_tag = "5539da4ccba34231bd8518776b177985d1cb37508b0c56257f0d97fe31bc7a1e"
_label = "opsat"

apiVersion = "apps/v1"
kind = "Deployment"
metadata = {
    name = "${_project}"
    labels.app = "${_label}"
}
spec = {
    replicas = 1
    selector.matchLabels = metadata.labels
    template.metadata.labels = metadata.labels
    template.spec.containers = [
        {
            name = metadata.name
            image = "${_registry}/${_repository}/${_image}:${_tag}"
            ports = [{ containerPort = 80 }]
        }
    ]
}
EOF
```

</details>

<details><summary><b>CONVERT KCL</b></summary>

```bash
kcl deployment.k # JUST RENDER
kcl deployment.k -o deployment.yaml # OUTPUT TO FILE
kcl deployment.k | kubectl apply -f - # APPLY TO CLUSTER
```

</details>
