# stuttgart-things/docs/terraform

<details open><summary>INIT|APPLY|DESTROY</summary>

```
terraform init
terraform plan
terraform apply
terraform destroy
```

</details close>

## AWS

<details open><summary>AWS CLI</summary>
  
```
sudo apt -y install awscli
aws configure
```

</details close>

<details open><summary>provider.tf</summary>

```
terraform {
  required_version = ">= 1.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.8"
    }
  }
}
```

</details close>

## CREATE GENERATED SECRET IN AWS SECRETS MANAGER 

<details open><summary>random-secret-aws.tf</summary>

```
mkdir -p ./aws-secrets

cat <<EOF > ./aws-secrets/random-secret-aws.tf
provider "aws" {
  region = "eu-central-1"
}

locals {
  secret_name = "admin"
  admin_user  = "chef"
}

# CREATE A RANDOM PASSWORD
resource "random_password" "admin" {
  length  = 32
  lower   = true
  numeric = true
  special = false
  upper   = true
}

# CREATE SECRET
resource "aws_secretsmanager_secret" "admin_secret" {
  name                    = local.secret_name
  recovery_window_in_days = 0
}

# WRITE INTO AWS SECRETS MANAGER
resource "aws_secretsmanager_secret_version" "admin_secret_version" {
  secret_id = aws_secretsmanager_secret.admin_secret.id
  secret_string = jsonencode({
    admin    = local.admin_user
    password = random_password.admin.result
  })
}
EOF
```

</details close>


</details close>


## OUTPUT/USE SECRET FROM AWS SECRETS MANAGER

<details open><summary>random-secret-aws.tf</summary>

```
data "aws_secretsmanager_secret" "msk_secrets" {
    arn = "arn:aws:secretsmanager:eu-central-1:367557680358:secret:AmazonMSK_example-vfUxyF"
}

data "aws_secretsmanager_secret_version" "secret_version" {
  secret_id = data.aws_secretsmanager_secret.msk_secrets.id
}

# 
output "secret_string" {
  value = jsondecode(nonsensitive(data.aws_secretsmanager_secret_version.secret_version.secret_string))["username"]
}
```

</details close>


## CREATE INLINE KUBERNETES (YAML) RESOURCES

<details open><summary>akhq_ingress.tf</summary>

```
resource "kubectl_manifest" "akhq_ingress" {
  yaml_body = <<YAML
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/hostname: ${format("akhq.%s", local.example_domain)}
    alb.ingress.kubernetes.io/certificate-arn: ${local.csr_certificate_arn}
    service.beta.kubernetes.io/aws-load-balancer-ssl-ports: 443,80
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: tls
    service.beta.kubernetes.io/aws-load-balancer-ssl-negotiation-policy: ${var.alb_ssl_policy}
    alb.ingress.kubernetes.io/ssl-policy: ${var.alb_ssl_policy}
    alb.ingress.kubernetes.io/subnets: subnet-ID1,subnet-ID2
    alb.ingress.kubernetes.io/target-type: instance
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/auth-on-unauthenticated-request: deny
    alb.ingress.kubernetes.io/load-balancer-attributes: routing.http2.enabled=true,idle_timeout.timeout_seconds=60
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTP": 80}, {"HTTPS":443}]'
    alb.ingress.kubernetes.io/healthcheck-path: /api/me
    alb.ingress.kubernetes.io/group.order: "2"
    alb.ingress.kubernetes.io/group.name: akhq
  labels:
    app.kubernetes.io/instance: akhq
    app.kubernetes.io/name: akhq
  name: akhq
  namespace: akhq
spec:
  ingressClassName: alb
  rules:
  - host: ${format("akhq.%s", local.example_domain)}
    http:
      paths:
      - backend:
          service:
            name: akhq
            port:
              name: http
        path: /
        pathType: Prefix
YAML
}
```

</details close>


<details open><summary>deploy-streamzi-msk.tf</summary>

```yaml
resource "kubectl_manifest" "template_topic" {
  yaml_body = <<YAML
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: ${var.msk_topic_prefix}-template
  namespace: ${var.application_namespace}
  labels:
    strimzi.io/cluster: ${var.msk_topic_prefix}-cluster
spec:
  partitions: 1
  replicas: 1
  config:
    retention.ms: 7200000
    segment.bytes: 1073741824
YAML

  depends_on = [
    kubectl_manifest.strimzi_deployment
  ]
}


resource "kubectl_manifest" "server_topic" {
  yaml_body = <<YAML
apiVersion: kafka.strimzi.io/v1beta2
kind: KafkaTopic
metadata:
  name: ${var.msk_topic_prefix}-study
  namespace: ${var.application_namespace}
  labels:
    strimzi.io/cluster: ${var.msk_topic_prefix}-cluster
spec:
  partitions: 1
  replicas: 1
  config:
    retention.ms: 7200000
    segment.bytes: 1073741824
YAML

  depends_on = [
    kubectl_manifest.strimzi_deployment
  ]
}

resource "kubectl_manifest" "strimzi_deployment" {
  yaml_body = <<YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: strimzi-topic-operator
  namespace: ${var.application_namespace}
  labels:
    app: strimzi
spec:
  replicas: 1
  selector:
    matchLabels:
      name: strimzi-topic-operator
  template:
    metadata:
      labels:
        name: strimzi-topic-operator
    spec:
      serviceAccountName: strimzi-topic-operator
      volumes:
        - name: strimzi-tmp
          emptyDir:
            medium: Memory
            sizeLimit: 5Mi
      containers:
        - name: strimzi-topic-operator
          image: quay.io/strimzi/operator:0.37.0
          args:
            - /opt/strimzi/bin/topic_operator_run.sh
          volumeMounts:
            - name: strimzi-tmp
              mountPath: /tmp
          env:
            - name: STRIMZI_TLS_ENABLED
              value: "true"
            - name: STRIMZI_PUBLIC_CA
              value: "true"
            - name: STRIMZI_TLS_AUTH_ENABLED
              value: "false"
            - name: STRIMZI_SASL_ENABLED
              value: "true"
            - name: STRIMZI_SASL_MECHANISM
              value: "scram-sha-512"
            - name: STRIMZI_SASL_USERNAME
              value: "${jsondecode(nonsensitive(data.aws_secretsmanager_secret_version.secret_version.secret_string))["username"]}"
            - name: STRIMZI_SASL_PASSWORD
              value: "${jsondecode(nonsensitive(data.aws_secretsmanager_secret_version.secret_version.secret_string))["password"]}"
            - name: STRIMZI_SECURITY_PROTOCOL
              value: "SASL_SSL"
            - name: STRIMZI_RESOURCE_LABELS
              value: "strimzi.io/cluster=${var.msk_topic_prefix}-cluster"
            - name: STRIMZI_KAFKA_BOOTSTRAP_SERVERS
              value: ${module.kafka[0].bootstrap_brokers_sasl_scram}
            - name: STRIMZI_ZOOKEEPER_CONNECT
              value: ${module.kafka[0].zookeeper_connect_string}
            - name: STRIMZI_ZOOKEEPER_SESSION_TIMEOUT_MS
              value: "18000"
            - name: STRIMZI_FULL_RECONCILIATION_INTERVAL_MS
              value: "120000"
            - name: STRIMZI_TOPIC_METADATA_MAX_ATTEMPTS
              value: "6"
            - name: STRIMZI_LOG_LEVEL
              value: INFO
            - name: STRIMZI_NAMESPACE
              value: "${var.application_namespace}"
          livenessProbe:
            httpGet:
              path: /healthy
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 30
          resources:
            limits:
              memory: 256Mi
              cpu: 500m
            requests:
              memory: 256Mi
              cpu: 100m
  strategy:
    type: Recreate
YAML

  depends_on = [
    kubectl_manifest.strimzi_role_binding
  ]
}

resource "kubectl_manifest" "strimzi_role_binding" {
  yaml_body = <<YAML
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: strimzi-topic-operator
  namespace: ${var.application_namespace}
  labels:
    app: strimzi
subjects:
  - kind: ServiceAccount
    name: strimzi-topic-operator
    namespace: ${var.application_namespace}
roleRef:
  kind: Role
  name: strimzi-topic-operator
  apiGroup: rbac.authorization.k8s.io
YAML

  depends_on = [
    kubectl_manifest.strimzi_role
  ]

}

resource "kubectl_manifest" "strimzi_role" {
  yaml_body = <<YAML
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: strimzi-topic-operator
  namespace: ${var.application_namespace}
  labels:
    app: strimzi
rules:
- apiGroups:
  - "kafka.strimzi.io"
  resources:
  - kafkatopics
  - kafkatopics/status
  verbs:
  - get
  - list
  - watch
  - create
  - patch
  - update
  - delete
- apiGroups:
  - ""
  resources:
  - events
  verbs:
  - create
YAML

  depends_on = [
    kubectl_manifest.strimzi_crds
  ]

}

resource "kubectl_manifest" "strimzi_crds" {
  yaml_body = <<YAML
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: kafkatopics.kafka.strimzi.io
  labels:
    app: strimzi
    strimzi.io/crd-install: "true"
spec:
  group: kafka.strimzi.io
  names:
    kind: KafkaTopic
    listKind: KafkaTopicList
    singular: kafkatopic
    plural: kafkatopics
    shortNames:
    - kt
    categories:
    - strimzi
  scope: Namespaced
  conversion:
    strategy: None
  versions:
  - name: v1beta2
    served: true
    storage: true
    subresources:
      status: {}
    additionalPrinterColumns:
    - name: Cluster
      description: The name of the Kafka cluster this topic belongs to
      jsonPath: .metadata.labels.strimzi\.io/cluster
      type: string
    - name: Partitions
      description: The desired number of partitions in the topic
      jsonPath: .spec.partitions
      type: integer
    - name: Replication factor
      description: The desired number of replicas of each partition
      jsonPath: .spec.replicas
      type: integer
    - name: Ready
      description: The state of the custom resource
      jsonPath: ".status.conditions[?(@.type==\"Ready\")].status"
      type: string
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              partitions:
                type: integer
                minimum: 1
                description: "The number of partitions the topic should have. This cannot be decreased after topic creation. It can be increased after topic creation, but it is important to understand the consequences that has, especially for topics with semantic partitioning. When absent this will default to the broker configuration for `num.partitions`."
              replicas:
                type: integer
                minimum: 1
                maximum: 32767
                description: The number of replicas the topic should have. When absent this will default to the broker configuration for `default.replication.factor`.
              config:
                x-kubernetes-preserve-unknown-fields: true
                type: object
                description: The topic configuration.
              topicName:
                type: string
                description: The name of the topic. When absent this will default to the metadata.name of the topic. It is recommended to not set this unless the topic name is not a valid Kubernetes resource name.
            description: The specification of the topic.
          status:
            type: object
            properties:
              conditions:
                type: array
                items:
                  type: object
                  properties:
                    type:
                      type: string
                      description: "The unique identifier of a condition, used to distinguish between other conditions in the resource."
                    status:
                      type: string
                      description: "The status of the condition, either True, False or Unknown."
                    lastTransitionTime:
                      type: string
                      description: "Last time the condition of a type changed from one status to another. The required format is 'yyyy-MM-ddTHH:mm:ssZ', in the UTC time zone."
                    reason:
                      type: string
                      description: The reason for the condition's last transition (a single word in CamelCase).
                    message:
                      type: string
                      description: Human-readable message indicating details about the condition's last transition.
                description: List of status conditions.
              observedGeneration:
                type: integer
                description: The generation of the CRD that was last reconciled by the operator.
              topicName:
                type: string
                description: Topic name.
            description: The status of the topic.
  - name: v1beta1
    served: true
    storage: false
    subresources:
      status: {}
    additionalPrinterColumns:
    - name: Cluster
      description: The name of the Kafka cluster this topic belongs to
      jsonPath: .metadata.labels.strimzi\.io/cluster
      type: string
    - name: Partitions
      description: The desired number of partitions in the topic
      jsonPath: .spec.partitions
      type: integer
    - name: Replication factor
      description: The desired number of replicas of each partition
      jsonPath: .spec.replicas
      type: integer
    - name: Ready
      description: The state of the custom resource
      jsonPath: ".status.conditions[?(@.type==\"Ready\")].status"
      type: string
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              partitions:
                type: integer
                minimum: 1
                description: "The number of partitions the topic should have. This cannot be decreased after topic creation. It can be increased after topic creation, but it is important to understand the consequences that has, especially for topics with semantic partitioning. When absent this will default to the broker configuration for `num.partitions`."
              replicas:
                type: integer
                minimum: 1
                maximum: 32767
                description: The number of replicas the topic should have. When absent this will default to the broker configuration for `default.replication.factor`.
              config:
                x-kubernetes-preserve-unknown-fields: true
                type: object
                description: The topic configuration.
              topicName:
                type: string
                description: The name of the topic. When absent this will default to the metadata.name of the topic. It is recommended to not set this unless the topic name is not a valid Kubernetes resource name.
            description: The specification of the topic.
          status:
            type: object
            properties:
              conditions:
                type: array
                items:
                  type: object
                  properties:
                    type:
                      type: string
                      description: "The unique identifier of a condition, used to distinguish between other conditions in the resource."
                    status:
                      type: string
                      description: "The status of the condition, either True, False or Unknown."
                    lastTransitionTime:
                      type: string
                      description: "Last time the condition of a type changed from one status to another. The required format is 'yyyy-MM-ddTHH:mm:ssZ', in the UTC time zone."
                    reason:
                      type: string
                      description: The reason for the condition's last transition (a single word in CamelCase).
                    message:
                      type: string
                      description: Human-readable message indicating details about the condition's last transition.
                description: List of status conditions.
              observedGeneration:
                type: integer
                description: The generation of the CRD that was last reconciled by the operator.
              topicName:
                type: string
                description: Topic name.
            description: The status of the topic.
  - name: v1alpha1
    served: true
    storage: false
    subresources:
      status: {}
    additionalPrinterColumns:
    - name: Cluster
      description: The name of the Kafka cluster this topic belongs to
      jsonPath: .metadata.labels.strimzi\.io/cluster
      type: string
    - name: Partitions
      description: The desired number of partitions in the topic
      jsonPath: .spec.partitions
      type: integer
    - name: Replication factor
      description: The desired number of replicas of each partition
      jsonPath: .spec.replicas
      type: integer
    - name: Ready
      description: The state of the custom resource
      jsonPath: ".status.conditions[?(@.type==\"Ready\")].status"
      type: string
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              partitions:
                type: integer
                minimum: 1
                description: "The number of partitions the topic should have. This cannot be decreased after topic creation. It can be increased after topic creation, but it is important to understand the consequences that has, especially for topics with semantic partitioning. When absent this will default to the broker configuration for `num.partitions`."
              replicas:
                type: integer
                minimum: 1
                maximum: 32767
                description: The number of replicas the topic should have. When absent this will default to the broker configuration for `default.replication.factor`.
              config:
                x-kubernetes-preserve-unknown-fields: true
                type: object
                description: The topic configuration.
              topicName:
                type: string
                description: The name of the topic. When absent this will default to the metadata.name of the topic. It is recommended to not set this unless the topic name is not a valid Kubernetes resource name.
            description: The specification of the topic.
          status:
            type: object
            properties:
              conditions:
                type: array
                items:
                  type: object
                  properties:
                    type:
                      type: string
                      description: "The unique identifier of a condition, used to distinguish between other conditions in the resource."
                    status:
                      type: string
                      description: "The status of the condition, either True, False or Unknown."
                    lastTransitionTime:
                      type: string
                      description: "Last time the condition of a type changed from one status to another. The required format is 'yyyy-MM-ddTHH:mm:ssZ', in the UTC time zone."
                    reason:
                      type: string
                      description: The reason for the condition's last transition (a single word in CamelCase).
                    message:
                      type: string
                      description: Human-readable message indicating details about the condition's last transition.
                description: List of status conditions.
              observedGeneration:
                type: integer
                description: The generation of the CRD that was last reconciled by the operator.
              topicName:
                type: string
                description: Topic name.
            description: The status of the topic.
YAML

  depends_on = [
    kubectl_manifest.strimzi_service_account
  ]

}

resource "kubectl_manifest" "strimzi_service_account" {
  yaml_body = <<YAML
apiVersion: v1
kind: ServiceAccount
metadata:
  name: strimzi-topic-operator
  namespace: ${var.application_namespace}
  labels:
    app: strimzi
YAML

  depends_on = [
    helm_release.akhq
  ]

}
```
</details close>

## HELM CHART DEPLOYMENT

<details open><summary>helm-akhq.tf</summary>

```
provider "helm" {
  kubernetes {
    config_path = "~/.kube/dev11"
  }
}

resource "helm_release" "akhq" {
  count      =  1
  name             = "akhq"
  namespace        = "akhq2"
  create_namespace = true
  repository       = "https://akhq.io"
  chart            = "akhq"
  version          = "0.3.1"
  atomic           = true
  timeout          = 240

  values = [
    yamlencode({
      akhq = {
        server = {
          access-log = {
            enabled = true
            name = "org.akhq.log.access"
          }
        }
      }
      secrets = {
        akhq = {
          connections = {
            my-cluster-sasl = {
              properties  = {
                "bootstrap.servers" = "my-release-kafka.akhq.svc.cluster.local:9092"
                "security.protocol" = "SASL_PLAINTEXT"
                "sasl.mechanism" = "SCRAM-SHA-512"
                "sasl.jaas.config" = "org.apache.kafka.common.security.scram.ScramLoginModule required username='user1' password='ssq15oEwl3';"
               }
            }
          }
        }
      }
  })]

}
```
</details close>
