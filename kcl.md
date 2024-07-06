# KCL

KCL is an open-source, constraint-based record and functional programming language. It leverages mature programming language technology and practices to facilitate the writing of many complex configurations.

# https://blog.devops.dev/kcl-and-kpm-the-art-of-managing-kubernetes-configurations-5a0f5b6d4198

## SNIPPETS

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
