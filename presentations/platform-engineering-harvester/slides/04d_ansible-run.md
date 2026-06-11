---
layout: default
num: '04 · Ansible · wrapped in Tekton · wrapped in Crossplane'
meta: 'AnsibleRun · Crossplane Configuration · Tekton PipelineRun'
---

<div class="page-label">04 · Ansible as a Crossplane API</div>

# Wrap Ansible in Tekton, in <span class="accent">Crossplane</span><span class="dot">.</span>

<p class="lede" style="margin-top: 10px; max-width: 94ch;">
One <code>AnsibleRun</code> object renders a Tekton <code>PipelineRun</code> that runs the playbook — and Crossplane tracks it all the way to <code>Ready</code>. The deep dive behind <a class="card-link" href="/4">"Tekton runs Ansible"</a>.
</p>

<div class="ar">
  <div class="ar-top">
    <div class="nest">
      <div class="layer xp">
        <div class="lh"><img :src="'/logos/crossplane.svg'" alt="Crossplane" />Crossplane · AnsibleRun<span>XR · namespaced v2</span></div>
        <div class="ls">Composition runs <code>function-kcl</code> (<code>kcl-tekton-pr</code>) → renders the PipelineRun, wrapped in a <code>provider-kubernetes</code> Object and applied to the target cluster</div>
        <div class="layer tk">
          <div class="lh"><img :src="'/logos/tekton.svg'" alt="Tekton" />Tekton · PipelineRun<span>execute-ansible-playbooks</span></div>
          <div class="ls"><code>git-clone</code> → <code>execute-ansible</code> on a workspace PVC</div>
          <div class="layer an">
            <div class="lh"><img :src="'/logos/ansible.svg'" alt="Ansible" />Ansible</div>
            <div class="ls"><code>sthings.baseos.setup</code> · vars + inventory → target host</div>
          </div>
        </div>
      </div>
    </div>
    <div class="ar-code">

```yaml
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: AnsibleRun                # a namespaced Crossplane v2 XR
metadata: { name: ansible-run-baseos }
spec:
  # what to run
  ansiblePlaybooks: [ sthings.baseos.setup ]
  ansibleVarsInventory: [ 'all+["10.31.102.107"]' ]
  # the Tekton pipeline that runs it
  gitRepoUrl: https://github.com/stuttgart-things/stage-time.git
  gitPath: pipelines/execute-ansible-playbooks.yaml
  # wrap the PipelineRun + apply it on the target cluster
  wrapInCrossplane: true
  crossplaneProviderConfig: in-cluster
```

</div>
</div>
<div class="ar-notes">
<div class="note" style="--c:#0d9488">
<div class="note-h">one object in</div>
<div class="note-d">Apply the <code>AnsibleRun</code>. The Composition renders the <code>PipelineRun</code> via KCL; <code>provider-kubernetes</code> applies it on <code>crossplaneProviderConfig</code>.</div>
</div>
<div class="note" style="--c:#B5832A">
<div class="note-h">status flows back</div>
<div class="note-d">A <code>derive-status</code> step mirrors the live PipelineRun onto the XR — <code>succeeded</code>, <code>reason</code>, child <code>taskRuns</code>.</div>
</div>
<div class="note" style="--c:#C2410C">
<div class="note-h">Ready = pipeline Succeeded</div>
<div class="note-d"><code>deriveReadiness: true</code> keeps the XR un-Ready until the playbook actually finished — GitOps can gate on it.</div>
</div>
</div>
<div class="deepdive">
<span class="dd-label">Source</span>
<a class="card-link" href="https://github.com/stuttgart-things/crossplane-configurations/tree/main/cicd/ansible-run" target="_blank">crossplane-configurations · ansible-run</a>
<a class="card-link" href="https://github.com/stuttgart-things/stage-time/blob/main/pipelines/execute-ansible-playbooks.yaml" target="_blank">stage-time · pipeline</a>
<a class="card-link" href="https://github.com/orgs/stuttgart-things/packages/container/package/kcl-tekton-pr" target="_blank">kcl-tekton-pr</a>
</div>
</div>

<style scoped>
.ar { margin-top: 20px; }
.ar-top { display: grid; grid-template-columns: 0.92fr 1.08fr; gap: 28px; align-items: start; }
.nest {}
.layer { border: 1.5px solid var(--c); border-radius: 14px; padding: 16px 18px; background: color-mix(in srgb, var(--c) 6%, var(--surface)); }
.layer.xp { --c:#0d9488; }
.layer.tk { --c:#B5832A; margin-top: 14px; }
.layer.an { --c:#C2410C; margin-top: 12px; }
.lh { font-size: 19px; font-weight: 600; color: var(--c); display: flex; align-items: center; gap: 10px; }
.lh img { height: 22px; width: auto; }
.lh span { font-family: var(--font-mono); font-size: 12.5px; color: var(--fg-faint); font-weight: 400; margin-left: auto; }
.ls { font-size: 14px; color: var(--fg-muted); line-height: 1.5; margin-top: 7px; }
.ls code { font-family: var(--font-mono); font-size: 12.5px; color: var(--c); }
.ar-code :deep(.slidev-code) { font-size: 12.5px !important; line-height: 1.45 !important; padding: 16px !important; }
.ar-notes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 22px; }
.note { border-left: 4px solid var(--c); border-radius: 10px; padding: 12px 16px; background: color-mix(in srgb, var(--c) 7%, transparent); }
.note-h { font-size: 16px; font-weight: 600; color: var(--c); }
.note-d { font-size: 13.5px; line-height: 1.5; color: var(--fg-muted); margin-top: 5px; }
.note-d code { font-family: var(--font-mono); font-size: 12px; color: var(--fg); }
.deepdive { margin-top: 22px; display: flex; flex-wrap: wrap; align-items: baseline; gap: 16px; }
.dd-label { font-family: var(--font-mono); font-size: 12px; color: var(--fg-faint); letter-spacing: 0.1em; text-transform: uppercase; }
</style>
