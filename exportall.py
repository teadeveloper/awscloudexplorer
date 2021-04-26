import click
from providers.aws.ec2 import AwsEc2
from providers.aws.s3 import AwsS3
from providers.aws.network import AwsNetwork
from providers.aws.security import AwsSecurity
from providers.aws.efs import AwsEfs
from providers.aws.iam import AwsIam
from providers.aws.lambdafunc import AwsLambda

import yaml

with open("forms/aws_form.yml") as f:
    configuration = yaml.safe_load(f)

aws_region = configuration["aws_region"]
aws_end_end_point = configuration["aws_end_end_point"]


ec2 = AwsEc2(aws_end_end_point, aws_region)
S3 = AwsS3(aws_end_end_point, aws_region)
Network = AwsNetwork(aws_end_end_point, aws_region)
Security = AwsSecurity(aws_end_end_point, aws_region)
EFS = AwsEfs(aws_end_end_point, aws_region)
IAM = AwsIam(aws_end_end_point, aws_region)
LAMBDA = AwsLambda(aws_end_end_point, aws_region)

@click.command()
@click.option("--ec2ins", is_flag=True, help="Export EC2 instances with keys in file forms/aws/form.yml")
@click.option("--ec2_all_keys", is_flag=True, help="Export EC2 instances with all keys")
@click.option("--vpc", is_flag=True, help="Export all VPCs")
@click.option("--subnet", is_flag=True, help="Export all Subnets")
@click.option("--acl", is_flag=True, help="Export Networks ACLs")
@click.option("--securitygroup", is_flag=True, help="Export all security groups")
@click.option("--networkinterface", is_flag=True, help="Export all security groups")
@click.option("--bucket", is_flag=True, help="Export all S3 Buckets")
@click.option("--ebs", is_flag=True, help="Export all block storages")
@click.option("--efs", is_flag=True, help="Export all block storages")
@click.option("--user", is_flag=True, help="Export all users")
@click.option("--group", is_flag=True, help="Export all groups")
@click.option("--role", is_flag=True, help="Export all roles")
@click.option("--policy", is_flag=True, help="Export all policies")
@click.option("--filename", help="File name and extension")
@click.option("--format", help="Format file to export, values: 0=EXCEL,1=CSV,2=STRING,3=MARKDOWN,4=HTML ")
@click.option("--examples", is_flag=True)
def cli(
        ec2ins,
        ec2_all_keys,
        filename,
        format,
        vpc,
        acl,
        securitygroup,
        networkinterface,
        bucket,
        ebs,
        efs,
        user,
        group,
        role,
        policy,
        subnet,
        examples
):
    if ec2ins:
        print("Exporting EC2 Instances to " + filename + " in format " + format)
        ec2.export_to(int(format), filename)

    if ec2_all_keys:
        print("Exporting EC2 Instances with all keys to " + filename + " in format " + format)
        ec2.all_keys_export_to(int(format), filename)

    if vpc:
        print("Exporting VPCs to " + filename + " in format " + format)
        Network.export_vpc_to(int(format), filename)

    if subnet:
        print("Exporting Subnets to " + filename + " in format " + format)
        Network.export_subnet_to(int(format), filename)

    if acl:
        print("Exporting ACLs to " + filename + " in format " + format)
        Network.export_acl_to(int(format), filename)

    if securitygroup:
        print("Exporting security groups to " + filename + " in format " + format)
        Security.export_to(int(format), filename)

    if networkinterface:
        print("Exporting network interfaces to " + filename + " in format " + format)
        Network.export_network_interfaces_to(int(format), filename)

    if bucket:
        print("Exporting S3 buckets to " + filename + " in format " + format)
        S3.export_to(int(format), filename)

    if efs:
        print("Exporting EFS to " + filename + " in format " + format)
        EFS.export_to(int(format), filename)

    if ebs:
        print("Exporting EBS to " + filename + " in format " + format)
        ec2.export_ebs_to(int(format), filename)

    if user:
        print("Exporting users to " + filename + " in format " + format)
        IAM.users_export_to(int(format), filename)

    if group:
        print("Exporting groups to " + filename + " in format " + format)
        IAM.groups_export_to(int(format), filename)

    if role:
        print("Exporting roles to " + filename + " in format " + format)
        IAM.roles_export_to(int(format), filename)

    if policy:
        print("Exporting policies to " + filename + " in format " + format)
        IAM.policies_export_to(int(format), filename)

    if examples:
        print("""

       1) To export all instances to excel:

       python exportall.py --ec2ins --filename="ec2instances.xls" --format=0
       
       2) To export all users to CSV:

       python exportall.py --user --filename="users.csv" --format=1
       
       3) To export all policies to HTML:

       python exportall.py --policy --filename="policies.csv" --format=4

       """)


if __name__ == "__main__":
    cli()

