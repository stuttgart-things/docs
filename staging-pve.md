# stuttgart-things/docs/staging-pve

## BOOTSRAP CLUSTER

{{< mermaid >}}
stateDiagram-v2
    Bootstrap: BOOTSTRAP
    note left of Bootstrap
        CREATES ALL VMS (MSO)
        PROVISIONS ALL VMS (TEKTON)
        BOOSTRAPS FLUX (TEKTON) 
        CREATES PACKER BUILDS (TEKTON)
    end note
    Bootstrap --> Vault
    Flux --> Bootstrap
    note left of Vault : Runs outside the cluster
{{< /mermaid >}}
