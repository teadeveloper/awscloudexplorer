""" Access to VPCs

This file contains the classes and methods to get information about VPCs.

"""

import boto3
import yaml
import pandas as pd


class AwsNetwork:

    def __init__(self, aws_end_point, aws_region):
        """
        Variables to be consume by the functions

        :param aws_end_point: AWS API endpoint.
        :param aws_region: AWS region

        """

        self.vpc_filters = []
        self.subnets_filters = []
        self.acl_network_filters = []
        self.network_interfaces_filters = []

        self.aws_end_point = aws_end_point
        self.aws_region = aws_region
        self.ec2client = boto3.client(
            'ec2', endpoint_url=self.aws_end_point, region_name=self.aws_region)

    def get_vpcs(self):
        """
        Get all VPCs
        :return: a list of lists with every VPC config.
        """
        vpcs_list = []
        vpcs = self.ec2client.describe_vpcs(Filters=self.vpc_filters)["Vpcs"]

        for vpc in vpcs:
            vpc_data = [vpc["VpcId"], vpc["CidrBlock"], vpc["State"],
                        vpc["DhcpOptionsId"], vpc["InstanceTenancy"]]
            vpcs_list.append(vpc_data)

        vpcs_list.insert(0, ["VPC ID", "CDIR BLOCK",
                             "STATE", "DHCP OPTIONS", "TENANCY"])
        return vpcs_list

    def get_subnets(self):
        """
        Get all subnets
        :return: a list of lists with every subnet config.
        """

        subnets_list = []
        subnets = self.ec2client.describe_subnets(
            Filters=self.subnets_filters)["Subnets"]

        for subnet in subnets:
            subnet_data = [subnet["SubnetId"], subnet["CidrBlock"], subnet["AvailableIpAddressCount"], subnet["VpcId"],
                           subnet["AvailabilityZone"], subnet["AvailabilityZoneId"]]
            subnets_list.append(subnet_data)

        subnets_list.insert(0, ["SUBNET ID", "CDIR BLOCK", "AVAILABLE IP",
                                "VPC ID", "AVAILABLE ZONE", "AVAILABLE ZONE ID"])
        return subnets_list

    def get_acl_network(self):
        """
        Get all VPCs
        :return: a list of lists with every VPC config.
        """
        acl_network_list = []
        acls = self.ec2client.describe_network_acls(
            Filters=self.acl_network_filters)["NetworkAcls"]

        for acl in acls:
            acl_data = [acl["NetworkAclId"], acl["VpcId"]]
            acl_network_list.append(acl_data)

        acl_network_list.insert(0, ["NETWORK ACL ID", "VPC ID"])
        return acl_network_list

    def get_network_interfaces(self):
        """
        Get all Network interfaces
        :return: a list of lists with every Network interface config.
        """
        network_interfaces_list = []
        response_network_interfaces_list = self.ec2client.describe_network_interfaces(
            Filters=self.network_interfaces_filters)["NetworkInterfaces"]

        for interface in response_network_interfaces_list:
            interface_data = [interface["NetworkInterfaceId"], interface["Description"],
                              interface["AvailabilityZone"], interface["MacAddress"], interface["OwnerId"]]
            network_interfaces_list.append(interface_data)

        network_interfaces_list.insert(
            0, ["INTERFACE ID", "DESCRIPTION", "AVAILABILITY ZONE", "MAC ADDRESS", "OWNERID"])
        return network_interfaces_list

    def get_subnet_yml_properties(self, subnet_id):
        """

        :param subnet_id: The ID of the subnet
        :return: a yml with the VPC configuration
        """

        subnet_data = self.ec2client.describe_subnets(SubnetIds=[subnet_id])
        results_subnet = yaml.dump(subnet_data).splitlines()
        return results_subnet

    def get_vpc_yml_properties(self, vpc_id):
        """

        :param vpc_id: The ID of the VPC.
        :return: a yml with the VPC configuration
        """

        vpc_data = self.ec2client.describe_vpcs(VpcIds=[vpc_id])
        results_vpc = yaml.dump((vpc_data)).splitlines()
        return results_vpc

    def get_acl_yml_network_properties(self, acl_id):
        """
        :param acl_id: The ID of the ACL.
        :return: a yml with the ACL configuration
        """
        acl_id_data = self.ec2client.describe_network_acls(
            NetworkAclIds=[acl_id])
        results_acl = yaml.dump(acl_id_data).splitlines()
        return results_acl

    def get_network_interface_properties(self, interface_id):
        """

        :param interface_id: The ID of the Network interface
        :return: a yml with the Network interface configuration
        """
        interface_data = self.ec2client.describe_network_interfaces(
            NetworkInterfaceIds=[interface_id])
        results_interface = yaml.dump(interface_data).splitlines()
        return results_interface

    def export_vpc_yaml(self, vpc_id):
        """
        Save the vpc information to a file

        :param vpc_id: Name of the bucket
        :return:
        """
        vpc_data = self.ec2client.describe_vpcs(VpcIds=[vpc_id])
        file = open(vpc_id + ".yml", "w")
        yaml.safe_dump(vpc_data, file)
        file.close()

    def export_network_interface_yaml(self, interface_id):
        """
        Save the Network interface data information to a file

        :param vpc_id: id of the Network interface
        :return:
        """
        interface_data = self.ec2client.describe_network_interfaces(
            NetworkInterfaceIds=[interface_id])
        file = open(interface_id + ".yml", "w")
        yaml.safe_dump(interface_data, file)
        file.close()

    def export_subnets_yaml(self, subnet_id):
        """
        Save the Subnets information to a file

        :param subnet_id: Name of the bucket
        :return:
        """
        subnet_data = self.ec2client.describe_subnets(SubnetIds=[subnet_id])
        results_subnet = yaml.dump(subnet_data).splitlines()
        file = open(subnet_id + ".yml", "w")
        yaml.safe_dump(subnet_data, file)
        file.close()

    def export_acls_yaml(self, acl_id):
        """
        Save the ALCs information to a file

        :param acl_id: Name of the bucket
        :return:
        """
        acl_id_data = self.ec2client.describe_network_acls(
            NetworkAclIds=[acl_id])
        results_acl = yaml.dump(acl_id_data).splitlines()
        file = open(acl_id + ".yml", "w")
        yaml.safe_dump(acl_id_data, file)
        file.close()

    def export_vpc_to(self, export_format, file_name):
        """Convert all VPCs in a AWS  to a excel, csv, readme, or html

         * export_format: html,string,csv, excel or markdown
         * file_name: file name to save the results.

         Returns
         -------
         N/A

         """

        aws_vpc_response = self.get_vpcs()

        vpcs = []

        for vpc in aws_vpc_response:
            vpcs.append(vpc)

        df_vpc = pd.DataFrame(vpcs)

        if export_format == 0:
            excel_writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            df_vpc.to_excel(
                excel_writer, sheet_name='VPCs', index=False)
            excel_writer.save()
        elif export_format == 1:
            df_vpc.to_csv(file_name)
        elif export_format == 2:
            df_vpc.to_string(file_name)
        elif export_format == 3:
            df_vpc.to_markdown(file_name)
        elif export_format == 4:
            df_vpc.to_html(file_name)

    def export_subnet_to(self, export_format, file_name):
        """Convert all the subnets in a AWS  to a excel, csv, readme, or html

         * export_format: html,string,csv, excel or markdown
         * file_name: file name to save the results.

         Returns
         -------
         N/A

         """

        aws_subnet_response = self.get_subnets()

        subnets = []

        for subnet in aws_subnet_response:
            subnets.append(subnet)

        df_subnets = pd.DataFrame(subnets)

        if export_format == 0:
            excel_writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            df_subnets.to_excel(
                excel_writer, sheet_name='Subnets', index=False)
            excel_writer.save()
        elif export_format == 1:
            df_subnets.to_csv(file_name)
        elif export_format == 2:
            df_subnets.to_string(file_name)
        elif export_format == 3:
            df_subnets.to_markdown(file_name)
        elif export_format == 4:
            df_subnets.to_html(file_name)

    def export_acl_to(self, export_format, file_name):
        """Convert all the ACLs in a AWS  to a excel, csv, readme, or html

         * export_format: html,string,csv, excel or markdown
         * file_name: file name to save the results.

         Returns
         -------
         N/A

         """

        aws_acl_response = self.get_acl_network()

        acls = []

        for acl in aws_acl_response:
            acls.append(acl)

        df_acls = pd.DataFrame(acls)

        if export_format == 0:
            excel_writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            df_acls.to_excel(
                excel_writer, sheet_name='acls', index=False)
            excel_writer.save()
        elif export_format == 1:
            df_acls.to_csv(file_name)
        elif export_format == 2:
            df_acls.to_string(file_name)
        elif export_format == 3:
            df_acls.to_markdown(file_name)
        elif export_format == 4:
            df_acls.to_html(file_name)

    def export_network_interfaces_to(self, export_format, file_name):
        """Convert all the Network interfaces in a AWS  to a excel, csv, readme, or html

         * export_format: html,string,csv, excel or markdown
         * file_name: file name to save the results.

         Returns
         -------
         N/A

         """

        network_interfaces = self.get_network_interfaces()

        network_interfaces_list = []

        for interface in network_interfaces:
            network_interfaces_list.append(interface)

        df_interfaces = pd.DataFrame(network_interfaces_list)

        if export_format == 0:
            excel_writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            df_subnets.to_excel(
                excel_writer, sheet_name='Subnets', index=False)
            excel_writer.save()
        elif export_format == 1:
            df_interfaces.to_csv(file_name)
        elif export_format == 2:
            df_interfaces.to_string(file_name)
        elif export_format == 3:
            df_interfaces.to_markdown(file_name)
        elif export_format == 4:
            df_interfaces.to_html(file_name)
