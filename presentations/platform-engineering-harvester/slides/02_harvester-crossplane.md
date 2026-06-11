---
layout: default
num: '02 · Create Harvester VM with Crossplane'
meta: 'Backstage · Git · GitOps · Crossplane · Harvester · Tekton'
---

<div class="page-label">02 · Create Harvester VM with Crossplane</div>

# From a Backstage form to a <span class="accent">running VM</span><span class="dot">.</span>

<p class="lede" style="margin-top: 14px; max-width: 88ch;">
Git-reviewed, GitOps-delivered, Crossplane-reconciled — then Tekton runs Ansible to configure the guest.
</p>

<div class="proc">
  <div class="flow2">
    <div class="stage" style="--c:#8b5cf6"><img :src="'/logos/backstage.svg'" class="slogo" alt="Backstage" /><div class="sn">1 · self-service</div><div class="st">Backstage</div><div class="sd">form renders a HarvesterVM claim</div></div>
    <div class="ar2">→</div>
    <div class="stage" style="--c:#64748b"><img :src="'/logos/git.svg'" class="slogo" alt="Git" /><div class="sn">2 · review</div><div class="st">Git</div><div class="sd">pull request + validation checks</div></div>
    <div class="ar2">→</div>
    <div class="stage" style="--c:#3b82f6"><img :src="'/logos/argo.svg'" class="slogo" alt="Argo CD" /><div class="sn">3 · delivery</div><div class="st">Argo CD · GitOps</div><div class="sd">sync &amp; apply to the cluster</div></div>
    <div class="ar2">→</div>
    <div class="stage" style="--c:#0d9488"><img :src="'/logos/crossplane.svg'" class="slogo" alt="Crossplane" /><div class="sn">4 · reconcile</div><div class="st">Crossplane</div><div class="sd">composition renders the resources</div></div>
    <div class="ar2">→</div>
    <div class="stage" style="--c:#3F7B59"><img :src="'/logos/harvester.svg'" class="slogo" alt="Harvester" style="height:22px;" /><div class="sn">5 · provision</div><div class="st">Harvester</div><div class="sd">KubeVirt VM is created</div></div>
  </div>
  <div class="downflow">▼&nbsp;&nbsp;once the VM is up</div>
  <div class="tekbanner">
    <div class="tk-h"><img :src="'/logos/tekton.svg'" class="banner-logo" alt="Tekton" />Tekton pipeline · runs <strong>Ansible</strong></div>
    <div class="tk-d"><img :src="'/logos/ansible.svg'" class="inline-logo" alt="Ansible" />post-provisioning configuration of the new Harvester VM — packages, users, app setup</div>
  </div>
  <div class="deepdive">
    <span class="dd-label">Appendix · deep dive</span>
    <a class="card-link" href="/10">Ansible-run · Crossplane</a>
    <a class="card-link" href="/12">Namespace example</a>
    <a class="card-link" href="/15">XRD</a>
    <a class="card-link" href="/16">Composition</a>
    <a class="card-link" href="/18">Functions</a>
    <a class="card-link" href="/19">XR / claim</a>
    <a class="card-link" href="/20">Configuration</a>
    <a class="card-link" href="/21">EnvironmentConfig</a>
    <a class="card-link" href="/25">KCL · t-shirt API</a>
    <a class="card-link" href="/26">KCL · function-kcl</a>
    <a class="card-link" href="/27">Nested package</a>
  </div>
</div>

<style scoped>
.proc { margin-top: 40px; }
.flow2 { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr auto 1fr; align-items: stretch; gap: 10px; }
.stage { border: 1px solid var(--rule); border-top: 4px solid var(--c); border-radius: 12px; background: var(--surface); padding: 18px 16px; display: flex; flex-direction: column; }
.sn { font-family: var(--font-mono); font-size: 12px; color: var(--c); letter-spacing: 0.06em; }
.st { font-size: 21px; font-weight: 600; line-height: 1.15; margin-top: 8px; }
.sd { font-size: 14.5px; color: var(--fg-muted); line-height: 1.4; margin-top: 8px; }
.ar2 { align-self: center; font-size: 26px; color: var(--accent); }
.slogo { height: 30px; width: auto; display: block; margin-bottom: 10px; }
.banner-logo { height: 34px; width: auto; }
.inline-logo { height: 22px; width: auto; vertical-align: -2px; margin-right: 8px; }
.downflow { text-align: center; font-family: var(--font-mono); font-size: 13px; color: var(--accent); margin: 16px 0; letter-spacing: 0.03em; }
.tekbanner { border: 1px solid var(--rule); border-left: 4px solid #B5832A; border-radius: 12px; background: color-mix(in srgb, #B5832A 7%, transparent); padding: 16px 22px; display: flex; justify-content: space-between; align-items: center; gap: 24px; }
.tk-h { font-size: 20px; font-weight: 600; display: flex; align-items: center; gap: 10px; white-space: nowrap; }
.tk-dot { width: 10px; height: 10px; border-radius: 50%; background: #B5832A; display: inline-block; }
.tk-d { font-size: 16px; color: var(--fg-muted); line-height: 1.4; }
.deepdive { margin-top: 24px; display: flex; flex-wrap: wrap; align-items: baseline; gap: 16px; }
.dd-label { font-family: var(--font-mono); font-size: 12px; color: var(--fg-faint); letter-spacing: 0.1em; text-transform: uppercase; }
</style>
