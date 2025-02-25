# KUBERNETES DEPLOYMENT

<details><summary>HELM-CLI</summary>

```bash
### ADD A REPO 
helm repo add headlamp https://headlamp-k8s.github.io/headlamp/
helm repo update

### SEARCH FOR CHARTS (+VERSIONS)
helm search repo headlamp --versions

### TEMPLATE (RENDER) w/ DEFAULS
helm template headlamp/headlamp --version 0.28.1 # = MANIFEST BASED ON DEFAULTS

### SHOW VALUES (SEE DEFAULT VARIABLE STRUCTURE)
helm show values headlamp/headlamp --version 0.28.1 # > values.yaml

## EXAMPLE ADDITION MANIFEST FOR A CERTIFICATE
kubectl create ns headlamp

kubectl apply -f - <<EOF
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: headlamp
  namespace: headlamp
spec:
  commonName: headlamp.rahul-story-test-rke.sthings-vsphere.labul.sva.de
  dnsNames:
    - headlamp.rahul-story-test-rke.sthings-vsphere.labul.sva.de
  issuerRef:
    kind: ClusterIssuer
    name: cluster-issuer-approle
  secretName: headlamp.rahul-story-test-rke.sthings-vsphere.labul.sva.de-tls
EOF

## EXAMPLE VALUES
cat <<EOF > values.yaml
---
ingress:
  enabled: true
  annotations:
    {}
    # kubernetes.io/tls-acme: "true"
  labels: {}
    # app.kubernetes.io/part-of: traefik
    # environment: prod
  ingressClassName: nginx
  hosts:
    - host: headlamp.rahul-story-test-rke.sthings-vsphere.labul.sva.de
      paths:
      - path: /
        type: ImplementationSpecific
  tls: 
   - secretName: headlamp.rahul-story-test-rke.sthings-vsphere.labul.sva.de-tls
     hosts:
       - headlamp.rahul-story-test-rke.sthings-vsphere.labul.sva.de
EOF

### TEMPLATE (RENDER) w/ CUSTOM VALUE FILE
helm template headlamp/headlamp --version 0.28.1 --values values.yaml # + e.g. | grep ingress -A30

### INSTALL + UPGRADE AT ONCE
helm upgrade --install headlamp headlamp/headlamp --version 0.28.1 --values headlamp.yaml -n headlamp --create-namespace
```

</details>
