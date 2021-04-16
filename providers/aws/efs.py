import boto3
import yaml
import pandas as pd
from hurry.filesize import size

class AwsEfs:

    def __init__(self, aws_end_point, aws_region):

        self.efs_filters = []
        self.aws_end_point = aws_end_point
        self.aws_region = aws_region
        self.efs_client = boto3.client(
            'efs', endpoint_url=self.aws_end_point, region_name=self.aws_region)

    def get_efs(self):
        """Gets a EFS file systems  to be showed in the main form grid.

         Parameters
         ----------
         No needed.

         Returns
         -------
         List of dictionaries, every dictionary has the properties of a EFS instance.
        """
        efs_list = []

        for efs in self.efs_client.describe_file_systems()["FileSystems"]:
            size = efs["SizeInBytes"]["Value"]
            efs_data = [efs["FileSystemId"],size, efs["CreationTime"],efs["Encrypted"],efs["NumberOfMountTargets"],efs["ThroughputMode"]]
            efs_list.append((efs_data))

        efs_list.insert(0,["FILESYSTEM ID","SIZE","CREATION TIME","ENCRYPTED","NUMBER MOUNT TARGETS","THROUGH PUT MODE"])
        return efs_list

    def get_efs_yml_properties(self, efs_id):
        """ Get the configuration of a specific EFS filesystem

        Parameters
        ----------
        efs_id: the name of the EFS

        Returns
        -------
        JSON results from AWS

        """
        try:
            efs_data = self.efs_client.describe_file_systems(FileSystemId=efs_id)
            results_efs_data = yaml.safe_dump(efs_data).splitlines()
            return results_efs_data
        except:
            return ["You have selected the HEAD, please select an item."]

    def export_efs_yaml(self, efs_id):
        """
        Save the EFS information to a file

        :param efs_id: Name of the efs_id
        :return:
        """
        bucket_data = self.efs_client.describe_file_systems(FileSystemId=efs_id)
        file = open(efs_id + ".yml", "w")
        yml_data_result = yaml.safe_dump(bucket_data, file)
        file.close()

    def export_to(self, export_format, file_name):
        """Convert all the EFS in a AWS  to a excel, csv, readme, or html

         * export_format: html,string,csv, excel or markdown
         * file_name: file name to save the results.

         Returns
         -------
         N/A

         """

        aws_response = self.get_efs()

        efs_fs = []

        for efs in aws_response:
            efs_fs.append(efs)

        df_efs= pd.DataFrame(efs_fs)

        if export_format == 0:
            excel_writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            df_efs.to_excel(
                excel_writer, sheet_name='EFS', index=False)
            excel_writer.save()
        elif export_format == 1:
            df_efs.to_csv(file_name)
        elif export_format == 2:
            df_efs.to_string(file_name)
        elif export_format == 3:
            df_efs.to_markdown(file_name)
        elif export_format == 4:
            df_efs.to_html(file_name)


