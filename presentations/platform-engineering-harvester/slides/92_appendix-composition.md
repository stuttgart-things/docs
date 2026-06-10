---
layout: default
class: 'is-appendix'
num: 'F · Appendix'
meta: 'Crossplane · Composition'
---

<div class="page-label">F · composition.yaml</div>

# <span class="accent">Composition</span><span class="dot">.</span>

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: harvester-vm
  labels:
    crossplane.io/xrd: harvestervms.resources.stuttgart-things.com
spec:
  compositeTypeRef:
    apiVersion: resources.stuttgart-things.com/v1alpha1
    kind: HarvesterVM
  mode: Pipeline
  pipeline:
    - step: load-environment        # shared per-env defaults
      functionRef:
        name: function-environment-configs
      input:
        apiVersion: environmentconfigs.fn.crossplane.io/v1beta1
        kind: Input
        spec:
          environmentConfigs:
            - type: Selector
              selector:
                matchLabels:
                  - key: harvester-vm.resources.stuttgart-things.com/environment
                    type: FromCompositeFieldPath
                    valueFromFieldPath: spec.environmentConfig
    - step: create-resources        # PVC + cloud-init + VM
      functionRef:
        name: function-patch-and-transform
    - step: ready                   # mark XR ready
      functionRef:
        name: function-auto-ready
```

<p class="lede" style="margin-top: 14px; max-width: 82ch;">
A function <strong>pipeline</strong>: load environment defaults, render the managed resources, then signal readiness.
</p>

<style>
.slidev-code { font-size: 14px !important; line-height: 1.4 !important; padding: 20px !important; }
</style>
