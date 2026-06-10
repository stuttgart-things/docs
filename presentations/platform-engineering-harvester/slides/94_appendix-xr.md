---
layout: default
class: 'is-appendix'
num: 'H · Appendix'
meta: 'Crossplane · XR / claim'
---

<div class="page-label">H · xr.yaml</div>

# Composite Resource <span class="accent">(claim)</span><span class="dot">.</span>

```yaml
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: HarvesterVM
metadata:
  name: harvester-vm-min
  namespace: default
spec:
  environmentConfig: default     # pull shared env defaults
  volume:
    pvcName: harvester-vm-min-disk
  cloudInit:
    vmName: harvester-vm-min
    hostname: harvester-vm-min
  vm:
    cpu:
      cores: 1
    resources:
      memory: 1Gi
      cpu: "1"
```

<p class="lede" style="margin-top: 18px; max-width: 82ch;">
What a developer actually applies — minimal fields. Everything else (provider, storage class, network, image) comes from the EnvironmentConfig.
</p>

<style>
.slidev-code { font-size: 19px !important; line-height: 1.5 !important; padding: 26px !important; }
</style>
