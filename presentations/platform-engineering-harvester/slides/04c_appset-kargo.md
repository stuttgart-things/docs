---
layout: default
num: '04 · ApplicationSet · labels & annotations'
meta: 'ApplicationSet · cluster selector · annotation templating'
---

<div class="page-label">04 · How an AppSet reads the cluster</div>

# Labels select, annotations <span class="accent">configure</span><span class="dot">.</span>

<p class="lede" style="margin-top: 10px; max-width: 94ch;">
The same two fields, now from the platform side — <code>appset-kargo.yaml</code>. The <strong>generator</strong> picks clusters by label; the <strong>template</strong> reads config from their annotations.
</p>

<div class="cfg">
  <div class="cfg-code">

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata: { name: kargo-cicd }
spec:
  goTemplate: true
  generators:
    - clusters:                        # iterate ArgoCD cluster Secrets
        selector:
          matchLabels:
            cicd-platform: "true"      # umbrella must be on
          matchExpressions:
            - key: cicd-platform/kargo # opt-out gate
              operator: NotIn
              values: ["false"]
  template:
    spec:
      source:
        repoURL: https://github.com/stuttgart-things/argocd.git
        path: cicd/kargo/install
        helm:
          valuesObject:
            # derive the host from the cluster's clusterbook
            # FQDN annotation; fall back if it's absent
            api:
              host: 'kargo.{{ index .metadata.annotations
                "clusterbook.stuttgart-things.com/fqdn"
                | trimPrefix "*." | default "example.com" }}'
```

  </div>
  <div class="cfg-side">
    <div class="note" style="--c:#8b5cf6">
      <div class="note-h">the generator → label gate</div>
      <div class="note-d"><code>clusters:</code> walks every ArgoCD cluster <code>Secret</code>. <code>matchLabels</code> needs the umbrella <code>cicd-platform=true</code>; the <code>NotIn ["false"]</code> rule makes Kargo <strong>opt-out</strong> — you get it unless you set the toggle to <code>false</code>.</div>
    </div>
    <div class="note" style="--c:#3b82f6">
      <div class="note-h">the template → annotation</div>
      <div class="note-d"><code>index .metadata.annotations "…/fqdn"</code> pulls the wildcard FQDN the operator stamped, strips the <code>*.</code> and builds <code>kargo.&lt;cluster&gt;.&lt;zone&gt;</code> — matching the HTTPRoute host + cert SAN.</div>
    </div>
    <div class="note" style="--c:#0d9488">
      <div class="note-h">safe by default</div>
      <div class="note-d">No FQDN annotation? It falls back to <code>kargo.example.com</code> — so the AppSet is safe to apply across every cluster it selects.</div>
    </div>
    <a class="card-link" href="https://github.com/stuttgart-things/argocd/blob/main/platforms/cicd/appset-kargo.yaml" target="_blank">Full AppSet · appset-kargo.yaml →</a>
    <a class="card-link" href="/9">Platform fan-out →</a>
  </div>
</div>

<style scoped>
.cfg { display: grid; grid-template-columns: 1.18fr 0.82fr; gap: 28px; margin-top: 24px; align-items: start; }
.cfg-code :deep(.slidev-code) { font-size: 12.5px !important; line-height: 1.42 !important; padding: 16px !important; }
.cfg-side { display: flex; flex-direction: column; gap: 14px; }
.note { border-left: 4px solid var(--c); border-radius: 10px; padding: 12px 16px; background: color-mix(in srgb, var(--c) 7%, transparent); }
.note-h { font-size: 17px; font-weight: 600; color: var(--c); }
.note-d { font-size: 14.5px; line-height: 1.5; color: var(--fg-muted); margin-top: 5px; }
.note-d code { font-family: var(--font-mono); font-size: 12.5px; color: var(--fg); }
.cfg-side .card-link { font-size: 14.5px; }
</style>
