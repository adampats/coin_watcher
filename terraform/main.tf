terraform {
  required_version = "~> 0.10.7"
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_sns_topic" "coin_watcher" {
  name = "coin_watcher"
  display_name = "coin_watcher"
}

resource "aws_iam_role" "coin_watcher_lambda" {
  name = "coin_watcher_lambda"
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

resource "aws_iam_role_policy" "coin_watcher_policy" {
  name = "coin_watcher_policy"
  role = "${aws_iam_role.coin_watcher_lambda.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "LambdaExecution",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Sid": "AllowSNSPublish",
      "Action": [
        "sns:Publish",
        "sns:GetTopicAttributes"
      ],
      "Effect": "Allow",
      "Resource": "${aws_sns_topic.coin_watcher.arn}"
    }
  ]
}
EOF
}

output "sns_topic_arn" {
  value = "${aws_sns_topic.coin_watcher.arn}"
}
