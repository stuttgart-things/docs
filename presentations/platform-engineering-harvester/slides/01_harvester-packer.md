---
layout: default
num: '01 · Create VM-Templates for Harvester'
meta: 'Packer · Backstage · Workflow'
---

<div class="page-label">01 · Create VM-Templates for Harvester</div>

# Create VM-Templates for <span class="accent">Harvester</span><span class="dot">.</span>

<p class="lede" style="margin-top: 24px; max-width: 70ch;">
Golden images for Harvester — built, versioned, and published to the catalog.
</p>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; margin-top: 56px;">
  <div class="surface" style="padding: 32px; min-height: 240px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 34px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 14px; color: var(--accent); letter-spacing: 0.14em;">A</div>
      <img :src="'/logos/backstage.svg'" alt="Backstage" style="height: 40px; width: auto;" />
    </div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">Backstage</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      Self-service template + software catalog — the entry point for new images.
    </p>
    <div v-click="1" style="margin-top: 18px; display: flex; flex-direction: column; gap: 12px;">
      <div>
        <div class="mono" style="font-size: 12px; color: var(--fg-faint); letter-spacing: 0.12em; margin-bottom: 6px;">EDGE</div>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
          <a class="card-link" href="https://backstage.platform.sthings.lab/create" target="_blank">Portal</a>
          <a class="card-link" href="https://backstage.platform.sthings.lab/catalog" target="_blank">Catalog</a>
        </div>
      </div>
      <div>
        <div class="mono" style="font-size: 12px; color: var(--fg-faint); letter-spacing: 0.12em; margin-bottom: 6px;">LAB</div>
        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
          <a class="card-link" href="https://backstage.platform.sthings-vsphere.labul.sva.de/create" target="_blank">Portal</a>
          <a class="card-link" href="https://backstage.platform.sthings-vsphere.labul.sva.de/catalog" target="_blank">Catalog</a>
        </div>
      </div>
      <a class="card-link" href="https://github.com/stuttgart-things/backstage-resources/tree/main/templates/golang-service" target="_blank">Golang Service Template</a>
      <a class="card-link" href="/13">Example catalog-info.yaml →</a>
      <a class="card-link" href="/26">Software template example →</a>
    </div>
  </div>
  <div class="surface" style="padding: 32px; min-height: 240px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 34px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 14px; color: var(--accent); letter-spacing: 0.14em;">B</div>
      <img :src="'/logos/harvester.svg'" alt="Harvester" style="height: 32px; width: auto;" />
    </div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">Harvester</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      HCI platform for VM and Kubernetes workloads.
    </p>
    <div v-click="1" style="margin-top: 18px; display: flex; flex-direction: column; gap: 10px;">
      <a class="card-link" href="https://harvester.sthings.lab/" target="_blank">Harvester · sthings.lab</a>
      <a class="card-link" href="/24">Harvester (SUSE) →</a>
      <a class="card-link" href="/25">Rancher →</a>
    </div>
  </div>
  <div class="surface" style="padding: 32px; min-height: 240px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 34px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 14px; color: var(--accent); letter-spacing: 0.14em;">C</div>
      <img :src="'/logos/github.svg'" alt="GitHub" style="height: 40px; width: auto;" />
    </div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">GitHub Workflow + Runner</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      Packer build on a self-hosted runner — reproducible in CI.
    </p>
    <div v-click="1" style="margin-top: 18px; display: flex; flex-direction: column; gap: 10px;">
      <a class="card-link" href="https://github.com/stuttgart-things/harvester/tree/main/packer" target="_blank">Harvester Packer Code</a>
    </div>
  </div>
</div>
