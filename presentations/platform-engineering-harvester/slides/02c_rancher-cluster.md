---
layout: default
num: '02c · Rancher cluster composition'
meta: 'Crossplane · EnvironmentConfig · go-templating · Rancher · Harvester · Argo CD'
---

<div class="page-label">02c · One claim → a whole Rancher cluster</div>

# What the <span class="accent">composition</span> does, step by step<span class="dot">.</span>

<p class="lede" style="margin-top: 12px; max-width: 96ch;">
The <code>RancherCluster</code> XR is intentionally thin — a <code>name</code>, an <code>environmentConfig</code> and a little sizing. The <strong>rancher-cluster</strong> Composition is a Crossplane <strong>Pipeline</strong>: it resolves per-environment defaults, then <code>function-go-templating</code> renders the resources in order — provision → wire → use → (optionally) register.
</p>

<div class="proc">
  <div class="flow2">
    <div class="stage" style="--c:#64748b"><img :src="'/logos/crossplane.svg'" class="slogo" alt="Crossplane" /><div class="sn">0 · resolve</div><div class="st">EnvironmentConfig</div><div class="sd"><code>function-environment-configs</code> loads per-env defaults · precedence <strong>XR&nbsp;spec&nbsp;→&nbsp;env&nbsp;→&nbsp;default</strong></div></div>
    <div class="ar2">→</div>
    <div class="stage" style="--c:#3F7B59"><img :src="'/logos/harvester.svg'" class="slogo" alt="Harvester" style="height:22px;" /><div class="sn">1 · provision</div><div class="st">cattle.io Cluster</div><div class="sd"><code>provisioning.cattle.io</code> Cluster on Rancher · Harvester: + <code>HarvesterConfig</code> VM template &amp; machine pool → Rancher boots the nodes</div></div>
    <div class="ar2">→</div>
    <div class="stage" style="--c:#0d9488"><img :src="'/logos/crossplane.svg'" class="slogo" alt="Crossplane" /><div class="sn">2 · wire</div><div class="st">ProviderConfig</div><div class="sd"><code>ClusterProviderConfig</code> → the downstream kubeconfig Secret <span class="muted">(split lab: bridge it to the control plane first)</span></div></div>
    <div class="ar2">→</div>
    <div class="stage" style="--c:#3b82f6"><img :src="'/logos/kubevirt.svg'" class="slogo" alt="Namespace" /><div class="sn">3 · use</div><div class="st">Bootstrap NS</div><div class="sd">create a <code>Namespace</code> on the new cluster through that CPC — the <strong>proof</strong> the extracted kubeconfig actually works</div></div>
    <div class="ar2">→</div>
    <div class="stage" style="--c:#8b5cf6"><img :src="'/logos/argo.svg'" class="slogo" alt="Argo CD" /><div class="sn">4 · register <span class="opt">opt</span></div><div class="st">Argo CD</div><div class="sd">SA + cluster-admin + non-expiring token → direct-endpoint kubeconfig → <code>ClusterbookCluster</code> → cluster in Argo CD</div></div>
  </div>
  <div class="cmbanner"><span class="cmb-dot"></span>The whole pipeline is bracketed by <code>function-auto-ready</code> — the XR flips <strong>Ready</strong> only once every rendered <code>Object</code> is.</div>
  <div class="deepdive">
    <span class="dd-label">Source</span>
    <a class="card-link" href="https://github.com/stuttgart-things/crossplane-configurations/tree/main/machinery/rancher-cluster" target="_blank">crossplane · rancher-cluster</a>
    <a class="card-link" href="https://github.com/stuttgart-things/kcl/tree/main/crossplane/xr-rancher-cluster" target="_blank">kcl · xr-rancher-cluster</a>
    <a class="card-link" href="/10">Clusterbook · deep dive</a>
  </div>
</div>

```yaml
# rancher-cluster Composition · mode: Pipeline
pipeline:
  - step: load-environment        # function-environment-configs → per-env defaults
  - step: render-rancher-cluster  # function-go-templating renders, in order:
      #  (1) provisioning.cattle.io/v1 Cluster   [+ HarvesterConfig & pool if harvester]
      #  (2) ClusterProviderConfig → <name>-kubeconfig   (3) bootstrap Namespace
      #  (4) argocd SA → token → kubeconfig → ClusterbookCluster   (register=true)
  - step: ready                   # function-auto-ready → XR Ready when all Objects are
```

<style scoped>
.proc { margin-top: 28px; }
.flow2 { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr auto 1fr; align-items: stretch; gap: 10px; }
.stage { border: 1px solid var(--rule); border-top: 4px solid var(--c); border-radius: 12px; background: var(--surface); padding: 16px 14px; display: flex; flex-direction: column; }
.sn { font-family: var(--font-mono); font-size: 12px; color: var(--c); letter-spacing: 0.06em; }
.st { font-size: 19px; font-weight: 600; line-height: 1.15; margin-top: 7px; }
.sd { font-size: 13.5px; color: var(--fg-muted); line-height: 1.42; margin-top: 8px; }
.sd code { font-family: var(--font-mono); font-size: 12px; color: var(--c); }
.sd .muted { color: var(--fg-faint); }
.opt { font-family: var(--font-mono); font-size: 10px; color: var(--fg-faint); border: 1px solid var(--rule); border-radius: 4px; padding: 0 4px; margin-left: 6px; vertical-align: 1px; }
.ar2 { align-self: center; font-size: 24px; color: var(--accent); }
.slogo { height: 28px; width: auto; display: block; margin-bottom: 9px; }
.cmbanner { margin-top: 22px; border: 1px solid var(--rule); border-left: 4px solid var(--accent); border-radius: 12px; background: color-mix(in srgb, var(--accent) 7%, transparent); padding: 14px 22px; font-size: 16px; font-weight: 500; display: flex; align-items: center; gap: 11px; }
.cmbanner code { font-family: var(--font-mono); font-size: 14px; font-weight: 600; }
.cmb-dot { width: 11px; height: 11px; border-radius: 50%; background: var(--accent); display: inline-block; flex: none; }
.deepdive { margin-top: 20px; display: flex; flex-wrap: wrap; align-items: baseline; gap: 16px; }
.dd-label { font-family: var(--font-mono); font-size: 12px; color: var(--fg-faint); letter-spacing: 0.1em; text-transform: uppercase; }
.proc + :deep(.slidev-code) { font-size: 12.5px !important; line-height: 1.5 !important; padding: 16px !important; margin-top: 22px; }
</style>
