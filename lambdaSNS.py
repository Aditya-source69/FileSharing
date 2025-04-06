import boto3
import os


def lambda_handler(event, context):
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = "us-east-1"
    email = event.get("email")
    sns_client = boto3.client(
        "sns",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    # do i need aws_access_key_id = ACCESS KEY or SECRET_KEY

    sns_client.publish(
        TopicArn="arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:YOUR_TOPIC_NAME",  # Replace with your SNS topic ARN
        Message="New user Added: " + email,
        Subject="New User Registration",
    )
