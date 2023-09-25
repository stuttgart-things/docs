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
    cat <<EOF >$DEMO_HOME/pod.yaml
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

* kustomize edit set image busybox=alpine:3.6
