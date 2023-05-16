# AWS

## AWS CLI 
The AWS Command Line Interface (AWS CLI) is a unified tool to manage your AWS services. With just one tool to download and configure, you can control multiple AWS services from the command line and automate them through scripts.

### INSTALLATION
#### Requirements
You must be able to extract or "unzip" the downloaded package. If your operating system doesn't have the built-in unzip command, use an equivalent.

#### Install the AWS CLI
To [install the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) you must run the following commands.

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

Confirm the installation with the following command.
```
aws --version
```


### BASIC COMMANDS

| COMMAND | DESCRIPTION | EXAMPLE CALL
|--|--|--|
| get-caller-identity  | Returns details about the IAM user | aws sts get-caller-identity --output text
| describe-instances| Display detailed information about all instances that are managed by you| aws ec2 describe-instances --filter Name=tag:Name,Values=dev-server
| start-instances| Starts the specified instance | aws ec2 start-instances --instance-ids i-5c8282ed i-44a44ac3|
| stop-instances| Stops the specified instance| aws ec2 stop-instances --instance-ids i-5c8282ed|
| terminate-instances| Terminates the specified instance|aws ec2 terminate-instances --instance-ids i-44a44ac3|
| create-tags| Adds a new tag to the specified instance|aws ec2 create-tags --resources i-dddddd70 --tags Key=Department,Value=Finance|
| attach-volume| Attaches a specified volume to a particular instance| aws ec2 attach-volume  --volume-id vol-1d5cc8cc --instance-id i-dddddd70 --device /dev/sdh|
| run-instances| Creates a new AWS EC2 instance| aws ec2 run-instances --image-id ami-22111148 --count 1 --instance-type t1.micro --key-name stage-key --security-groups my-aws-security-group|
| reboot-instances| Reboots the given instance| aws ec2 reboot-instances --instance-ids i-dddddd70|
| modify-instance-attribute| Changes an attribute of existing instance| aws ec2 modify-instance-attribute --instance-id i-44a44ac3 --instance-type "{\"Value\": \"m1.small\"}"|
| create-image| Creates new image| aws ec2 create-image --instance-id i-44a44ac3 --name "Dev AMI" --description "AMI for development server"|
| get-console-output| Displays whatever was sent to the system console for your particular instance| aws ec2 get-console-output --instance-id i-44a44ac3|
| monitor-instances| Enables advanced cloudwatch monitoring| aws ec2 monitor-instances --instance-ids i-44a44ac3|
| describe-key-pairs| Displays all keypairs created so far| aws ec2 describe-key-pairs|
| describe-subnets| Describes one or more of your subnets| aws ec2 describe-subnets|
| describe-vpcs| Describes one or more of your VPCs| aws ec2 describe-vpcs|

Reference Links:
- [15 Essential Amazon AWS EC2 CLI Command](https://www.thegeekstuff.com/2016/04/aws-ec2-cli-examples/)
- [describe-VPCs](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-vpcs.html)
- [describe-subnets](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-subnets.html)
