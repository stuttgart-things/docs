# stuttgart-things/docs/staging-pve

## BOOSTRAP CLUSTER

{{< mermaid >}}
stateDiagram-v2
    Bootstrap: BOOTSTRAP
    note right of Bootstrap
        CREATES ALL VMS (MSO)
        PROVISIONS ALL VMS (TEKTON)
        BOOSTRAPS FLUX (TEKTON)
        CREATES PACKER BUILDS (TEKTON)
    end note
    Bootstrap --> Vault
    note left of Vault : Runs outside the cluster
{{< /mermaid >}}
