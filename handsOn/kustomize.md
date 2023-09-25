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

## configMapGenerator
