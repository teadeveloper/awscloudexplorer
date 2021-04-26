from providers.aws.ec2 import AwsEc2
from providers.aws.s3 import AwsS3
from providers.aws.network import AwsNetwork
from providers.aws.security import AwsSecurity
from providers.aws.efs import AwsEfs
from providers.aws.iam import AwsIam
from providers.aws.lambdafunc import AwsLambda

import boto3
import json
import yaml

aws_region = None
aws_end_end_point = None
# "http://localhost:4566"

instancias = AwsEc2(aws_end_end_point, aws_region)
s3 = AwsS3(aws_end_end_point, aws_region)
ec2 = AwsEc2(aws_end_end_point, aws_region)
network = AwsNetwork(aws_end_end_point, aws_region)
security = AwsSecurity(aws_end_end_point, aws_region)
efs = AwsEfs(aws_end_end_point, aws_region)
accounts = AwsIam(aws_end_end_point, aws_region)
lamdafunc = AwsLambda(aws_end_end_point, aws_region)

#results = s3.get_method_results("jky876587", "describe_instance_attribute")
#results = ec2.get_method_results("i-0cf04fd9d3a5836d3", "describe_instance_status")

#ec2.ec2_export_to("string", "prueba.txt")

results = lamdafunc.get_lambdas()
print(results)



@click.option("--export_ec2", is_flag=True, help="Export EC2 instances with keys in file forms/aws/form.yml")
@click.option("--export_ec2_all_keys", is_flag=True, help="Export EC2 instances with all keys")
@click.option("--VPC", is_flag=True, help="Export all VPCs")
@click.option("--Subnet", is_flag=True, help="Export all Subnets")
@click.option("--ACL", is_flag=True, help="Export Networks ACLs")
@click.option("--SecurityGroup", is_flag=True, help="Export all security groups")
@click.option("--NetworkInterface", is_flag=True, help="Export all security groups")
@click.option("--Bucket", is_flag=True, help="Export all S3 Buckets")
@click.option("--EBS", is_flag=True, help="Export all block storages")
@click.option("--EFS", is_flag=True, help="Export all block storages")
@click.option("--Users", is_flag=True, help="Export all users")
@click.option("--Groups", is_flag=True, help="Export all groups")
@click.option("--Role", is_flag=True, help="Export all roles")
@click.option("--Policy", is_flag=True, help="Export all policies")
@click.option("--LambdaFunction", is_flag=True, help="Export all lambda functions")
@click.option("--filename", help="File name and extension")
@click.option("--format", help="Format file to export, values: 0=EXCEL,1=CSV,2=STRING,3=MARKDOWN,4=HTML ")
@click.option("--examples",  is_flag=True)