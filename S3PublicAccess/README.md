# Remediate Public S3 Access

This template provisions the following:
  - Lambda function to act as the remediation action
  - CloudWatch Event rule/pattern to match on Config compliance changes
  - IAM role for the Lambda function, allowing for CloudWatch logging and S3 PutBucketPublicAccessBlock
  - SNS topic to send an alert of the remediation action taking place
  - SNS subscription to the email supplied in the Parameters field
  - Two config rules with the source identifiers of
     - S3_BUCKET_PUBLIC_WRITE_PROHIBITED
     - S3_BUCKET_PUBLIC_READ_PROHIBITED

### Setup
1. Edit `template.yaml` to update the `RECEIVER` variable with a valid email address for the alert from SNS
2. Run `sam build && sam deploy --guided`


#### Notes
- This setup can be swapped around to instead react upon CW event similar to the VPC function. Reasoning here would be that Config has a charge associated with each evaluation of the rule which could get costly.
