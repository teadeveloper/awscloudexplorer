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
            account_data = [account["UserId"], account["UserName"], account["CreateDate"], account["Path"]]
            accounts_list.append(account_data)

        accounts_list.insert(0, ["USER ID", "USER NAME", "CREATE DATE", "PATH"])
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
            role_data = [role["RoleId"], role["RoleName"], role["CreateDate"], role["MaxSessionDuration"]]
            role_list.append(role_data)

        role_list.insert(0, ["ROLE ID", "ROLE NAME", "CREATE DATE", "SESSION DURATION"])
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
            group_data = [group["GroupId"], group["GroupName"], group["CreateDate"]]
            group_list.append(group_data)

        group_list.insert(0, ["GROUP ID", "GROUP NAME", "CREATE DATE"])
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
            policy_data = [policy["PolicyId"], policy["PolicyName"], policy["CreateDate"]]
            policies_list.append(policy_data)

        policies_list.insert(0, ["GROUP ID", "GROUP NAME", "CREATE DATE"])
        return policies_list
