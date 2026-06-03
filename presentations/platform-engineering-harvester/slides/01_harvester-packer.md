---
layout: default
num: '01'
meta: 'Harvester · Packer'
---

<div class="page-label">01 · Create VM-Templates for Harvester</div>

# Create VM-Templates for <span class="accent">Harvester</span><span class="dot">.</span>

<p class="lede" style="margin-top: 24px; max-width: 70ch;">
Golden images for Harvester — built, versioned, and published to the catalog.
</p>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; margin-top: 56px;">
  <div class="surface" v-click style="padding: 32px; min-height: 220px;">
    <div class="mono" style="font-size: 14px; color: var(--accent); margin-bottom: 14px; letter-spacing: 0.14em;">01</div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">Backstage</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      Self-service template as the entry point for new images.
    </p>
  </div>
  <div class="surface" v-click style="padding: 32px; min-height: 220px;">
    <div class="mono" style="font-size: 14px; color: var(--accent); margin-bottom: 14px; letter-spacing: 0.14em;">02</div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">GitHub Workflow + Runner</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      Packer build on a self-hosted runner — reproducible in CI.
    </p>
  </div>
  <div class="surface" v-click style="padding: 32px; min-height: 220px;">
    <div class="mono" style="font-size: 14px; color: var(--accent); margin-bottom: 14px; letter-spacing: 0.14em;">03</div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">catalog.yaml</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      Published as a Backstage entity — discoverable in the software catalog.
    </p>
  </div>
</div>

<div class="slide-meta">
  <span>01 · Create VM-Templates for Harvester</span>
  <span>Packer · Backstage · Workflow</span>
</div>
