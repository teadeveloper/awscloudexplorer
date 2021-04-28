import boto3
import yaml
import pandas as pd
from hurry.filesize import size


class AwsS3:

    def __init__(self, aws_end_point, aws_region):

        self.bucket_filters = []
        self.aws_end_point = aws_end_point
        self.aws_region = aws_region
        self.s3_resource = boto3.resource(
            's3', endpoint_url=self.aws_end_point, region_name=self.aws_region)
        self.s3_client = boto3.client(
            's3', endpoint_url=self.aws_end_point, region_name=self.aws_region)

    def get_buckets(self):
        """Gets a S3 bucket names to be showed in the main form grid.

         Parameters
         ----------
         No needed.

         Returns
         -------
         List of dictionaries, every dictionary has the properties of a ec2 instance.
        """
        buckets_list = []

        for bucket in self.s3_client.list_buckets(Filters=self.bucket_filters)['Buckets']:
            bucket_data = [bucket["Name"], bucket["CreationDate"], self.s3_client.get_bucket_location(
                Bucket=bucket['Name'])['LocationConstraint']]
            buckets_list.append(bucket_data)

        buckets_list.insert(
            0, ["NAME", "CREATION DATE", "LOCATION CONSTRAINT"])

        return buckets_list

    def get_bucket_yml_properties(self, bucket_id):
        """ Get the configuration of a specific s3 bucket

        Parameters
        ----------
        bucket_id: the name of the S3 Bucket

        Returns
        -------
        JSON results from AWS

        """
        bucket_data = self.s3_client.list_objects(Bucket=bucket_id)
        results_bucket_data = yaml.safe_dump(bucket_data).splitlines()
        return results_bucket_data

    def export_s3_yaml(self, bucket_id):
        """
        Save the bucket information to a file

        :param bucket_id: Name of the bucket
        :return:
        """
        bucket_data = self.s3_client.list_objects(Bucket=bucket_id)
        file = open(bucket_id + ".yml", "w")
        yml_data_result = yaml.safe_dump(bucket_data, file)
        file.close()

    def export_to(self, export_format, file_name):
        """Convert all the S3 in a AWS  to a excel, csv, readme, or html

         * export_format: html,string,csv, excel or markdown
         * file_name: file name to save the results.

         Returns
         -------
         N/A

         """

        aws_response = self.get_buckets()

        s3_buckets = []

        for bucket in aws_response:

            bucket_objets = self.s3_client.list_objects_v2(Bucket=bucket[0])

            if bucket_objets["KeyCount"] > 0:
                total_bytes = 0
                for obj in bucket_objets["Contents"]:
                    total_bytes += obj["Size"]
                bucket.append(size(total_bytes))
                bucket.append(bucket_objets["KeyCount"])
            s3_buckets.append(bucket)

        df_s3 = pd.DataFrame(s3_buckets)

        if export_format == 0:
            excel_writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            df_s3.to_excel(
                excel_writer, sheet_name='S3 Buckets', index=False)
            excel_writer.save()
        elif export_format == 1:
            df_s3.to_csv(file_name)
        elif export_format == 2:
            df_s3.to_string(file_name)
        elif export_format == 3:
            df_s3.to_markdown(file_name)
        elif export_format == 4:
            df_s3.to_html(file_name)

    def get_number_of_objets_size(self, bucket_id):
        """
        Get the total number of  objects in the bucket and calculates the total size of all of them.

        :param bucket_id: bucket name
        :return: string with the total size and number of objects.
        """

        bucket_objets = self.s3_client.list_objects_v2(Bucket=bucket_id)

        num_objects = bucket_objets["KeyCount"]

        total_bytes = 0

        if bucket_objets["KeyCount"] > 0:
            total_bytes = 0
            for obj in bucket_objets["Contents"]:
                total_bytes += obj["Size"]

        message = bucket_id + " Objects: " + \
            str(num_objects) + " Total Size: " + str(size(total_bytes))

        return message
