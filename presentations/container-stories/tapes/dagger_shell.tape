#!/usr/bin/env dagger

container |
    from cgr.dev/chainguard/wolfi-base |
    with-exec apk add curl git bash wget kubectl helm k9s cilium terraform |
    with-exec -- wget https://github.com/helmfile/helmfile/releases/download/v1.1.7/helmfile_1.1.7_linux_amd64.tar.gz |
    with-exec -- tar xvfz helmfile_1.1.7_linux_amd64.tar.gz |
    with-exec -- mv helmfile /usr/bin/ |
    with-directory /showcase https://github.com/stuttgart-things/platform-engineering-showcase.git#main |
    with-mounted-file /root/.kube/config ../../../.kube/keycloak-cluster |
    with-env-variable KUBECONFIG /root/.kube/config |
    with-mounted-file apply-helm.sh apply-helm.sh |
    with-mounted-file provisioning.yaml provisioning.yaml |
    with-mounted-file crds.yaml crds.yaml |
    terminal

    #with-secret-variable VCENTER_FQDN env://VCENTER_FQDN |
    #with-secret-variable BLA vault://eva.kubeconfig |

    #--token=vault://secret/data/github?field=token
    # MOUNT CURRENT DIR
    #with-mounted-directory /workspace . |

    # MOUNT CACHE
    #with-mounted-cache /data my-workspace |
    #terminal|
    #with-exec -- mkdir /output |
    #with-exec -- cp -r /data/ /output/data/ |
    #directory /output |
    #export ./output-dir