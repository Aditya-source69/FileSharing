import boto3


def lambda_handler(event, context):
    ACCESS_KEY = "AKIA3SR6ZX6FT4OAXVPJ"
    SECRET_KEY = "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"
    AWS_REGION = "us-east-1"
    email = event.get("email")
    sns_client = boto3.client(
        "sns",
        region_name=AWS_REGION,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    # do i need aws_access_key_id = ACCESS KEY or SECRET_KEY

    sns_client.publish(
        TopicArn="arn:aws:sns:us-east-1:795774402443:mksns",
        Message="New user Added: " + email,
        Subject="New User",
    )
