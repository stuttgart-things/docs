---
layout: default
class: 'is-appendix'
num: 'D · Appendix'
meta: 'Crossplane · simple example · XR'
---

<div class="page-label">D · namespace · xr.yaml</div>

# Simple example — <span class="accent">XR / claim</span><span class="dot">.</span>

```yaml
apiVersion: resources.stuttgart-things.com/v1alpha1
kind: ManagedNamespace
metadata:
  name: team-alpha
  namespace: default
spec:
  providerConfigRef: in-cluster
  name: team-alpha
  labels:
    team: alpha
    env: dev
  roleBindings:
    - name: team-alpha-view
      roleRef:
        kind: ClusterRole
        name: view
      subjects:
        - kind: Group
          name: team-alpha
          apiGroup: rbac.authorization.k8s.io
```

<p class="lede" style="margin-top: 18px; max-width: 82ch;">
What a team applies — a name, some labels and a view RoleBinding. Crossplane creates and reconciles the namespace on the target cluster.
</p>

<style>
.slidev-code { font-size: 18px !important; line-height: 1.5 !important; padding: 24px !important; }
</style>
