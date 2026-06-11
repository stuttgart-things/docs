---
layout: default
class: 'is-appendix'
num: 'P · Appendix'
meta: 'Crossplane · nested Configuration package'
---

<div class="page-label">P · nested Configuration package</div>

# <span class="accent">Nested</span> Configuration package<span class="dot">.</span>

<div class="nest">
  <div class="topbox">
    <div class="tb-h"><img :src="'/logos/kcl.svg'" alt="KCL" style="height: 34px; width: auto;" />virtual-machine</div>
    <div class="tb-s">XVirtualMachine · t-shirt API · function-kcl Composition</div>
  </div>
  <div class="nestarrow">dependsOn&nbsp;&nbsp;▼</div>
  <div class="deps">
    <div class="depbox">
      <div class="dep-k">Functions</div>
      <div class="pills"><span class="pill">function-kcl</span><span class="pill">function-environment-configs</span><span class="pill">function-auto-ready</span></div>
    </div>
    <div class="depbox cfg">
      <div class="dep-k">vm-provision <span>Configuration</span></div>
      <div class="pills"><span class="pill">vsphere-vm</span><span class="pill">proxmox-vm</span><span class="pill">ansible-run</span></div>
    </div>
    <div class="depbox cfg">
      <div class="dep-k">harvester-vm <span>Configuration</span></div>
      <div class="pills"><span class="pill">volume-claim</span><span class="pill">cloud-config</span><span class="pill">ansible-run</span><span class="pill">provider-kubernetes</span></div>
    </div>
  </div>
  <div class="nestnote">installing <code>virtual-machine</code> pulls every nested package transitively — one install, the whole stack</div>
</div>

<style scoped>
.nest { margin-top: 32px; }
.topbox { border: 2px solid var(--accent); border-radius: 14px; background: var(--surface-accent); padding: 18px 24px; text-align: center; }
.tb-h { font-size: 24px; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 12px; }
.tb-s { font-family: var(--font-mono); font-size: 14px; color: var(--fg-muted); margin-top: 6px; }
.nestarrow { text-align: center; font-family: var(--font-mono); font-size: 14px; color: var(--accent); margin: 14px 0; letter-spacing: 0.06em; }
.deps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; align-items: start; }
.depbox { border: 1px solid var(--rule); border-radius: 12px; background: var(--surface); padding: 18px; }
.depbox.cfg { border-left: 4px solid var(--accent); }
.dep-k { font-size: 19px; font-weight: 600; }
.dep-k span { font-family: var(--font-mono); font-size: 12px; color: var(--accent); margin-left: 6px; font-weight: 500; }
.depbox .pills { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.pill { font-family: var(--font-mono); font-size: 14px; padding: 4px 11px; border-radius: 999px; background: color-mix(in srgb, var(--accent) 12%, transparent); color: var(--accent); }
.nestnote { font-family: var(--font-mono); font-size: 13px; color: var(--fg-faint); margin-top: 24px; text-align: center; }
</style>
