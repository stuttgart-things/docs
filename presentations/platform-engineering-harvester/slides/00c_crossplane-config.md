---
layout: default
num: '00c · Crossplane · Configuration · claim-machinery-api'
meta: 'Crossplane · Configuration · claim-machinery-api'
---

<div class="page-label">00c · The machinery behind the namespace</div>

# Crossplane, Configuration &amp; the <span class="accent">claim API</span><span class="dot">.</span>

<p class="lede" style="margin-top: 24px; max-width: 78ch;">
The engine that reconciles the claim, the Configuration that owns the namespace, and the API that serves the claim templates.
</p>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; margin-top: 56px;">
  <div class="surface" style="padding: 32px; min-height: 260px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 34px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 14px; color: var(--accent); letter-spacing: 0.14em;">A</div>
      <img :src="'/logos/crossplane.svg'" alt="Crossplane" style="height: 36px; width: auto;" />
    </div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">Crossplane</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      Deployment, Komponenten &amp; Konzepte — Provider, XRD, Composition, Functions.
    </p>
    <div v-click="1" style="margin-top: 18px; display: flex; flex-direction: column; gap: 10px;">
      <a class="card-link" href="https://docs.crossplane.io/latest/concepts/" target="_blank">Crossplane Concepts</a>
      <a class="card-link" href="https://docs.crossplane.io/latest/software/install/" target="_blank">Deployment / Install</a>
      <a class="card-link" href="https://github.com/stuttgart-things/crossplane-configurations" target="_blank">crossplane-configurations</a>
    </div>
  </div>
  <div class="surface" style="padding: 32px; min-height: 260px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 34px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 14px; color: var(--accent); letter-spacing: 0.14em;">B</div>
      <img :src="'/logos/crossplane.svg'" alt="Crossplane Configuration" style="height: 36px; width: auto;" />
    </div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">Configuration · namespace</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      Crossplane v2 Configuration — turns a <span class="mono">ManagedNamespace</span> XR into a fully-managed Namespace.
    </p>
    <div v-click="1" style="margin-top: 18px; display: flex; flex-direction: column; gap: 10px;">
      <a class="card-link" href="https://github.com/stuttgart-things/crossplane-configurations/tree/main/k8s/namespace" target="_blank">k8s/namespace</a>
      <a class="card-link" href="https://github.com/stuttgart-things/crossplane-configurations/blob/main/k8s/namespace/apis/definition.yaml" target="_blank">XRD (definition.yaml)</a>
      <a class="card-link" href="https://github.com/stuttgart-things/crossplane-configurations/blob/main/k8s/namespace/apis/composition.yaml" target="_blank">Composition</a>
    </div>
  </div>
  <div class="surface" style="padding: 32px; min-height: 260px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 34px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 14px; color: var(--accent); letter-spacing: 0.14em;">C</div>
      <img :src="'/logos/kcl.svg'" alt="claim-machinery-api" style="height: 34px; width: auto;" />
    </div>
    <div style="font-size: 26px; font-weight: 600; line-height: 1.2;">claim-machinery-api</div>
    <p style="font-size: 18px; line-height: 1.4; margin-top: 10px; color: var(--fg-muted);">
      Backstage-kompatible API zum Discovern &amp; Rendern KCL-basierter Crossplane-Claim-Templates.
    </p>
    <div v-click="1" style="margin-top: 18px; display: flex; flex-direction: column; gap: 10px;">
      <a class="card-link" href="https://github.com/stuttgart-things/claim-machinery-api" target="_blank">claim-machinery-api</a>
      <a class="card-link" href="https://stuttgart-things.github.io/claim-machinery-api/" target="_blank">Documentation</a>
      <a class="card-link" href="https://github.com/stuttgart-things/kcl/tree/main/crossplane/xr-namespace" target="_blank">KCL · xr-namespace</a>
    </div>
  </div>
</div>
