# Remediate Public S3 Access

This template provisions the following:
  - A Lambda function to act as the remediation action
  - A CloudWatch Event rule/pattern to match on Config compliance changes
  - An IAM role for the Lambda function, allowing for CloudWatch logging and S3 PutBucketPublicAccessBlock
  - An SNS topic to send an alert of the remediation action taking place
  - An SNS topic subscription to the email supplied in the Parameters field
  - Two config rules with the source identifiers of S3_BUCKET_PUBLIC_WRITE_PROHIBITED and S3_BUCKET_PUBLIC_READ_PROHIBITED
