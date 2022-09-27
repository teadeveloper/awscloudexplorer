import datetime
import time
import pandas as pd
import streamlit as st
from PIL import Image
from providers.aws.ec2 import AwsEc2
from providers.aws.s3 import AwsS3
from providers.aws.network import AwsNetwork
from providers.aws.security import AwsSecurity
from providers.aws.efs import AwsEfs
from providers.aws.iam import AwsIam
from providers.aws.lambdafunc import AwsLambda
from hurry.filesize import size

import yaml

with open("forms/aws_form.yml") as f:
    configuration = yaml.safe_load(f)

aws_region = configuration["aws_region"]
aws_end_end_point = configuration["aws_end_end_point"]


ec2 = AwsEc2(aws_end_end_point, aws_region)
S3 = AwsS3(aws_end_end_point, aws_region)
Network = AwsNetwork(aws_end_end_point, aws_region)
Security = AwsSecurity(aws_end_end_point, aws_region)
EFS = AwsEfs(aws_end_end_point, aws_region)
IAM = AwsIam(aws_end_end_point, aws_region)
LAMBDA = AwsLambda(aws_end_end_point, aws_region)

@st.cache
def run_fxn(n: int) -> list:
    return range(n)


def main():
    """Generación de la webapp con streamlit"""
    # Definir título
    st.title("Título: Tutorial de Streamlit")

    # Definir Header/Subheader
    st.header("Este es un header")
    st.subheader("Este es un subheader")

    # Definir un Texto
    st.text("Texto: Hola Streamlit")


if __name__ == "__main__":
    main()