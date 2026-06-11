---
layout: default
num: '04 · ClusterbookCluster · config'
meta: 'ClusterbookCluster · labels → AppSets · annotations → config'
---

<div class="page-label">04 · The cluster config</div>

# A cluster, as <span class="accent">YAML</span><span class="dot">.</span>

<p class="lede" style="margin-top: 10px; max-width: 92ch;">
<strong>Labels pick the platforms, annotations carry their config.</strong> The operator copies both onto the ArgoCD cluster <code>Secret</code> — and stamps the reserved IP/DNS as <code>[auto]</code> annotations.
</p>

<div class="cfg">
  <div class="cfg-code">

```yaml
apiVersion: clusterbook.stuttgart-things.com/v1alpha1
kind: ClusterbookCluster
metadata:
  name: crossplane-dev1
spec:
  clusterName: crossplane-dev1
  clusterType: default          # vSphere RKE2 (or "kind")
  networkKey: '10.31.103'       # pool the IP is reserved from
  createDNS: true               # reserve a wildcard DNS record
  providerConfigRef: { name: default }
  kubeconfigSecretRef:
    name: crossplane-dev1
    namespace: argocd
    key: kubeconfig

  labels:                       # → which platforms (AppSets match here)
    cicd-platform: 'true'              # umbrella switch
    cicd-platform/crossplane: 'true'   # one component
    cicd-platform/tekton: 'true'
    network-platform: 'true'
    network-platform/cilium-lb: 'true'
    storage-platform/openebs: 'true'
    security-platform/kyverno: 'true'

  annotations:                  # → the components' config
    clusterbook.stuttgart-things.com/vault-server: https://vault…
    clusterbook.stuttgart-things.com/vault-pki-path: pki/sign/sthings
```

  </div>
  <div class="cfg-side">
    <div class="note" style="--c:#8b5cf6">
      <div class="note-h">labels = which platforms</div>
      <div class="note-d">Each <code>&lt;profile&gt;: 'true'</code> is the umbrella switch; <code>&lt;profile&gt;/&lt;component&gt;</code> flips one component. Platform ApplicationSets <code>matchLabels</code> on them — see <a class="card-link" href="/8">the fan-out</a>.</div>
    </div>
    <div class="note" style="--c:#3b82f6">
      <div class="note-h">annotations = the config</div>
      <div class="note-d">Each component reads its parameters from annotations. <code>[user]</code> ones you set (Vault, NFS…); <code>[auto]</code> ones — <code>ip</code>, <code>fqdn</code> — the operator stamps from the reservation.</div>
    </div>
    <div class="note" style="--c:#0d9488">
      <div class="note-h">one Secret out</div>
      <div class="note-d">The operator reserves IP&nbsp;+&nbsp;DNS from clusterbook, then writes <strong>one</strong> ArgoCD cluster <code>Secret</code> carrying every label and annotation.</div>
    </div>
    <a class="card-link" href="https://github.com/stuttgart-things/argocd/blob/main/platforms/cluster.reference.yaml" target="_blank">Full reference · cluster.reference.yaml →</a>
  </div>
</div>

<style scoped>
.cfg { display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 28px; margin-top: 24px; align-items: start; }
.cfg-code :deep(.slidev-code) { font-size: 13px !important; line-height: 1.42 !important; padding: 16px !important; }
.cfg-side { display: flex; flex-direction: column; gap: 14px; }
.note { border-left: 4px solid var(--c); border-radius: 10px; padding: 12px 16px; background: color-mix(in srgb, var(--c) 7%, transparent); }
.note-h { font-size: 17px; font-weight: 600; color: var(--c); }
.note-d { font-size: 14.5px; line-height: 1.5; color: var(--fg-muted); margin-top: 5px; }
.note-d code { font-family: var(--font-mono); font-size: 12.5px; color: var(--fg); }
.note-d .card-link { font-size: 14.5px; }
</style>
