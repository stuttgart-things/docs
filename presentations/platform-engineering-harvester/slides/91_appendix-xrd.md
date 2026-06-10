---
layout: default
class: 'is-appendix'
num: 'E · Appendix'
meta: 'Crossplane · XRD'
---

<div class="page-label">E · xrd.yaml</div>

# <span class="accent">CompositeResourceDefinition</span><span class="dot">.</span>

```yaml
apiVersion: apiextensions.crossplane.io/v2
kind: CompositeResourceDefinition
metadata:
  name: harvestervms.resources.stuttgart-things.com
spec:
  group: resources.stuttgart-things.com
  scope: Namespaced
  names:
    kind: HarvesterVM
    plural: harvestervms
  versions:
    - name: v1alpha1
      served: true
      referenceable: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                environmentConfig:   # selects per-env defaults
                  type: string
                  default: default
                providerConfigRef:   # env default, XR override
                  type: string
                vm:
                  type: object
```

<p class="lede" style="margin-top: 16px; max-width: 82ch;">
The <code>HarvesterVM</code> API — what a developer fills in. Fields like <code>providerConfigRef</code> default from the EnvironmentConfig and can be overridden per claim.
</p>

<style>
.slidev-code { font-size: 16px !important; line-height: 1.45 !important; padding: 22px !important; }
</style>
