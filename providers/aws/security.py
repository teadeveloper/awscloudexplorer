""" Access to Security

This file contains the classes and methods to get information about Security.

"""

import boto3
import yaml
import pandas as pd


class AwsSecurity:

    def __init__(self, aws_end_point, aws_region):
        """
        Variables to be consume by the functions

        :param aws_end_point: AWS API endpoint.
        :param aws_region: AWS region

        """
        self.security_groups_filters = []
        self.aws_end_point = aws_end_point
        self.aws_region = aws_region
        self.ec2client = boto3.client(
            'ec2', endpoint_url=self.aws_end_point, region_name=self.aws_region)

    def get_security_groups(self):
        """
        Get all Security Groups
        :return: a list of lists with every SecurityGroup config.
        """
        security_group_list = []

        security_groups = self.ec2client.describe_security_groups(
            Filters=self.security_groups_filters)["SecurityGroups"]

        for security_group in security_groups:

            security_group_data = [security_group["GroupId"],
                                   security_group["Description"], security_group["OwnerId"]]
            security_group_list.append(security_group_data)

        return security_group_list

    def get_security_groups_yml_properties(self, security_group_id):
        """ Get the configuration of a specific Security Group

        Parameters
        ----------
        security_group_id: the ID of the security group

        Returns
        -------
        JSON results from AWS

        """
        security_group_data = self.ec2client.describe_security_groups(
            GroupIds=[security_group_id])
        results_security_group_data = yaml.safe_dump(
            security_group_data).splitlines()
        return results_security_group_data

    def export_security_group_yaml(self, security_group_id):
        """
        Save the Security Group information to a file

        :param bucket_id: Name of the bucket
        :return:
        """
        security_group_data = self.ec2client.describe_security_groups(
            GroupIds=[security_group_id])
        file = open(security_group_id + ".yml", "w")
        yml_data_result = yaml.safe_dump(security_group_data, file)
        file.close()

    def export_to(self, export_format, file_name):
        """Convert all Security Groups in a AWS  to a excel, csv, readme, or html

         * export_format: html,string,csv, excel or markdown
         * file_name: file name to save the results.

         Returns
         -------
         N/A

         """

        aws_response = self.get_security_groups()

        security_groups = []

        for security_group in aws_response:
            security_groups.append(security_group)

        df_security_groups = pd.DataFrame(security_groups)

        if export_format == 0:
            excel_writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            df_security_groups.to_excel(
                excel_writer, sheet_name='S3 Buckets', index=False)
            excel_writer.save()
        elif export_format == 1:
            df_security_groups.to_csv(file_name)
        elif export_format == 2:
            df_security_groups.to_string(file_name)
        elif export_format == 3:
            df_security_groups.to_markdown(file_name)
        elif export_format == 4:
            df_security_groups.to_html(file_name)
