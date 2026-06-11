---
layout: default
num: '04 · Clusterbook · cluster config → platforms'
meta: 'Clusterbook · ClusterbookCluster · ArgoCD platforms'
---

<div class="page-label">04 · From cluster config to platforms</div>

# One config object, a whole <span class="accent">platform</span><span class="dot">.</span>

<p class="lede" style="margin-top: 12px; max-width: 92ch;">
A <code>ClusterbookCluster</code> declares what a cluster <em>is</em>. The <strong>clusterbook-operator</strong> reserves its IP&nbsp;&amp;&nbsp;DNS and renders an ArgoCD cluster <code>Secret</code> — labels and annotations included. The platform <strong>ApplicationSets</strong> take it from there.
</p>

<div class="cb">
  <div class="cbflow">
    <div class="stage" style="--c:#8b5cf6">
      <div class="sn">1 · declare</div>
      <div class="st">ClusterbookCluster</div>
      <div class="sd">a CR in Git — <code>clusterName</code>, <code>networkKey</code>, <code>labels</code>, <code>annotations</code></div>
    </div>
    <div class="ar2">→</div>
    <div class="stage" style="--c:#0d9488">
      <div class="sn">2 · reconcile</div>
      <div class="st">clusterbook-operator</div>
      <div class="sd">reserves IP&nbsp;+&nbsp;DNS, then renders the ArgoCD cluster <code>Secret</code></div>
    </div>
    <div class="ar2">→</div>
    <div class="stage" style="--c:#3b82f6">
      <div class="sn">3 · register</div>
      <div class="st">ArgoCD cluster Secret</div>
      <div class="sd"><code>labels</code> ← spec.labels · <code>annotations</code> ← spec.annotations</div>
    </div>
    <div class="ar2">→</div>
    <div class="stage" style="--c:#3F7B59">
      <div class="sn">4 · fan-out</div>
      <div class="st">Platform ApplicationSets</div>
      <div class="sd">select by label · read config from annotations</div>
    </div>
  </div>

  <div class="cbservice">
    <div class="cbs-h"><span class="cbs-dot"></span>clusterbook · IPAM backend</div>
    <div class="cbs-d">CIDR network pools · IP&nbsp;+&nbsp;wildcard-DNS reservation · gRPC&nbsp;/&nbsp;REST&nbsp;/&nbsp;CR — the operator calls this in step&nbsp;2</div>
  </div>

  <div class="deepdive">
    <span class="dd-label">Instances</span>
    <a class="card-link" href="https://clusterbook.infra.sthings-vsphere.labul.sva.de/" target="_blank">clusterbook · Lab</a>
    <a class="card-link" href="https://clusterbook.infra.sthings.lab/" target="_blank">clusterbook · Edge</a>
    <a class="card-link" href="https://argocd.platform.sthings-vsphere.labul.sva.de/" target="_blank">ArgoCD · Lab</a>
    <a class="card-link" href="https://argocd.platform.sthings.lab/" target="_blank">ArgoCD · Edge</a>
    <span class="dd-label" style="margin-left: 8px;">Source</span>
    <a class="card-link" href="https://github.com/stuttgart-things/clusterbook" target="_blank">stuttgart-things/clusterbook</a>
    <a class="card-link" href="https://github.com/stuttgart-things/argocd/tree/main/platforms" target="_blank">argocd/platforms</a>
    <a class="card-link" href="/10">Config example →</a>
    <a class="card-link" href="/8">Platform fan-out →</a>
  </div>
</div>

<style scoped>
.cb { margin-top: 40px; }
.cbflow { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr; align-items: stretch; gap: 12px; }
.stage { border: 1px solid var(--rule); border-top: 5px solid var(--c); border-radius: 14px; background: var(--surface); padding: 28px 24px; min-height: 188px; display: flex; flex-direction: column; }
.sn { font-family: var(--font-mono); font-size: 14px; color: var(--c); letter-spacing: 0.06em; }
.st { font-size: 26px; font-weight: 600; line-height: 1.15; margin-top: 10px; }
.sd { font-size: 17px; color: var(--fg-muted); line-height: 1.5; margin-top: 14px; }
.sd code { font-family: var(--font-mono); font-size: 15px; color: var(--c); }
.ar2 { align-self: center; font-size: 34px; color: var(--accent); }
.cbservice { margin-top: 22px; border: 1px solid var(--rule); border-left: 4px solid #B5832A; border-radius: 12px; background: color-mix(in srgb, #B5832A 7%, transparent); padding: 16px 22px; display: flex; align-items: center; justify-content: space-between; gap: 24px; }
.cbs-h { font-size: 20px; font-weight: 600; display: flex; align-items: center; gap: 10px; white-space: nowrap; }
.cbs-dot { width: 11px; height: 11px; border-radius: 50%; background: #B5832A; display: inline-block; }
.cbs-d { font-size: 16px; color: var(--fg-muted); line-height: 1.4; }
.deepdive { margin-top: 24px; display: flex; flex-wrap: wrap; align-items: baseline; gap: 16px; }
.dd-label { font-family: var(--font-mono); font-size: 12px; color: var(--fg-faint); letter-spacing: 0.1em; text-transform: uppercase; }
</style>
