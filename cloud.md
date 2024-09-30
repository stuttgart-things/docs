# stuttgart-things/docs/cloud

## AZURE

### GET AKS KUBECONFIG

```bash
az login --use-device-code
RG=homerun
CLUSTER_NAME=homerun
az aks get-credentials --resource-group ${RG} --name ${CLUSTER_NAME}
```


## AWS

### CLI-SNIPPETS

<details><summary><b>AWS S3</b></summary>

```bash
# LIST BUCKETS
aws s3 ls

# CREATE BUCKET
aws s3 mb s3://ankit-devops

# LIST BUCKET CONTENT
aws s3 ls s3://terraform-20240319071635887700000001

# COPY FILE TO BUCKET
aws s3 cp cic-k8s-role-service-account.yml s3://terraform-20240319071635887700000001/test.yml

# LIST VPCS
aws ec2 --query 'Vpcs[*].{name:Tags[?Key==`Name`].Value|[0], VpcId:VpcId, Cidr:CidrBlockAssociationSet[*].CidrBlock}' describe-vpcs
```

</details>

<details><summary><b>INSTALL AWS CLI</b></summary>

The AWS Command Line Interface (AWS CLI) is a unified tool to manage your AWS services. With just one tool to download and configure, you can control multiple AWS services from the command line and automate them through scripts.

### INSTALLATION

#### Requirements

You must be able to extract or "unzip" the downloaded package. If your operating system doesn't have the built-in unzip command, use an equivalent.

#### Install the AWS CLI

To [install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) you must run the following commands.

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Confirm the installation with the following command.

```bash
aws --version
```

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: basic
type: Opaque
stringData:
  .gitconfig: |
    [url "https://<USERNAME>:<TOKEN>@github.<ENT>.com"]
        insteadOf = https://github.<ENT>.com
    [user]
        name = Patrick Hermann
        email = patrick.hermann@sva.de
  .git-credentials: |
    https://<USERNAME>:<TOKEN>@github.<ENT>.com
```

</details>

<details><summary><b>BASIC CLI COMMANDS</b></summary>

| COMMAND                   | DESCRIPTION                                                                   | EXAMPLE CALL                                                                                                                                  |
| ------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| get-caller-identity       | Returns details about the IAM user                                            | aws sts get-caller-identity --output text                                                                                                     |
| describe-instances        | Display detailed information about all instances that are managed by you      | aws ec2 describe-instances --filter Name=tag:Name,Values=dev-server                                                                           |
| start-instances           | Starts the specified instance                                                 | aws ec2 start-instances --instance-ids i-5c8282ed i-44a44ac3                                                                                  |
| stop-instances            | Stops the specified instance                                                  | aws ec2 stop-instances --instance-ids i-5c8282ed                                                                                              |
| terminate-instances       | Terminates the specified instance                                             | aws ec2 terminate-instances --instance-ids i-44a44ac3                                                                                         |
| create-tags               | Adds a new tag to the specified instance                                      | aws ec2 create-tags --resources i-dddddd70 --tags Key=Department,Value=Finance                                                                |
| attach-volume             | Attaches a specified volume to a particular instance                          | aws ec2 attach-volume --volume-id vol-1d5cc8cc --instance-id i-dddddd70 --device /dev/sdh                                                     |
| run-instances             | Creates a new AWS EC2 instance                                                | aws ec2 run-instances --image-id ami-22111148 --count 1 --instance-type t1.micro --key-name stage-key --security-groups my-aws-security-group |
| reboot-instances          | Reboots the given instance                                                    | aws ec2 reboot-instances --instance-ids i-dddddd70                                                                                            |
| modify-instance-attribute | Changes an attribute of existing instance                                     | aws ec2 modify-instance-attribute --instance-id i-44a44ac3 --instance-type "{\"Value\": \"m1.small\"}"                                        |
| create-image              | Creates new image                                                             | aws ec2 create-image --instance-id i-44a44ac3 --name "Dev AMI" --description "AMI for development server"                                     |
| get-console-output        | Displays whatever was sent to the system console for your particular instance | aws ec2 get-console-output --instance-id i-44a44ac3                                                                                           |
| monitor-instances         | Enables advanced cloudwatch monitoring                                        | aws ec2 monitor-instances --instance-ids i-44a44ac3                                                                                           |
| describe-key-pairs        | Displays all keypairs created so far                                          | aws ec2 describe-key-pairs                                                                                                                    |
| describe-subnets          | Describes one or more of your subnets                                         | aws ec2 describe-subnets                                                                                                                      |
| describe-vpcs             | Describes one or more of your VPCs                                            | aws ec2 describe-vpcs                                                                                                                         |

Reference Links:

- [15 Essential Amazon AWS EC2 CLI Command](https://www.thegeekstuff.com/2016/04/aws-ec2-cli-examples/)
- [describe-VPCs](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpcs.html)
- [describe-subnets](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-subnets.html)

</details>

## GCR

<details><summary><b>WORK W/ GCR REGISTRY</b></summary>

## LOGIN W/HELM AT GCR

```bash
cat gcr.json | helm registry login -u _json_key --password-stdin \eu.gcr.io
```

## PUSH OCI HELM CHART TO GCR

```bash
helm package ./sthings-helm-toolkit
helm push sthings-helm-toolkit-2.4.7.tgz oci://eu.gcr.io/stuttgart-things/sthings-helm-toolkit
```

## LOGIN W/NERDCTL AT GCR

```bash
cat gcr.json | nerdctl login -u _json_key --password-stdin \eu.gcr.io
```

## ADD GCR TO HARBOR (REGISTRY)

Endpoint: https://eu.gcr.io
Access ID: \_json_key

<details><summary><b>Access Secret</b></summary>

```yaml
{
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": "",
}
```

</details>

</details>
