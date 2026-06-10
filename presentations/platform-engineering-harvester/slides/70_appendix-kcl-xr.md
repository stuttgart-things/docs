---
layout: default
class: 'is-appendix'
num: 'N · Appendix'
meta: 'KCL · high-level VM API'
---

<div class="page-label">N · virtual-machine · xr.yaml</div>

# A high-level <span class="accent">VM API</span><span class="dot">.</span>

```yaml
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: XVirtualMachine
metadata:
  name: vm-harvester
  namespace: default
spec:
  size: medium          # → cpu / ram / disk (via KCL)
  provider: harvester   # harvester | vsphere | proxmox
  environment: labul    # picks the EnvironmentConfig topology
  os: ubuntu24
  ansible: true         # base-OS provisioning once the VM boots
```

<p class="lede" style="margin-top: 18px; max-width: 84ch;">
One opinionated XR — ask for a VM by <strong>t-shirt size</strong> and <strong>provider</strong>. A KCL Composition and a stack of nested Configurations do the rest.
</p>

<style>
.slidev-code { font-size: 18px !important; line-height: 1.5 !important; padding: 24px !important; }
</style>
