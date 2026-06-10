---
layout: default
class: 'is-appendix'
num: 'C · Appendix'
meta: 'Crossplane · simple example · Composition'
---

<div class="page-label">C · namespace · composition.yaml</div>

# Simple example — <span class="accent">Composition</span><span class="dot">.</span>

```yaml
apiVersion: apiextensions.crossplane.io/v1
kind: Composition
metadata:
  name: managed-namespace
spec:
  compositeTypeRef:
    apiVersion: resources.stuttgart-things.com/v1alpha1
    kind: ManagedNamespace
  mode: Pipeline
  pipeline:
    - step: render-namespace
      functionRef:
        name: function-go-templating
      input:
        apiVersion: gotemplating.fn.crossplane.io/v1beta1
        kind: GoTemplate
        source: Inline
        inline:
          template: |
            {{- $spec := .observed.composite.resource.spec }}
            ---
            apiVersion: kubernetes.m.crossplane.io/v1alpha1
            kind: Object
            spec:
              providerConfigRef:
                name: {{ $spec.providerConfigRef }}
                kind: ClusterProviderConfig
              forProvider:
                manifest:
                  apiVersion: v1
                  kind: Namespace
                  metadata:
                    name: {{ $spec.name }}
                    {{- with $spec.labels }}
                    labels:
                      {{- range $k, $v := . }}
                      {{ $k }}: {{ $v | quote }}
                      {{- end }}
                    {{- end }}
```

<p class="lede" style="margin-top: 12px; max-width: 82ch;">
One templating step turns the claim into a single <code>Namespace</code> — the easiest way to see how a Composition renders resources.
</p>

<style>
.slidev-code { font-size: 13.5px !important; line-height: 1.38 !important; padding: 18px !important; }
</style>
