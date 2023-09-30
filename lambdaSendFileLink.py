import boto3
import json

ACCESS_KEY = "AKIA3SR6ZX6FT4OAXVPJ"
SECRET_KEY = "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"
AWS_REGION = "us-east-1"


def lambda_handler(event, context):
    ACCESS_KEY = "AKIA3SR6ZX6FT4OAXVPJ"
    SECRET_KEY = "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"
    AWS_REGION = "us-east-1"
    emails = event.get("email")
    botoS3 = boto3.client(
        "s3",
        region_name=AWS_REGION,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    botoSES = boto3.client("ses", region_name="us-east-1")
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
                "Data": "Test email",
            },
        },
        Source="mkimbell@uab.edu",
    )

    print(response)

    return {
        "statusCode": 200,
        "body": json.dumps(
            "Email Sent Successfully. MessageId is: " + response["MessageId"]
        ),
    }
