---
layout: default
class: 'is-appendix'
num: 'B · Appendix'
meta: 'Crossplane · simple example · XRD'
---

<div class="page-label">B · namespace · xrd.yaml</div>

# Simple example — <span class="accent">XRD</span><span class="dot">.</span>

```yaml
apiVersion: apiextensions.crossplane.io/v2
kind: CompositeResourceDefinition
metadata:
  name: managednamespaces.resources.stuttgart-things.com
spec:
  group: resources.stuttgart-things.com
  scope: Namespaced
  names:
    kind: ManagedNamespace
    plural: managednamespaces
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
                providerConfigRef:   # target cluster
                  type: string
                name:                # namespace to create
                  type: string
                labels:
                  type: object
                resourceQuota:       # optional
                  type: object
              required:
                - providerConfigRef
                - name
```

<p class="lede" style="margin-top: 14px; max-width: 82ch;">
The same pattern as HarvesterVM, but tiny — a <code>ManagedNamespace</code> API with just a name, a target cluster and a few optional add-ons.
</p>

<style>
.slidev-code { font-size: 15px !important; line-height: 1.4 !important; padding: 20px !important; }
</style>
