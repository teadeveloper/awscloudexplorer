from providers.aws.ec2 import AwsEc2
from providers.aws.s3 import AwsS3
from providers.aws.network import AwsNetwork
from providers.aws.security import AwsSecurity
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


#results = s3.get_method_results("jky876587", "describe_instance_attribute")
#results = ec2.get_method_results("i-0cf04fd9d3a5836d3", "describe_instance_status")

#ec2.ec2_export_to("string", "prueba.txt")
results = network.get_network_interfaces()
print(results)

#print (yaml.dump(results))
