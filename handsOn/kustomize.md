# KUSTOMIZE EXERCISES

## CHEETSHEET

```bash
# To view Resources found in a directory containing a kustomization file, run the following command:
kubectl kustomize <kustomization_directory>
# To apply those Resources, run kubectl apply with --kustomize or -k flag:
kubectl apply -k <kustomization_directory>
kubectl apply -k <kustomization_directory> -n <NAMESPACE>
```

## configMapGenerator

TASKS:

* CREATE THE FOLLOWING FILES

    ```bash
    mkdir -p ./cm
    cat <<EOF >./cm/application.properties
    CITY=OBERKOCHEN
    EOF
    ```

    ```bash
    cat <<EOF >./cm/kustomization.yaml
    configMapGenerator:
    - name: example-configmap-1
      files:
        - application.properties
    EOF
    ```

* CHECK CREATED FILES
* VIEW RESOURCES
* APPLY (INTO YOUR NAMESPACE)
* CHANGE application.properties
* RENDER RESOURCES TO FILE
* CHECK (CHANGES) ON FILESYSTEM
* CHECK (CHANGES) ON CLUSTER

## change image names and tags

TASKS:

* CREATE THE FOLLOWING FILES

    ```bash
    mkdir -p ./pod
    cat <<EOF >./pod/kustomization.yaml
    resources:
    - pod.yaml
    EOF
    ```

    ```bash
    cat <<EOF >./pod/pod.yaml
    apiVersion: v1
    kind: Pod
    metadata:
    name: myapp-pod
    labels:
        app: myapp
    spec:
    containers:
    - name: myapp-container
        image: busybox:1.29.0
        command: ['sh', '-c', 'echo The app is running! && sleep 3600']
    EOF
    ```

* Fix the syntax errors in the pod manifest
* kustomize edit set image busybox=alpine:3.6
* build and or apply

## work w/ environments

TASKS:
* CREATE THE FOLLOWING FILES

    ```bash
    mkdir -p ./kustomize/base
    mkdir -p ./kustomize/overlays/dev
    cat <<EOF >./kustomize/base/kustomization.yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization

    resources:
    - deployment.yaml

    images:
    - name: nginx
    newTag: 1.8.0
    EOF
    ```

    ```bash
    cat <<EOF >./kustomize/base/deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: the-deployment
    annotations:
        app: nginx
    spec:
    template:
        spec:
        containers:
        - name: nginxapp
            image: nginx:1.7.9
    EOF
    ```

    ```bash
    mkdir -p ./kustomize/base
    mkdir -p ./kustomize/overlays/dev
    cat <<EOF >./kustomize/dev/kustomization.yaml
    apiVersion: kustomize.config.k8s.io/v1beta1
    kind: Kustomization

    resources:
    - ../../base

    patches:
    - path: deploy-patch.yaml
    EOF
    ```

    ```bash
    cat <<EOF >./kustomize/dev/deploy-patch.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: the-deployment
    spec:
    template:
        spec:
        containers:
            - name: istio-proxy
            image: docker.io/istio/proxyv2
            args:
            - proxy
            - sidecar
    EOF
    ```

* build base
* apply base
* build dev
* apply dev
* create prod env
