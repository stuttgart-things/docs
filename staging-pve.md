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

## Just another example to test some things

{{< mermaid >}}
pie title What Voldemort doesn't have?
         "FRIENDS" : 2
         "FAMILY" : 3
         "NOSE" : 45
%%{init:{'theme':'dark'}}%%
{{< /mermaid >}}

{{< mermaid >}}
sequenceDiagram
Fred->>Jill:Hello my Snookums
note over Fred:True Love
Jill->>Fred:Oh my Darling!
note over Jill:True Love Returned
%%{init:{'theme':'dark'}}%%
{{< /mermaid >}}

