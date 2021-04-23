import boto3
import yaml
import pandas as pd

class AwsLambda:

    def __init__(self, aws_end_point, aws_region):

        self.aws_end_point = aws_end_point
        self.aws_region = aws_region
        self.lambda_client = boto3.client(
            'lambda', endpoint_url=self.aws_end_point, region_name=self.aws_region)

    def get_lambdas(self):
        """Gets lambdas to be showed in the main form grid.

         Parameters
         ----------
         No needed.

         Returns
         -------
         List of dictionaries, every dictionary has the properties of an account
        """

        functions = []

        function_results = self.lambda_client.list_functions()["Functions"]

        for function in function_results:
            functions_data = [function["FunctionName"], function["FunctionArn"],function["Runtime"]]
            functions.append(functions_data)

        #vpcs_list.insert(0, ["VPC ID", "CDIR BLOCK", "STATE", "DHCP OPTIONS", "TENANCY"])

        return functions
