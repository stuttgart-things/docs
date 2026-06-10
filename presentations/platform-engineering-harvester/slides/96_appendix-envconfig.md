---
layout: default
class: 'is-appendix'
num: 'J · Appendix'
meta: 'Crossplane · EnvironmentConfig'
---

<div class="page-label">J · environmentconfig.yaml</div>

# <span class="accent">EnvironmentConfig</span><span class="dot">.</span>

```yaml
apiVersion: apiextensions.crossplane.io/v1beta1
kind: EnvironmentConfig
metadata:
  name: harvester-vm-defaults
  labels:
    harvester-vm.resources.stuttgart-things.com/environment: default
data:
  providerConfigRef: default
  storageClassName: harvester-longhorn
  namespace: vms
  networkName: default/vms
  imageId: default/image-ubuntu
```

<p class="lede" style="margin-top: 18px; max-width: 82ch;">
Per-environment defaults selected by label. One claim, many targets — swap the EnvironmentConfig to retarget storage, network and base image.
</p>

<style>
.slidev-code { font-size: 20px !important; line-height: 1.5 !important; padding: 26px !important; }
</style>
