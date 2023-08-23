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
data "aws_secretsmanager_secret" "ms_secrets" {
    arn = "arn:aws:secretsmanager:eu-central-1:367557680358:secret:AmazonMSK_example-vfUxyF"
}

data "aws_secretsmanager_secret_version" "secret_version" {
  secret_id = data.aws_secretsmanager_secret.ms_secrets.id
}

# 
output "secret_string" {
  value = jsondecode(nonsensitive(data.aws_secretsmanager_secret_version.secret_version.secret_string))["username"]
}
```

</details close>


