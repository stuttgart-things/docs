# stuttgart-things/docs/kubernetes-monitoring

## DEPLOY VPA

```bash
kubectl create ns monitoring
helm repo add fairwinds-stable https://charts.fairwinds.com/stable && helm repo update
helm upgrade --install vpa fairwinds-stable/vpa -n monitoring  --version 3.0.2 --create-namespace
helm -n monitoring test vpa
```

## FORKED GIT-REPOSITORY: FOR RKE CLUSTERS (at least for =<52.1.0)

```bash
git clone https://github.com/mohamadkhani/helm-charts.git
cd helm-charts/kube-prometheus-stack && helm dep update
```

## HELM REPO: NON RKE/RANCHER K8S

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

## CREATE TLS CERTIFICATE

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: monitoring-ingress
  namespace: monitoring
spec:
  commonName: monitoring.dev43.sthings-pve.labul.sva.de
  dnsNames:
    - monitoring.dev43.sthings-pve.labul.sva.de
  issuerRef:
    kind: ClusterIssuer
    name: cluster-issuer-approle
  secretName: monitoring-tls
```

## CREATE VALUES FILE

```yaml
cat <<EOF > ./values.yaml
alertmanager:
  enabled: false
prometheus:
  prometheusSpec:
    scrapeInterval: 30s
    evaluationInterval: 30s
    retention: 24h
    resources:
      requests:
        cpu: 200m
        memory: 200Mi
    podMonitorNamespaceSelector: { }
    podMonitorSelector:
      matchLabels:
        app.kubernetes.io/component: monitoring
grafana:
  defaultDashboardsEnabled: true
  adminPassword: <CHANGEME>
  ingress:
    enabled: true
    ingressClassName: nginx
    hosts:
      - monitoring.dev43.sthings-pve.labul.sva.de
    path: /
    tls:
      - secretName: monitoring-tls
        hosts:
          - monitoring.dev43.sthings-pve.labul.sva.de
kube-state-metrics:
  rbac:
    extraRules:
      - apiGroups: ["autoscaling.k8s.io"]
        resources: ["verticalpodautoscalers"]
        verbs: ["list", "watch"]
  prometheus:
    monitor:
      enabled: true
  customResourceState:
    enabled: true
    config:
      kind: CustomResourceStateMetrics
      spec:
        resources:
          - groupVersionKind:
              group: autoscaling.k8s.io
              kind: "VerticalPodAutoscaler"
              version: "v1"
            labelsFromPath:
              verticalpodautoscaler: [metadata, name]
              namespace: [metadata, namespace]
              target_api_version: [apiVersion]
              target_kind: [spec, targetRef, kind]
              target_name: [spec, targetRef, name]
            metrics:
              - name: "vpa_containerrecommendations_target"
                help: "VPA container recommendations for memory."
                each:
                  type: Gauge
                  gauge:
                    path: [status, recommendation, containerRecommendations]
                    valueFrom: [target, memory]
                    labelsFromPath:
                      container: [containerName]
                commonLabels:
                  resource: "memory"
                  unit: "byte"
              - name: "vpa_containerrecommendations_target"
                help: "VPA container recommendations for cpu."
                each:
                  type: Gauge
                  gauge:
                    path: [status, recommendation, containerRecommendations]
                    valueFrom: [target, cpu]
                    labelsFromPath:
                      container: [containerName]
                commonLabels:
                  resource: "cpu"
                  unit: "core"
  selfMonitor:
    enabled: true
EOF
```

## DEPLOY KUBE-PROMETHEUS-STACK

```bash
helm upgrade --install kube-prometheus-stack . --values values.yaml --version 52.1.0 --namespace monitoring --create-namespace
# OR W/ HELM REPOSITORY
helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack --values values.yaml --version 52.1.0 --namespace monitoring --create-namespace
```

## DEPLOY GOLDILOCKS

```bash
helm repo add fairwinds-stable https://charts.fairwinds.com/stable && helm repo update
helm upgrade --install goldilocks --namespace monitoring fairwinds-stable/goldilocks --version 8.0.0 --create-namespace
```

## LABEL NAMESPACE W/ GOLDILOCKS

```bash
kubectl label ns velero goldilocks.fairwinds.com/enabled=true
```

</details>


