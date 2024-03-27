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

<details><summary><b>UPDATE/SET YAML KEYS</b></summary>

```bash
cat <<EOF > ./Chart.yaml
---
version: 1.2.3
EOF

# UPDATE KEY
yq e -i '.version = "1.2.4"' Chart.yaml

# SET KEY
yq e -i '.name = "serviceA"' Chart.yaml
```

</details>
