from typing import Dict, Optional
import os
import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore


def lambda_handler(event, context) -> Dict:
    """
    Trigger function for 'delete-flow-logs' and 'create-vpc' calls.
    When triggered, check for all VPCs and enable FlowLogs if missing on any
    """

    destination: Optional[str] = os.environ.get("DESTINATION")
    assert destination, "failed to get destination"

    ec2_client = boto3.client("ec2")
    try:
        vpcs_res: Dict = ec2_client.describe_vpcs()
    except ClientError as error:
        raise error

    for vpc in vpcs_res.get("Vpcs", []):
        try:
            flow_logs_res: Dict = ec2_client.describe_flow_logs(
                Filters=[{"Name": "resource-id", "Values": [vpc.get("VpcId")]}],
            )
        except ClientError as error:
            raise error

        flow_logs = flow_logs_res.get("FlowLogs", [])

        if len(flow_logs) == 0:
            try:
                response = ec2_client.create_flow_logs(
                    ResourceIds=[vpc.get("VpcId")],
                    ResourceType="VPC",
                    TrafficType="ALL",
                    LogDestinationType="s3",
                    LogDestination=destination,
                )
            except ClientError as error:
                raise error

            if response.get("Unsuccessful", []) != []:
                raise Exception(f"failed to create_flow_logs {response}")

            print(f"Created flow logs for {vpc.get('VpcId')}")

        elif len(flow_logs) >= 1:
            exists = False
            for flow_log in flow_logs:
                if flow_log.get("LogDestination", "") == destination:
                    exists = True

            if not exists:
                try:
                    ec2_client.create_flow_logs(
                        ResourceIds=[vpc.get("VpcId")],
                        ResourceType="VPC",
                        TrafficType="ALL",
                        LogDestinationType="s3",
                        LogDestination=destination,
                    )
                except ClientError as error:
                    raise error
                print(f"Created flow logs for {vpc.get('VpcId')}")

    return {"statusCode": 200, "body": "success"}
