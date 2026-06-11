---
layout: default
num: '02 · KCL profiles as self-service claims'
meta: 'KCL · claim-machinery-api · claims CLI · Backstage plugin'
---

<div class="page-label">02 · KCL profiles, served as self-service claims</div>

# One KCL profile, two <span class="accent">front doors</span><span class="dot">.</span>

<p class="lede" style="margin-top: 12px; max-width: 94ch;">
The same <code>XVirtualMachine</code> KCL module is served by <strong>claim-machinery-api</strong> and consumed two ways — the <code>claims</code> CLI or the Backstage plugin — both rendering one claim into a Git PR. Then it's the <a class="card-link" href="/6">VM flow from before</a>.
</p>

<div class="cm">
<div class="cmflow">
<div class="stage" style="--c:#2563eb"><div class="lh"><img :src="'/logos/kcl.svg'" alt="KCL" />KCL profile<span>xr-virtualmachine</span></div><div class="ls"><code>XVirtualMachine</code> XR · templates <code>minimal</code> / <code>detailed</code> · params size · provider · environment — published to OCI (<code>ghcr.io</code>)</div></div>
<div class="ar2">→</div>
<div class="stage" style="--c:#0d9488"><div class="lh">claim-machinery-api<span>serve · render</span></div><div class="ls">discovers + renders the KCL templates · exposes the <strong>parameter schema</strong> (types, enums, defaults) · <code>profiles/</code> map environment → placement</div></div>
<div class="ar2">→</div>
<div class="consume"><div class="mini" style="--c:#64748b"><div class="lh">claims · CLI<span>terminal</span></div><div class="ls">interactive render → Git PR</div></div><div class="mini" style="--c:#8b5cf6"><div class="lh"><img :src="'/logos/backstage.svg'" alt="Backstage" />Backstage plugin<span>scaffolder</span></div><div class="ls">template picker + dynamic param form → <code>claim-machinery:render</code> → MR</div></div></div>
</div>
<div class="cmbanner"><span class="cmb-dot"></span>Both render the <strong>same claim</strong> → Git PR/MR → GitOps → Crossplane → the running Harvester VM</div>
<div class="deepdive">
<span class="dd-label">Source</span>
<a class="card-link" href="https://github.com/stuttgart-things/kcl/tree/main/crossplane/xr-virtualmachine" target="_blank">kcl · xr-virtualmachine</a>
<a class="card-link" href="https://github.com/stuttgart-things/claim-machinery-api" target="_blank">claim-machinery-api</a>
<a class="card-link" href="https://github.com/stuttgart-things/claims" target="_blank">claims · CLI</a>
<a class="card-link" href="https://github.com/stuttgart-things/backstage-claim-machinery-plugin" target="_blank">backstage-claim-machinery-plugin</a>
</div>
</div>

```yaml
# one KCL profile, served by claim-machinery-api, rendered on demand
kcl run oci://ghcr.io/stuttgart-things/xr-virtualmachine \
  -D templateName=detailed -D provider=harvester \
  -D size=medium -D environment=labul
---
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: XVirtualMachine        # size · provider · environment → a HarvesterVM
metadata: { name: vm-harv }
```

<style scoped>
.cm { margin-top: 32px; }
.cmflow { display: grid; grid-template-columns: 1fr auto 1fr auto 1.12fr; align-items: stretch; gap: 12px; }
.stage { border: 1px solid var(--rule); border-top: 4px solid var(--c); border-radius: 14px; background: var(--surface); padding: 22px 20px; display: flex; flex-direction: column; }
.lh { font-size: 21px; font-weight: 600; color: var(--c); display: flex; align-items: center; gap: 10px; line-height: 1.15; }
.lh img { height: 24px; width: auto; }
.lh span { font-family: var(--font-mono); font-size: 12.5px; color: var(--fg-faint); font-weight: 400; margin-left: auto; }
.ls { font-size: 15px; color: var(--fg-muted); line-height: 1.5; margin-top: 12px; }
.ls code { font-family: var(--font-mono); font-size: 13.5px; color: var(--c); }
.ar2 { align-self: center; font-size: 32px; color: var(--accent); }
.consume { display: flex; flex-direction: column; gap: 12px; }
.mini { border: 1px solid var(--rule); border-left: 4px solid var(--c); border-radius: 12px; background: color-mix(in srgb, var(--c) 6%, var(--surface)); padding: 14px 16px; flex: 1; }
.mini .lh { font-size: 18px; }
.mini .lh img { height: 20px; }
.mini .ls { margin-top: 7px; font-size: 14px; }
.cmbanner { margin-top: 22px; border: 1px solid var(--rule); border-left: 4px solid var(--accent); border-radius: 12px; background: color-mix(in srgb, var(--accent) 7%, transparent); padding: 15px 22px; font-size: 17px; font-weight: 600; display: flex; align-items: center; gap: 11px; }
.cmb-dot { width: 11px; height: 11px; border-radius: 50%; background: var(--accent); display: inline-block; flex: none; }
.deepdive { margin-top: 20px; display: flex; flex-wrap: wrap; align-items: baseline; gap: 16px; }
.dd-label { font-family: var(--font-mono); font-size: 12px; color: var(--fg-faint); letter-spacing: 0.1em; text-transform: uppercase; }
.cm + :deep(.slidev-code) { font-size: 13px !important; line-height: 1.45 !important; padding: 16px !important; margin-top: 22px; }
</style>
