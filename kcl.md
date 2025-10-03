# KCL

KCL is an open-source, constraint-based record and functional programming language. It leverages mature programming language technology and practices to facilitate the writing of many complex configurations.

# https://blog.devops.dev/kcl-and-kpm-the-art-of-managing-kubernetes-configurations-5a0f5b6d4198

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
