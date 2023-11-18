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
%%{init:{'theme':'base'}}%%
%%{init:{'themeCSS':'.messageLine0:nth-of-type(2) { stroke: red; };.messageText:nth-of-type(1) { fill: green; font-size: 30px !important;}; g:nth-of-type(3) rect.actor { stroke:blue;fill: pink; }; g:nth-of-type(5) .note { stroke:blue;fill: crimson; };#arrowhead path {stroke: blue; fill:red;};'}}%%
{{< /mermaid >}}

## another diagram

%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'primaryColor': '#BB2528',
      'primaryTextColor': '#fff',
      'primaryBorderColor': '#7C0000',
      'lineColor': '#F8B229',
      'secondaryColor': '#006100',
      'tertiaryColor': '#fff'
    }
  }
}%%
        graph TD
          A[Christmas] -->|Get money| B(Go shopping)
          B --> C{Let me think}
          B --> G[/Another/]
          C ==>|One| D[Laptop]
          C -->|Two| E[iPhone]
          C -->|Three| F[fa:fa-car Car]
          subgraph section
            C
            D
            E
            F
            G
          end
