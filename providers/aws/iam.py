import boto3
import yaml
import pandas as pd


class AwsIam:

    def __init__(self, aws_end_point, aws_region):

        self.aws_end_point = aws_end_point
        self.aws_region = aws_region
        self.iam_client = boto3.client(
            'iam', endpoint_url=self.aws_end_point, region_name=self.aws_region)

    def get_users(self):
        """Gets accounts to be showed in the main form grid.

         Parameters
         ----------
         No needed.

         Returns
         -------
         List of dictionaries, every dictionary has the properties of an account
        """
        accounts_list = []

        accounts = self.iam_client.list_users()["Users"]

        for account in accounts:
            account_data = [account["UserName"], account["UserId"],account["CreateDate"], account["Path"]]
            accounts_list.append(account_data)

        accounts_list.insert(0, ["USER NAME", "USER ID", "CREATE DATE", "PATH"])
        return accounts_list

    def get_roles(self):
        """Gets roles to be showed in the main form grid.

         Parameters
         ----------
         No needed.

         Returns
         -------
         List of dictionaries, every dictionary has the properties of roles
        """
        role_list = []
        for role in self.iam_client.list_roles()["Roles"]:
            role_data = [role["RoleName"],role["RoleId"], role["CreateDate"], role["MaxSessionDuration"]]
            role_list.append(role_data)

        role_list.insert(0, ["ROLE NAME", "ROLE ID", "CREATE DATE", "SESSION DURATION"])
        return role_list

    def get_groups(self):
        """Gets groups to be showed in the main form grid.

         Parameters
         ----------
         No needed.

         Returns
         -------
         List of dictionaries, every dictionary has the properties of groups
        """
        group_list = []

        for group in self.iam_client.list_groups()["Groups"]:
            group_data = [group["GroupName"], group["GroupId"], group["CreateDate"]]
            group_list.append(group_data)

        group_list.insert(0, ["GROUP NAME", "GROUP ID", "CREATE DATE"])
        return group_list

    def get_policies(self):
        """Gets policies to be showed in the main form grid.

         Parameters
         ----------
         No needed.

         Returns
         -------
         List of dictionaries, every dictionary has the properties of policies
        """
        policies_list = []

        policies = self.iam_client.list_policies()["Policies"]

        for policy in policies:
            policy_data = [policy["PolicyName"],policy["PolicyId"], policy["CreateDate"],policy["Arn"]]
            policies_list.append(policy_data)

        policies_list.insert(0, ["GROUP NAME", "GROUP ID", "CREATE DATE","ARN"])
        return policies_list


    def get_user_yml_properties(self, username):

        """
        :param username: The name of the user
        :return: a yml with the user configuration
        """
        data = self.iam_client.get_user(UserName=username)
        results = yaml.dump(data).splitlines()
        return results


    def get_groups_yml_properties(self, groupname):

        """
        :param groupname: The group name of the group
        :return: a yml with the user configuration
        """
        data = self.iam_client.get_group(GroupName=groupname)
        results = yaml.dump(data).splitlines()
        return  results


    def get_policy_yml_properties(self, arnname):

        """
        :param arnname: The group name of the PolicyArn (string)
        The Amazon Resource Name (ARN) of the managed policy that you want information ab

        :return: a yml with the user configuration
        """
        data = self.iam_client.get_policy(PolicyArn=arnname)
        results = yaml.dump(data).splitlines()
        return  results

    def get_role_yml_properties(self, rolename):

        """
        :param rolename: The role name


        :return: a yml with the user configuration
        """
        data = self.iam_client.get_role(RoleName=rolename)
        results = yaml.dump(data).splitlines()
        return  results

    def export_user_yaml(self, username):
        """
        Save the Username information to a file

        :param username: The name of the user
        :return:
        """
        data = self.iam_client.get_user(UserName=username)
        file = open(username + ".yml", "w")
        yml_data_result = yaml.safe_dump(data, file)
        file.close()

    def export_policy_yaml(self, arnname,groupname):
        """
        Save the policy name information to a file

        :param arnname: The arn string of the policy
        :param groupname: The name of the group
        :return:
        """
        data = self.iam_client.get_policy(PolicyArn=arnname)
        file = open(groupname + ".yml", "w")
        yml_data_result = yaml.safe_dump(data, file)
        file.close()

    def export_group_yaml(self, groupname):
        """
        Save the group name information to a file

        :param username: The name of the group
        :return:
        """
        data = self.iam_client.get_group(GroupName=groupname)
        file = open(groupname + ".yml", "w")
        yml_data_result = yaml.safe_dump(data, file)
        file.close()

    def export_role_yaml(self, rolename):
        """
        Save the role name information to a file

        :param username: The name of the role
        :return:
        """
        data = self.iam_client.get_role(RoleName=rolename)
        file = open(rolename + ".yml", "w")
        yml_data_result = yaml.safe_dump(data, file)
        file.close()
