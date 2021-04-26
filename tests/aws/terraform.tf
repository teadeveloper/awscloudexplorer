#https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/custom-service-endpoints

provider "aws" {
  s3_force_path_style = true
}


variable "instance_count" {
  default = "2"
}

variable "instance_type" {
  default = "t2.nano"
}


resource "aws_instance" "awsinstances" {
  count         = "2"
  ami           = "ami-04169656fea786776"
  instance_type = "t2.nano"

  tags = {
    Name  = "Terraform-${count.index + 1}"
    Batch = "cloudexplorer"
  }
}

variable "s3_bucket_names" {
  type = list
  default = [
   "bucketatstt00001",
   "bucketbtest00002",
   "bucketctest00003",
   "bucketdtest00004",
   "bucketetest00005",
   ]
}

resource "aws_s3_bucket" "aws_buckets" {
  count         = "4"
  bucket        = var.s3_bucket_names[count.index]
  acl           = "private"
  force_destroy = true

    tags = {
    tag1 = "valor1"
  }
}


resource "aws_efs_file_system" "efs_ce1" {
  creation_token = "my-product1"

  tags = {
    tag1 = "valor1"
  }
}


resource "aws_efs_file_system" "efs_ce2" {
  creation_token = "my-product2"

  tags = {
    tag1 = "valor2"
  }
}


resource "aws_efs_file_system" "efs_ce3" {
  creation_token = "my-product3"

  tags = {
    tag1 = "valor3"
  }
}


variable "username" {
  type = "list"
  default = ["user1","user2","user3"]
}
#main.tf
resource "aws_iam_user" "users_ce" {
  count = "3"
  name = "${element(var.username,count.index )}"
}

resource "aws_iam_group" "developers1" {
  name = "developers1"
  path = "/users/"
}

resource "aws_iam_group" "developers2" {
  name = "developers2"
  path = "/users/"
}

resource "aws_iam_group" "developers3" {
  name = "developers3"
  path = "/users/"
}


data "archive_file" "lambda_zip" {
    type          = "zip"
    source_file   = "index.js"
    output_path   = "lambda_function.zip"
}

resource "aws_lambda_function" "test_lambda0" {
  filename         = "lambda_function.zip"
  function_name    = "test_lambda1"
  role             = "${aws_iam_role.iam_for_lambda_tf.arn}"
  handler          = "index.handler"
  source_code_hash = "${data.archive_file.lambda_zip.output_base64sha256}"
  runtime          = "nodejs12.x"
}

resource "aws_lambda_function" "test_lambda1" {
  filename         = "lambda_function.zip"
  function_name    = "test_lambda2"
  role             = "${aws_iam_role.iam_for_lambda_tf.arn}"
  handler          = "index.handler"
  source_code_hash = "${data.archive_file.lambda_zip.output_base64sha256}"
  runtime          = "nodejs12.x"
}

resource "aws_lambda_function" "test_lambda2" {
  filename         = "lambda_function.zip"
  function_name    = "test_lambda3"
  role             = "${aws_iam_role.iam_for_lambda_tf.arn}"
  handler          = "index.handler"
  source_code_hash = "${data.archive_file.lambda_zip.output_base64sha256}"
  runtime          = "nodejs12.x"
}

resource "aws_iam_role" "iam_for_lambda_tf" {
  name = "iam_for_lambda_tf"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}