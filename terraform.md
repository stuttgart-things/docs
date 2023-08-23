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

