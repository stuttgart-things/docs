---
layout: default
class: 'is-appendix'
num: 'I · Appendix'
meta: 'Crossplane · Configuration'
---

<div class="page-label">I · configuration.yaml</div>

# <span class="accent">Configuration</span> package<span class="dot">.</span>

```yaml
apiVersion: pkg.crossplane.io/v1
kind: Configuration
metadata:
  name: harvester-vm
spec:
  package: ghcr.io/stuttgart-things/crossplane-configurations/harvester-vm:v0.1.0
```

<p class="lede" style="margin-top: 18px; max-width: 82ch;">
XRD, Composition and Functions bundled into one versioned OCI package — installed into the cluster with a single resource.
</p>

<style>
.slidev-code { font-size: 22px !important; line-height: 1.55 !important; padding: 28px !important; }
</style>
