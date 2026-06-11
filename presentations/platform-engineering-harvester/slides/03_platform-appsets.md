---
layout: default
num: '03 · Platform ApplicationSets'
meta: 'ArgoCD · AppSets · label-driven fan-out'
---

<div class="page-label">03 · Platform fan-out with ArgoCD</div>

# One ArgoCD, many <span class="accent">platforms</span><span class="dot">.</span>

<p class="lede" style="margin-top: 12px; max-width: 84ch;">
Each platform is an ApplicationSet in the management cluster. Its <strong>cluster selector</strong> matches a <strong>label</strong> — so every downstream cluster gets exactly the platforms it opted into.
</p>

<div class="board">
  <div class="mgmt">
    <div class="mgmt-h"><span class="mgmt-t"><img :src="'/logos/argo.svg'" alt="Argo CD" style="height: 28px; width: auto; vertical-align: -5px; margin-right: 8px;" />ArgoCD · management cluster</span><span class="mgmt-sub">platforms/ ApplicationSets</span></div>
    <div class="plat" style="--c: #8b5cf6">
      <div class="plat-top"><span class="dot2"></span>cicd-platform</div>
      <div class="sel">cluster selector · <code>matchLabels: cicd-platform=true</code></div>
      <div class="pills"><span class="pill">crossplane</span><span class="pill">tekton</span><span class="pill">kro</span><span class="pill">dapr</span><span class="pill">kargo</span></div>
    </div>
    <div class="plat" style="--c: #3b82f6">
      <div class="plat-top"><span class="dot2"></span>network-platform</div>
      <div class="sel">cluster selector · <code>matchLabels: network-platform=true</code></div>
      <div class="pills"><span class="pill">cilium</span><span class="pill">cert-manager</span><span class="pill">trust-manager</span></div>
    </div>
    <div class="plat" style="--c: #B5832A">
      <div class="plat-top"><span class="dot2"></span>storage-platform</div>
      <div class="sel">cluster selector · <code>matchLabels: storage-platform=true</code></div>
      <div class="pills"><span class="pill">openebs</span><span class="pill">longhorn</span><span class="pill">nfs-csi</span></div>
    </div>
    <div class="plat" style="--c: #3F7B59">
      <div class="plat-top"><span class="dot2"></span>security-platform</div>
      <div class="sel">cluster selector · <code>matchLabels: security-platform=true</code></div>
      <div class="pills"><span class="pill">external-secrets</span><span class="pill">kyverno</span></div>
    </div>
    <div class="plat" style="--c: #64748b">
      <div class="plat-top"><span class="dot2"></span>kind-platform</div>
      <div class="sel">cluster selector · <code>clusterType: kind</code></div>
      <div class="pills"><span class="pill">cilium</span><span class="pill">cert-manager</span></div>
    </div>
  </div>
  <div class="arrowcol">
    <div class="arrowbig">⇒</div>
    <div class="arrowlbl">generator<br/>selects by<br/>label</div>
  </div>
  <div class="downstream">
    <div class="surface ds">
      <div class="ds-name">crossplane-dev1 <span>cicd-vsphere</span></div>
      <div class="dslabels"><span class="lab" style="--c:#8b5cf6">cicd-platform</span><span class="lab" style="--c:#3b82f6">network-platform</span><span class="lab" style="--c:#B5832A">storage-platform</span><span class="lab" style="--c:#3F7B59">security-platform</span></div>
    </div>
    <div class="surface ds">
      <div class="ds-name">homerun2-dev <span>network-only</span></div>
      <div class="dslabels"><span class="lab" style="--c:#3b82f6">network-platform</span><span class="lab" style="--c:#3F7B59">security-platform</span></div>
    </div>
    <div class="surface ds">
      <div class="ds-name">cd-mgmt-1-kind-dev1 <span>kind-dev</span></div>
      <div class="dslabels"><span class="lab" style="--c:#64748b">kind-platform</span></div>
    </div>
    <div class="ds-note">labels carried on the ArgoCD cluster <code>Secret</code> · stamped from <code>ClusterbookCluster</code></div>
  </div>
</div>

<style scoped>
.board { display: grid; grid-template-columns: 1.25fr auto 0.92fr; gap: 22px; align-items: start; margin-top: 34px; }
.mgmt { border: 2px solid var(--rule-strong); border-radius: 16px; padding: 22px; background: var(--surface); }
.mgmt-h { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 16px; font-family: var(--font-mono); }
.mgmt-t { font-size: 17px; font-weight: 700; letter-spacing: 0.04em; }
.mgmt-sub { font-size: 13px; color: var(--fg-muted); }
.plat { border-left: 5px solid var(--c); border-radius: 10px; padding: 14px 18px; margin-bottom: 13px; background: color-mix(in srgb, var(--c) 7%, transparent); }
.plat:last-child { margin-bottom: 0; }
.plat-top { font-size: 20px; font-weight: 600; display: flex; align-items: center; gap: 9px; line-height: 1.1; }
.dot2 { width: 11px; height: 11px; border-radius: 50%; background: var(--c); display: inline-block; }
.sel { font-family: var(--font-mono); font-size: 13px; color: var(--fg-muted); margin-top: 5px; }
.sel code { color: var(--c); }
.plat .pills { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 10px; }
.pill { font-family: var(--font-mono); font-size: 13.5px; padding: 4px 11px; border-radius: 999px; background: color-mix(in srgb, var(--c) 14%, transparent); color: var(--c); }
.arrowcol { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; padding-top: 70px; }
.arrowbig { font-size: 44px; color: var(--accent); line-height: 1; }
.arrowlbl { font-family: var(--font-mono); font-size: 13px; color: var(--fg-muted); text-align: center; line-height: 1.35; }
.downstream { display: flex; flex-direction: column; gap: 16px; }
.ds { padding: 20px 22px; }
.ds-name { font-size: 20px; font-weight: 600; display: flex; justify-content: space-between; align-items: baseline; gap: 8px; }
.ds-name span { font-family: var(--font-mono); font-size: 13px; color: var(--accent); }
.dslabels { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 14px; }
.lab { font-family: var(--font-mono); font-size: 13.5px; padding: 4px 11px; border-radius: 7px; border: 1px solid var(--c); color: var(--c); background: color-mix(in srgb, var(--c) 8%, transparent); }
.ds-note { font-family: var(--font-mono); font-size: 12.5px; color: var(--fg-faint); line-height: 1.4; margin-top: 6px; }
</style>
