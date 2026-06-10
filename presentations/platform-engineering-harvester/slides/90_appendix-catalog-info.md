---
layout: default
class: 'is-appendix'
num: 'A · Appendix'
meta: 'Backstage · catalog-info example'
---

<div class="page-label">A · catalog-info.yaml</div>

# Example <span class="accent">catalog-info</span><span class="dot">.</span>

```yaml
apiVersion: backstage.io/v1alpha1
kind: Resource
metadata:
  name: sthings-leap-packer-image
  description: sthings-leap golden Packer base image for Harvester
  annotations:
    github.com/project-slug: stuttgart-things/harvester
    sthings.lab/last-modified-by: patrick hermann
  tags:
    - harvester
    - packer
    - golden
    - leap
spec:
  type: packer-image-golden
  lifecycle: production
  owner: platform-team
  profile:
    baseImage: leap15
    addedUsers:
      - sthings
```

<p class="lede" style="margin-top: 18px; max-width: 82ch;">
A golden Packer base image registered as a Backstage <code>Resource</code> entity — discoverable in the software catalog.
</p>

<style>
.slidev-code { font-size: 19px !important; line-height: 1.5 !important; padding: 26px !important; }
</style>
