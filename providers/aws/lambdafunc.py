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
            functions_data = [function["FunctionName"], function["FunctionArn"],
                              function["Runtime"], function["CodeSize"], function["Description"]]
            functions.append(functions_data)

        functions.insert(0, ["FUNCTION NAME", "FUNCTION ARN",
                             "RUNTIME", "CODE SIZE", "DESCRIPTION"])

        #vpcs_list.insert(0, ["VPC ID", "CDIR BLOCK", "STATE", "DHCP OPTIONS", "TENANCY"])

        return functions

    def get_function_yml_properties(self, functioname):
        """
        :param functioname: The name of the Lambda function, version, or alias.
        :return: a yml with the user configuration
        """
        data = self.lambda_client.get_function(FunctionName=functioname)
        results = yaml.dump(data).splitlines()
        return results

    def export_funcion_yaml(self, functioname):
        """
        Save the function information to a file

        :param functioname: The name of the Lambda function, version, or alias.
        :return: a yml with the user configuration
        """
        data = self.lambda_client.get_function(FunctionName=functioname)
        results = yaml.dump(data).splitlines()
        file = open(functioname + ".yml", "w")
        yaml.safe_dump(data, file)
        file.close()

    def funcion_yaml_export_to(self, export_format, file_name):
        """Convert all lambda funcions in a AWS  to a excel, csv, readme, or html

         * export_format: html,string,csv, excel or markdown
         * file_name: file name to save the results.

         Returns
         -------
         N/A

         """

        aws_response = self.get_lambdas()

        functions = []

        for function in aws_response:
            functions.append(function)

        df = pd.DataFrame(functions)

        if export_format == 0:
            excel_writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            df.to_excel(
                excel_writer, sheet_name='VPCs', index=False)
            excel_writer.save()
        elif export_format == 1:
            df.to_csv(file_name)
        elif export_format == 2:
            df.to_string(file_name)
        elif export_format == 3:
            df.to_markdown(file_name)
        elif export_format == 4:
            df.to_html(file_name)
