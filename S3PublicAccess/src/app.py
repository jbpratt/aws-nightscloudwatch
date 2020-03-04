import os
from typing import Dict
import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore


def lambda_handler(event, context) -> Dict:
    bucket_name = event.get("detail", {}).get("resourceId")
    account_id = event.get("detail", {}).get("awsAccountId")
    compliance = (
        event.get("detail", {}).get("newEvaluationResult", {}).get("complianceType")
    )

    assert bucket_name, "failed to get bucket_name"
    assert account_id, "failed to get account_id"
    assert compliance, "failed to get compliance state"

    if compliance == "NON_COMPLIANT":
        try:
            boto3.client("s3").put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    "BlockPublicAcls": True,
                    "IgnorePublicAcls": True,
                    "BlockPublicPolicy": True,
                    "RestrictPublicBuckets": True,
                },
            )
        except ClientError as ex:
            raise ex

    topic_arn = os.environ.get("SNS_TOPIC")
    assert topic_arn, "No topic supplied"

    subject = f"S3 Public Access Remediated ({account_id})"
    message = f"Bucket: {bucket_name} in Account: {account_id} was made public and has been remediated"

    try:
        boto3.client("sns").publish(
            TopicArn=topic_arn, Message=message, Subject=subject
        )
    except ClientError as ex:
        raise ex

    return {"status": 200, "body": message}
