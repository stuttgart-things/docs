---
layout: default
num: '02'
meta: 'Harvester · Crossplane'
---

<div class="page-label">02 · Create Harvester VM with Crossplane</div>

# Create Harvester VM with <span class="accent">Crossplane</span><span class="dot">.</span>

<p class="lede" style="margin-top: 24px; max-width: 70ch;">
Declarative VMs on Harvester — provisioned as Kubernetes resources, reconciled continuously.
</p>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; margin-top: 56px;">
  <div class="surface" v-click style="padding: 32px; min-height: 220px;">
    <div class="mono" style="font-size: 14px; color: var(--accent); margin-bottom: 14px; letter-spacing: 0.14em;">01</div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">Crossplane</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      Composition + provider turn a VM claim into real Harvester resources.
    </p>
  </div>
  <div class="surface" v-click style="padding: 32px; min-height: 220px;">
    <div class="mono" style="font-size: 14px; color: var(--accent); margin-bottom: 14px; letter-spacing: 0.14em;">02</div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">Environment Config</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      Per-environment values injected into the composition — one claim, many targets.
    </p>
  </div>
  <div class="surface" v-click style="padding: 32px; min-height: 220px;">
    <div class="mono" style="font-size: 14px; color: var(--accent); margin-bottom: 14px; letter-spacing: 0.14em;">03</div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">GitOps</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      Claims live in Git — Argo CD applies and reconciles the desired state.
    </p>
  </div>
</div>

<div class="slide-meta">
  <span>02 · Create Harvester VM with Crossplane</span>
  <span>Crossplane · Environment Config · GitOps</span>
</div>
