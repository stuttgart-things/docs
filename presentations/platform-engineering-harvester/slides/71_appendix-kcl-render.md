---
layout: default
class: 'is-appendix'
num: 'O · Appendix'
meta: 'KCL · function-kcl render'
---

<div class="page-label">O · function-kcl</div>

# Compose with <span class="accent">KCL</span><span class="dot">.</span> <img :src="'/logos/kcl.svg'" alt="KCL" style="height: 30px; width: auto; vertical-align: -3px; margin-left: 6px;" />

```yaml
- step: render
  functionRef:
    name: function-kcl
  input:
    apiVersion: krm.kcl.dev/v1alpha1
    kind: KCLInput
    spec:
      source: |
        oxr = option("params").oxr
        _spec = oxr.spec
        _provider = _spec.provider          # harvester | vsphere | proxmox
        _ctx = option("params").ctx or {}
        _env = _ctx["apiextensions.crossplane.io/environment"][_provider]

        # t-shirt size → cpu / ram / disk
        _sizes = {
            small:  {cpu: "2",  ram: "2048",  disk: "32"}
            medium: {cpu: "4",  ram: "4096",  disk: "64"}
            large:  {cpu: "8",  ram: "8192",  disk: "128"}
            xlarge: {cpu: "16", ram: "16384", disk: "256"}
        }
        _size = _sizes[_spec.size]

        # provider routing — topology block picked by provider
        _vsphere = {network: _env.network} if _provider == "vsphere" else {}
        _proxmox = {node: _env.node}       if _provider == "proxmox" else {}

        # route to the matching lower-level resource
        _vm = {
            apiVersion = "resources.stuttgart-things.com/v1alpha1"
            kind = "HarvesterVM" if _provider == "harvester" else "VMProvision"
            metadata.name = oxr.metadata.name
            spec.vm = {cpu: _size.cpu, ram: _size.ram, disk: _size.disk}
            if _provider == "vsphere":
                spec.vsphere = _vsphere
            if _provider == "proxmox":
                spec.proxmox = _proxmox
        }
```

<p class="lede" style="margin-top: 12px; max-width: 86ch;">
KCL as the composition language — t-shirt sizing and provider routing (<code>if _provider == …</code>) decide which lower-level resource gets emitted, no long patch chains.
</p>

<style>
.slidev-code { font-size: 13px !important; line-height: 1.38 !important; padding: 18px !important; }
</style>
