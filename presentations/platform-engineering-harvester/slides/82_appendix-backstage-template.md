---
layout: default
class: 'is-appendix'
num: 'M · Appendix'
meta: 'Backstage · Software Template'
---

<div class="page-label">M · Backstage Software Template</div>

# A <span class="accent">Software Template</span><span class="dot">.</span>

<p class="lede" style="margin-top: 10px; max-width: 84ch;">
Self-service "Create Harvester Dev Image" — a form that opens an auto-merging PR and registers the result in the catalog.
</p>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; margin-top: 28px;">
  <div>
    <div class="mono" style="font-size: 13px; color: var(--accent); margin-bottom: 8px; letter-spacing: 0.14em;">1 · THE FORM</div>

```yaml
parameters:
  - title: Add New Users
    properties:
      users:
        type: array
        items:
          properties:
            name:
              type: string
            ssh_authorized_keys:
              type: array
```

  </div>
  <div>
    <div class="mono" style="font-size: 13px; color: var(--accent); margin-bottom: 8px; letter-spacing: 0.14em;">2 · THE ACTIONS</div>

```yaml
steps:
  - id: combine-users      # merge + dedupe
    action: roadiehq:utils:jsonata
  - id: create-pull-request
    action: publish:github:pull-request
    input:
      update: true         # auto-merge
  - id: register           # add to catalog
    action: catalog:register
```

  </div>
  <div>
    <div class="mono" style="font-size: 13px; color: var(--accent); margin-bottom: 8px; letter-spacing: 0.14em;">3 · THE OUTPUT</div>

```yaml
output:
  links:
    - title: Pull Request
      url: ${{ steps.create-pull-request
               .output.remoteUrl }}
    - title: Open in Catalog
      entityRef: ${{ steps.register
                     .output.entityRef }}
```

  </div>
</div>

<style>
.slidev-code { font-size: 13px !important; line-height: 1.4 !important; padding: 16px !important; }
</style>
