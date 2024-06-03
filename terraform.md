# stuttgart-things/docs/terraform

## GENERAL

<details><summary><b>INSTALL TERRAFORM CLI (AS BINARY)</b></summary>

```bash
TERRAFORM_VERSION=1.7.5
wget -O terraform.zip https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
sudo unzip terraform.zip -d /usr/bin/
rm terraform.zip
terraform --version
```

</details>

<details><summary><b>REMOTE STATE</b></summary>

## MINIO

```hcl
terraform {
  backend "s3" {

    endpoints = {
      s3 = "https://artifacts.app1.sthings-vsphere.labul.sva.de"
    }
    skip_requesting_account_id = true
    skip_s3_checksum = true
    key = "cologne2.tfstate"
    bucket = "vspherevm-labul"
    region = "main"
    skip_credentials_validation = true
    skip_metadata_api_check = true
    skip_region_validation = true
    use_path_style = true
    workspace_key_prefix = false
  }
}
```

```bash
export AWS_ACCESS_KEY_ID=sthings
export AWS_SECRET_ACCESS_KEY=<SECRETVALUE>
```

</details>

<details><summary><b>YAML INLINE OBJECT LIST TEMPLATING TO FILE</b></summary>

```hcl
# main.tf
variable "users" {
  description = "A list of users."

  type = list(object({
    name  = string
    gecos = string
  }))
}

locals {
  all_users = templatefile("${path.module}/users.tmpl", {
    "users" = var.users
  })
}

resource "local_file" "all_users" {
  filename = "users.yaml"
  content  = local.all_users
}
```

```
# users.tmpl
${yamlencode({
  users = [
    for user in users : {
      name = user.name
      gecos = user.gecos
    }
  ]
})}
```

```hcl
# terraform.tfvars
users = [
{
    name  = "ankit"
    gecos = "ankits user"
},
{
    name  = "anuj"
    gecos = "anuj user"
}
]
```

</details>

<details><summary><b>INIT|APPLY|DESTROY</b></summary>

```bash
terraform init
terraform init --upgrade # REDOWNLOAD MODULE / UPGRADE PROVIDERS
terraform verify
terraform plan
terraform apply
terraform destroy
```

</details>

<details><summary><b>CREATE MODULE</b></summary>

```go
# MODULE CALL
# ./module/main.tf
terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

resource "random_string" "module1_random" {
  length           = var.length
  special          = true
  override_special = "/@£$"
}

output "random_string" {
  value = random_string.module1_random
}

variable "length" {
  type        = number
  default     = 3
  description = "Length of the random string "
}
```

### CALLING MODULE W/ VARIABLE

```go
# MODULE CALL
# ./module-call/call.tf
module "random" {
  source = "../module"
  length = 5
}

# USE OUTPUT FROM MODULE OUTPUT
output "random_string" {
  value = "${module.random.random_string}"
}
```

</details>

<details><summary><b>REFRENCE MODULE</b></summary>

```hcl
# LOCAL
module "labda-vm" {
  source                  = "./vsphere-vm"
```

```hcl
# FROM GITHUB
module "labda-vm" {
  source                  = "github.com/stuttgart-things/vsphere-vm" # HTTPS
  source                  = "github.com/stuttgart-things/vsphere-vm.git" # SSH
```

```hcl
# AS ZIP
module "labda-vm" {
  source                  = "https://github.com/stuttgart-things/vsphere-vm/releases/download/vsphere-vm-2.6.1/vsphere-vm.zip"
```

</details>

<details><summary><b>PACKAGE MODULE</b></summary>

```bash
# CHANGE TO MODULE DIR
cd ~/projects/terraform/vsphere-vm/
zip -r vsphere-vm.zip * -j
gh release create vsphere-vm-2.6.1 --notes "released module tesed with provider 2.6.1" vsphere-vm.zip

# RELEASED ARTIFACT
https://github.com/stuttgart-things/vsphere-vm/releases/download/vsphere-vm-2.6.1/vsphere-vm.zip
```

</details>

<details><summary><b>APPLY W/ VARS</b></summary>

```bash
terraform apply \
-var "github_org=stuttgart-things" \
-var "github_repository=stuttgart-things" \
-var "github_token=<TOKEN>" \
-var "target_path=clusters/labda/vsphere/utah" \
-var "kubeconfig_path=/home/sthings/.kube/labda-utah" \
-var "context=utah"
```

</details>

<details><summary><b>PROVIDER</b></summary>

```hcl
terraform {
  required_version = ">= 1.6.5"

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.24.0"
    }

    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.14.0"
    }

    vault = {
      source  = "hashicorp/vault"
      version = ">= 3.21.0"
    }

    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.12.1"
    }

    local = {
      source  = "hashicorp/local"
      version = "2.4.1"
    }
  }
}
```

</details>

<details><summary><b>VARIABLES</b></summary>

```hcl
# JUST DECLARE
variable "createDefaultAdminPolicy" { default = false }

# PROPER DECLARATION
variable "token_max_ttl" {
  type        = number
  default     = 0
  description = "The maximum lifetime for generated tokens in number of seconds. Its current value will be referenced at renewal time."
}

# LIST OBJECT
variable "secret_engines" {
  type = list(object({
    name        = string
    path        = string
    description = string
    data_json   = string
  }))
  default     = []
  description = "A list of secret path objects"
}

# NUMBER
variable "vm_memory" {
  default     = 4096
  type        = number
  description = "amount of memory of the vm"
}

# STRING
variable "vsphere_vm_template" {
  default     = false
  type        = string
  description = "name of vsphere vm template"
}

# LIST
variable "bootstrap" {
  description = "Bootstrap os"
  type        = list(string)
  default     = ["whoami", "hostname"]
}

# LIST WITH NUMBER
variable "sg_ports" {
  type = list(number)
  default = [ 443,80,8080 ]
  description = "list of ingress ports"
}
```

</details>

<details><summary><b>VARIABLE VALIDATION</b></summary>

```hcl
# STRING REGEX
variable "vsphere_vm_name" {
  default     = "terraform-vm"
  type        = string
  description = "name of vsphere virtual machine"

  validation {
    condition     = can(regex("^[a-zA-Z][a-zA-Z\\-\\0-9]{1,32}$", var.vsphere_vm_name))
    error_message = "VM name must start with letter, only contain letters, numbers, dashes, and must be between 1 and 32 characters."
  }

}

# ALLOWED NUMBER(S)
variable "vm_num_cpus" {
  default     = 4
  type        = number
  description = "amount of cpus from the vm"

  validation {
    condition     = contains([2, 4, 6, 8, 10, 12, 16], var.vm_num_cpus)
    error_message = "Valid values for vm_num_cpus are (2, 4, 6, 8, 10, 12, 16)"
  }

}
```

</details>

<details><summary><b>OUTPUTS</b></summary>

```hcl
# LIST
output "ip" {
  value = vsphere_virtual_machine.vm[*].default_ip_address
}

# FOR EACH
output "role_id" {
  description = "Output of role id"
  value = [
    for role in vault_approle_auth_backend_role.approle : role.role_id
  ]
}
```

</details>

<details><summary><b>COMBINE VARIABLE AND STRING</b></summary>

```hcl
// STRING + FOREACH
path = "cluster_name-${each.value["name"]}"

// STRING + VAR
path = "my\.${var.hosted_zone}"

// VAR + STRING + VAR
path =  "${var.cluster_name}-${each.value["name"]}"
```

</details>

<details><summary><b>ENABLE/DISABLE RESOURCE CREATION W/ COUNT</b></summary>

```hcl
variable "csi_enabled" {
 description = "Enable secrets store csi driver"
 type        = bool
 default     = true
}

resource "helm_release" "csi" {
  count            =  var.csi_enabled ? 1 : 0
  name             = "secrets-store-csi-driver"
  namespace        = "vault"
  #....
}
```

</details>

<details><summary><b>CREATE TEMPLATED RESOURCE</b></summary>

## TEMPLATE

```yaml
# ./templates/vault-connection.tpl
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultConnection
metadata:
  name: ${name}
  namespace: ${namespace}
spec:
  address: ${vault_addr}
  skipTLSVerify: true
```

## RESOURCE

```hcl
resource "kubernetes_manifest" "vault_connection" {

  manifest = yamldecode(templatefile(
    "${path.module}/templates/vault-connection.tpl",
    {
      "name"       = "tektoncd"
      "namespace"  = "default"
      "vault_addr" = var.vault_addr
    }
  ))

}
```

</details>

<details><summary><b>LOOP/MAP IN TEMPLATE</b></summary>

## TEMPLATE

```hcl
# ./templates/secret.tpl
apiVersion: v1
kind: Secret
metadata:
  name: ${name}
  namespace: ${namespace}
stringData:
  %{ for key, value in kvs }
  ${key}: ${value}
  %{ endfor ~}
```

## RESOURCE

```hcl
resource "kubernetes_manifest" "k8s_secret" {
  depends_on = [flux_bootstrap_git.flux2]

  for_each = {
    for secret in var.secrets :
    secret.name => secret
  }

  computed_fields = ["stringData"]
  manifest = yamldecode(templatefile(
    "${path.module}/templates/secret.yaml.tpl",
    {
      "name"      = each.value["name"]
      "namespace" = each.value["namespace"]
      "kvs"       = each.value["kvs"]
    }
  ))

}

// KUBECONFIG FILE HANDLING
data "local_file" "kubeconfig" {
  filename = var.kubeconfig_path
}

locals {
  kubeconfig = yamldecode(data.local_file.kubeconfig.content)
}
```

## VARIABLE DECLARATION

```hcl
variable "secrets" {
  type = list(object({
    name      = string
    namespace = string
    kvs       = map(string)
  }))
  default     = []
  description = "A list of secret objects"
}
```

## CALL

```hcl
# main.tf
# ..
secrets = [
  {
    name = "sops-age"
    namespace = "flux-system"
    kvs = {
      "age.agekey" = "AGE-SECRET-KEY"
    }
  },
]
```

</details>

<details><summary><b>LOOP FOR EACH</b></summary>

```hcl
resource "aws_security_group" "demo-security-group" {
name = "demo-security-group"

dynamic "ingress" {
  for_each = var.sg_ports
  content {
    from_port = ingress.value
    protocol = "tcp"
    to_port = ingress.value
    cidr_blocks = ["0.0.0.0/0"]
  }
}
}
```

 </details>

<details><summary><b>USE COUNT W/ FOR EACH</b></summary>

```hcl
resource "kubernetes_manifest" "vault_connection" {

  for_each = {
    for auth in var.k8s_auths :
    auth.name => auth
    if var.vso_enabled[1]
  }

  manifest = yamldecode(templatefile(
    "${path.module}/templates/vault-connection.tpl",
    {
      "name"       = each.value["name"]
      "namespace"  = each.value["namespace"]
      "vault_addr" = var.vault_addr
    }
  ))

  depends_on = [helm_release.vso]
}
```

</details>

<details><summary><b>READ YAML FIELD FROM FILE</b></summary>

```hcl
variable "kubeconfig_path" {
  type        = string
  default = "/home/sthings/.kube/labda-app"
  description = "kubeconfig path"
}

locals {
  kubeconfig= yamldecode(file(var.kubeconfig_path))
}

output "kubeconfig-host" {
  value = local.kubeconfig.clusters[0].cluster.server
}
```

</details>

<details><summary><b>TERRAFORM HELLO WORLD</b></summary>

```bash
mkdir helloworld
```

```bash
cat <<EOT >> helloworld/hello.tf
resource "null_resource" "default" {
  provisioner "local-exec" {
    command = "echo 'Hello World'"
  }
}
EOT
```

```bash
terraform -chdir=helloworld init
terraform -chdir=helloworld apply
```

</details>

## AWS

<details><summary><b>AWS CLI</b></summary>

```bash
sudo apt -y install awscli
aws configure
```

</details>

<details><summary><b>AWS PROVIDER</b></summary>

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

</details>

<details><summary><b>CREATE GENERATED SECRET IN AWS SECRETS MANAGER</b></summary>

```bash
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

</details>

<details><summary><b>OUTPUT/USE SECRET FROM AWS SECRETS MANAGER</b></summary>

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

</details>

## KUBERNETES

<details><summary><b>CREATE INLINE KUBERNETES (YAML) RESOURCES</b></summary>

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

</details>

<details><summary><b>READ K8S SECRET</b></summary>

```hcl
resource "kubernetes_secret" "vault" {
  metadata {
    name      = "vault"
    namespace = "default"
    annotations = {
      "kubernetes.io/service-account.name"      = "vault"
      "kubernetes.io/service-account.namespace" = "default"
    }
  }
  type = "kubernetes.io/service-account-token"
}

data "kubernetes_secret" "vault" {
  metadata {
    name      = "vault"
    namespace = "default"
  }
}

output "ca_crt" {
  value = nonsensitive(data.kubernetes_secret.vault.data["ca.crt"])
}

output "token" {
  value = nonsensitive(data.kubernetes_secret.vault.datoken)
}
```

</details>

<details><summary><b>K8S MANIFEST APP DEPLOYMENT</b></summary>

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

</details>

<details><summary><b>HELM CHART DEPLOYMENT</b></summary>

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

</details>

<details><summary><b>RENDERING OF MANIFEST</b></summary>

```hcl
# provider.tf
// ..
    kubectl = {
      source = "gavinbunney/kubectl"
      version = ">=1.14.0"
    }
// ..
```

```hcl
# certificate_manifest.yaml.tpl
%{ for INGRESS_HOSTNAME in split(",", INGRESS_HOSTNAME) }
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name:  ${NAME}-${INGRESS_HOSTNAME}
  namespace: ${NAMESPACE}
spec:
  commonName: ${INGRESS_HOSTNAME}.${INGRESS_DOMAIN}
  dnsNames:
    - ${INGRESS_HOSTNAME}.${INGRESS_DOMAIN}
  issuerRef:
    kind: ClusterIssuer
    name: ${CLUSTER_ISSUER}
  secretName: ${INGRESS_HOSTNAME}-ingress-tls
  %{ endfor }
```

```hcl
# cert.tf
data "kubectl_path_documents" "certs" {
    pattern = "${path.module}/templates/cert*.yaml.tpl"
    vars = {
        INGRESS_HOSTNAME = format("%s,%s",var.ingress_hostname_api,var.ingress_hostname_console)
        INGRESS_DOMAIN = var.ingress_domain
        CLUSTER_ISSUER = var.cluster_issuer
        NAMESPACE = var.namespace
        NAME = var.helm_release_name
    }
}

resource "kubectl_manifest" "cert_manifest" {
    count = var.create_cert == true ? length(data.kubectl_path_documents.certs.documents) : 0
    yaml_body = element(data.kubectl_path_documents.certs.documents, count.index)
}
```

</details>

<details><summary><b>REMOTE STATE IN GCP</b></summary>

```hcl
resource "random_id" "bucket_prefix" {
  byte_length = 8
}

terraform {
 backend "gcs" {
   credentials = "gcp-credentials.json"
   bucket  = "sthings-bucket-f0b3f1ee5"
   prefix  = "terraform/state"
 }
}
```

</details>
