# Night's CloudWatch

> Night gathers, and now my watch begins.

A collection of templates for monitoring for specific events and the remediation of resources based on it

- S3 buckets allowing public read or write are remediated on compliance change of Config rule
- VPC flow logs are enabled and pointing to the correct destination on all VPCs

### Setup and Build
1. [Install SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
2. Authenticate for local AWS credentials through the AWS CLI
3. Step into the desired directory and run `sam build && sam deploy --guided`
