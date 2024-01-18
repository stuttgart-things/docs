# stuttgart-things/docs/kustomize

## SNIPPETS

<details><summary><b>PATCH INGRESS W/ REPLACE</b></summary>

```bash
BASE_DIR=./kustomize/ingress
mkdir -p ${BASE_DIR}

cat <<EOF > ${BASE_DIR}/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ingress.yaml

patches:
  - target:
      kind: Ingress
      name: ingress
    patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: stuttgart-things.com
EOF

cat <<EOF > ${BASE_DIR}/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress
spec:
  ingressClassName: alb
  rules:
    - host: app.whatever.com
      http:
        paths:
        - backend:
            service:
             name: web
             port:
              number: 80
          pathType: ImplementationSpecific
EOF
```

```bash
# RENDER TO STDOUT
kubectl kustomize ${BASE_DIR}
```

</details>
