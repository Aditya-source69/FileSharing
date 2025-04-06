import boto3
import json
import os

# Use environment variables for AWS credentials
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = "us-east-1"

def lambda_handler(event, context):
    emails = event.get("email")
    botoS3 = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )
    botoSES = boto3.client("ses", region_name=AWS_REGION)
    key = event.get("filename")
    bucket = "mkcloudbucket"
    url = f"https://{bucket}.s3.amazonaws.com/{key}"

    response = botoSES.send_email(
        Destination={"ToAddresses": emails},
        Message={
            "Body": {
                "Text": {
                    "Charset": "UTF-8",
                    "Data": "Your file is ready to download: " + url,
                }
            },
            "Subject": {
                "Charset": "UTF-8",
                "Data": "File Sharing Notification",
            },
        },
        Source="your-verified-ses-email@example.com",  # Replace with your verified SES email
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            "Email Sent Successfully. MessageId is: " + response["MessageId"]
        ),
    }
