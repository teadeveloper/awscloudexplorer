""" Access to EC2

This file contains the classes and methods to get information about ec2 instances.

"""

import boto3
import yaml
import pandas as pd


class AwsEc2:

    def __init__(self, aws_end_point, aws_region):
        """
        Variables to be consume by the functions

        :param aws_end_point: AWS API endpoint.
        :param aws_region: AWS region

        """

        self.aws_end_point = aws_end_point
        self.ec2_filter = [{'Name': 'instance-state-name',
                            'Values': ['running', 'stopped', 'terminated']}]
        self.ebs_filters = []
        self.aws_region = aws_region
        self.ec2resource = boto3.resource(
            'ec2', endpoint_url=self.aws_end_point, region_name=self.aws_region)
        self.ec2client = boto3.client(
            'ec2', endpoint_url=self.aws_end_point, region_name=self.aws_region)

    def get_instances(self):
        """
        Get a list of all instances in AWS EC2 service

        :return: List
        """

        ec2_instances = []

        for instance in self.ec2resource.instances.filter(Filters=self.ec2_filter):

            ec2_instance = []

            if instance.tags is not None:
                for tag in instance.tags:
                    if tag['Key'] == 'Name':
                        ec2_instance.append(tag['Value'])
            else:
                ec2_instance.append(None)

            ec2_instance.append(instance.id)
            ec2_instance.append(instance.instance_type, )
            ec2_instance.append(instance.public_ip_address)
            ec2_instance.append(instance.private_ip_address)
            ec2_instance.append(instance.image.id)
            ec2_instance.append(instance.state["Name"])
            ec2_instances.append(ec2_instance)

        return ec2_instances

    def get_ebs(self):
        """
        Get a list of all EBS volumes in AWS account

        :return: List of lists
        """
        response_ebs_list = self.ec2client.describe_volumes(Filters=self.ebs_filters)["Volumes"]
        ebs_volumes = []

        for ebs in response_ebs_list:
            ebs_data = [ebs["VolumeId"], ebs["Size"], ebs["VolumeType"], ebs["Iops"], ebs["Encrypted"]]
            ebs_volumes.append((ebs_data))
        return ebs_volumes

    def get_ebs_yml_properties(self, ebs_id):
        """
        Get the EBS configuration.

        :param ebs_id: AWS EBS volume id
        :return: Configuration in YAML export_format.
        """
        ebs_data = self.ec2client.describe_volumes(VolumeIds=[ebs_id])

        yml_data_result = yaml.dump(ebs_data)
        return yml_data_result.splitlines()

    def get_ec2_yml_properties(self, ec2_id):
        """
        Get the EC2 configuration.

        :param ec2_id: AWS ec2 instance id
        :return: Configuration in YAML export_format.
        """

        ec2_data = self.ec2client.describe_instances(
            Filters=[{'Name': 'instance-id', 'Values': [ec2_id]}])
        yml_data_result = yaml.safe_dump(ec2_data["Reservations"])
        return yml_data_result.splitlines()

    def get_ec2_properties(self, ec2_id):
        """
        Get EC2 configuration about a specific instance.

        :param ec2_id: ID of the AWS EC2 instance.
        :return: AWS JSON export_format.
        """

        ec2_data = self.ec2client.describe_instances(
            Filters=[{'Name': 'instance-id', 'Values': [ec2_id]}])
        return ec2_data['Reservations']

    def export_to(self, export_format, file_name):
        """
        Convert all the instances in a AWS  to a excel, csv, readme, or html

         Parameters
         ----------

         param export_format: html,string,csv, excel or markdown

        :param
        :file_name: file name to save the results.

        :returns
        N/A
        """
        with open("forms/aws_form.yml") as f:
            configuration = yaml.safe_load(f, Loader=yaml.FullLoader)

        ec2_keys = configuration["ec2_export_selected_keys"]

        aws_response = self.ec2client.describe_instances()

        ec2_instances = []

        for instances_data in aws_response['Reservations']:

            ec2_properties = {}

            for instance in instances_data['Instances']:

                for value in ec2_keys:

                    try:
                        if type(instance[value]) == dict or type(instance[value]) == list:
                            data = yaml.dump(instance[value])
                            ec2_properties[value] = data

                        else:
                            ec2_properties[value] = str(instance[value])
                    except:
                        pass

                ec2_instances.append(ec2_properties)
                ec2_properties = {}

        self.data_to_file(ec2_instances, export_format, file_name)

    def data_to_file(self, data, export_format, file_name):

        """
        Convert de data to a pandas data frame and save it to a file.

        :param data: Array or dictionary
        :param export_format: format to export: HTML,markdown, string, csv
        :param file_name: the file name to save the data
        :return:
        """

        df_ec2_instances = pd.DataFrame(data)

        if export_format == 0:
            excel_writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            df_ec2_instances.to_excel(
                excel_writer, sheet_name='EC2 instances', index=False)
            excel_writer.save()
        elif export_format == 1:
            df_ec2_instances.to_csv(file_name)
        elif export_format == 2:
            df_ec2_instances.to_string(file_name)
        elif export_format == 3:
            df_ec2_instances.to_markdown(file_name)
        elif export_format == 4:
            df_ec2_instances.to_html(file_name)

    def all_keys_export_to(self, export_format, file_name):
        """
       Convert and save to a file all EC2 instances to a Excel, CSV, Markdown, String or HTML

       :param export_format: the name of the export_format, it could be: excel, html, markdown, string or csv
       :param file_name:
       :return:
       """

        aws_response = self.ec2client.describe_instances()

        ec2_instances = []

        for instances in aws_response['Reservations']:

            ec2_properties = {}

            for instance in instances['Instances']:

                ec2_keys = (instance.keys())

                for value in ec2_keys:

                    try:
                        if type(instance[value]) == dict or type(instance[value]) == list:
                            data = yaml.dump(instance[value])
                            ec2_properties[value] = data
                        else:
                            ec2_properties[value] = str(instance[value])
                    except:
                        pass

                ec2_instances.append(ec2_properties)
                ec2_properties = {}

        self.data_to_file(ec2_instances, export_format, file_name)

    def export_instance_yaml(self, ec2_id):
        """
        Export to a file the EC2 instance configuration in YML export_format.

        :param ec2_id: AWS EC2 id instance.
        :return:
        """
        ec2_data = self.ec2client.describe_instances(
            Filters=[{'Name': 'instance-id', 'Values': [ec2_id]}])
        file = open(ec2_id + ".yml", "w")
        yaml.safe_dump(ec2_data["Reservations"], file)
        file.close()

    def export_ebs_yml(self, ebs_id):
        """
        Get the EBS configuration.

        :param ebs_id: AWS EBS volume id
        """
        ebs_data = self.ec2client.describe_volumes(VolumeIds=[ebs_id])
        file = open(ebs_id + ".yml", "w")
        yaml.safe_dump(ebs_data, file)
        file.close()

    def export_ebs_to(self, export_format, file_name):

        """Convert all EBS  in a AWS  to a excel, csv, readme, or html

                * export_format: html,string,csv, excel or markdown
                * file_name: file name to save the results.

                Returns
                -------
                N/A

                """

        aws_ebs_response = self.get_ebs()

        ebs_volumes = []

        for ebs in aws_ebs_response:
            ebs_volumes.append(ebs)

        df_ebs = pd.DataFrame(ebs_volumes)

        if export_format == 0:
            excel_writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            df_ebs.to_excel(
                excel_writer, sheet_name='VPCs', index=False)
            excel_writer.save()
        elif export_format == 1:
            df_ebs.to_csv(file_name)
        elif export_format == 2:
            df_ebs.to_string(file_name)
        elif export_format == 3:
            df_ebs.to_markdown(file_name)
        elif export_format == 4:
            df_ebs.to_html(file_name)
