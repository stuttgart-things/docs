---
layout: default
num: '00 · Intro'
meta: 'Platform Engineering · Backstage · Harvester · GitOps · CI/CD'
---

<div class="page-label">00 · Intro</div>

# What we'll <span class="accent">cover</span><span class="dot">.</span>

<p class="lede" style="margin-top: 24px; max-width: 78ch;">
The building blocks — infrastructure, pipelines and delivery, the portal, and the practice that ties them together.
</p>

<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 26px; margin-top: 48px;">
  <div class="surface" style="flex: 0 1 calc(33.333% - 18px); padding: 34px; min-height: 200px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 36px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 15px; color: var(--accent); letter-spacing: 0.14em;">A</div>
    </div>
    <div style="font-size: 28px; font-weight: 600; line-height: 1.2;">Platform Engineering</div>
    <p style="font-size: 19px; line-height: 1.45; margin-top: 12px; color: var(--fg-muted);">
      The method: personas, golden paths, product thinking.
    </p>
  </div>
  <div class="surface" style="flex: 0 1 calc(33.333% - 18px); padding: 34px; min-height: 200px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 36px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 15px; color: var(--accent); letter-spacing: 0.14em;">B</div>
      <img :src="'/logos/backstage.svg'" alt="Backstage" style="height: 42px; width: auto;" />
    </div>
    <div style="font-size: 28px; font-weight: 600; line-height: 1.2;">Backstage</div>
    <p style="font-size: 19px; line-height: 1.45; margin-top: 12px; color: var(--fg-muted);">
      Developer portal as the golden-path frontend.
    </p>
  </div>
  <div class="surface" style="flex: 0 1 calc(33.333% - 18px); padding: 34px; min-height: 200px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 36px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 15px; color: var(--accent); letter-spacing: 0.14em;">C</div>
      <img :src="'/logos/harvester.svg'" alt="Harvester" style="height: 34px; width: auto;" />
    </div>
    <div style="font-size: 28px; font-weight: 600; line-height: 1.2;">Harvester</div>
    <p style="font-size: 19px; line-height: 1.45; margin-top: 12px; color: var(--fg-muted);">
      HCI platform for VM and Kubernetes workloads.
    </p>
  </div>
  <div class="surface" style="flex: 0 1 calc(33.333% - 18px); padding: 34px; min-height: 200px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 36px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 15px; color: var(--accent); letter-spacing: 0.14em;">D</div>
      <img :src="'/logos/argo.svg'" alt="Argo CD" style="height: 42px; width: auto;" />
    </div>
    <div style="font-size: 28px; font-weight: 600; line-height: 1.2;">GitOps</div>
    <p style="font-size: 19px; line-height: 1.45; margin-top: 12px; color: var(--fg-muted);">
      Git as source of truth — Argo CD reconciles every cluster.
    </p>
  </div>
  <div class="surface" style="flex: 0 1 calc(33.333% - 18px); padding: 34px; min-height: 200px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 36px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 15px; color: var(--accent); letter-spacing: 0.14em;">E</div>
      <img :src="'/logos/tekton.svg'" alt="Tekton" style="height: 42px; width: auto;" />
    </div>
    <div style="font-size: 28px; font-weight: 600; line-height: 1.2;">CI/CD</div>
    <p style="font-size: 19px; line-height: 1.45; margin-top: 12px; color: var(--fg-muted);">
      Pipelines build, test and ship — Tekton &amp; GitHub workflows.
    </p>
  </div>
  <div class="surface" style="flex: 0 1 calc(33.333% - 18px); padding: 34px; min-height: 200px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 36px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 15px; color: var(--accent); letter-spacing: 0.14em;">F</div>
      <img :src="'/logos/kubevirt.svg'" alt="KubeVirt" style="height: 42px; width: auto;" />
    </div>
    <div style="font-size: 28px; font-weight: 600; line-height: 1.2;">KubeVirt</div>
    <p style="font-size: 19px; line-height: 1.45; margin-top: 12px; color: var(--fg-muted);">
      Runs VMs as Kubernetes workloads — the engine inside Harvester.
    </p>
  </div>
</div>
