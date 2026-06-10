---
layout: default
class: 'is-appendix'
num: 'G · Appendix'
meta: 'Crossplane · Function (templating)'
---

<div class="page-label">G · function-go-templating</div>

# A <span class="accent">Function</span> in action<span class="dot">.</span>

```yaml
- step: create-vm
  functionRef:
    name: function-go-templating
  input:
    apiVersion: gotemplating.fn.crossplane.io/v1beta1
    kind: GoTemplate
    source: Inline
    inline:
      template: |
        {{- $xr  := .observed.composite.resource }}
        {{- $env := index .context
              "apiextensions.crossplane.io/environment" | default dict }}
        ---
        apiVersion: kubevirt.io/v1
        kind: VirtualMachine
        metadata:
          name: {{ $xr.spec.cloudInit.vmName }}
          namespace: {{ $xr.spec.cloudInit.namespace
                        | default $env.namespace | default "vms" }}
        spec:
          runStrategy: {{ $xr.spec.vm.runStrategy | default "RerunOnFailure" }}
          template:
            spec:
              domain:
                cpu:
                  cores: {{ $xr.spec.vm.cpu.cores }}
                resources:
                  limits:
                    memory: {{ $xr.spec.vm.resources.memory }}
```

<p class="lede" style="margin-top: 14px; max-width: 82ch;">
A Function transforms inputs into resources. Here <code>function-go-templating</code> reads the XR and EnvironmentConfig and templates the VirtualMachine — with <code>default</code> fallbacks for unset fields.
</p>

<style>
.slidev-code { font-size: 14.5px !important; line-height: 1.4 !important; padding: 20px !important; }
</style>
