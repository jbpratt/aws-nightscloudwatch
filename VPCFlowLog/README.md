# VPC Flow Log Watcher

This template provisions the following:
  - A Lambda function to act as the remediation action
  - A CloudWatch Event rule/pattern to match on "create-vpc" and "delete-flow-logs"
  - An IAM role for the Lambda function, allowing for CloudWatch logging and EC2 permissions
