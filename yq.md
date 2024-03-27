# stuttgart-things/docs/yq

## SNIPPETS

<details><summary><b>READ YAML KEYS</b></summary>

```bash
cat <<EOF > ./collection.yaml
---
name: deploy_rke
namespace: sthings
requirements: |
  roles:
    - src: https://github.com/stuttgart-things/deploy-configure-rke.git
      scm: git
      version: main
EOF

yq -r ".name" ./collection.yaml # = deploy_rke
yq -r ".requirements" ./collection.yaml # = roles ..
```

</details>
