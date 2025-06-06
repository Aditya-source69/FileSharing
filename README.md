# Cloud File Sharing Service

A secure file sharing service built with Flask and AWS services.

## Features
- User account creation with profile pictures
- File upload and sharing
- Email notifications for new users and file sharing
- Secure file storage using AWS S3
- Database storage using AWS RDS

## Setup Instructions

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# AWS Credentials
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key

# Database Configuration
export DB_ENDPOINT=your_rds_endpoint
export DB_PORT=3306
export DB_USER=admin
export DB_PASSWORD=your_database_password
export DB_NAME=appdb
```

4. Initialize the database:
```bash
python app.py
```
Then visit: `http://localhost:5000/initialize`

## Deployment on Render.com

1. Fork this repository
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Add the required environment variables in Render dashboard
5. Deploy!

## AWS Services Used
- S3 for file storage
- RDS for database
- Lambda for serverless functions
- SNS for notifications
- SES for email sending

## Security Notes
- Never commit AWS credentials to version control
- Use environment variables for sensitive data
- Keep your AWS credentials secure
- Configure proper IAM roles and permissions

# cloud-file-upload

<img width="1006" alt="cloud file workflow" src="https://github.com/mfkimbell/cloud-file-sharing-service/assets/107063397/24d39502-8fbc-4e58-b2b4-5bb51a40998c">



In this application, a user can
create an account and upload a profile picture. This will save their information on RDS in a MySQL database, it will then send an email to my personal email telling me a user has created an account. A user can enter their credentials and allow them to login to the main webapp. A user can then select up to 5 emails to upload a file to. Each address will recieve an email with a link that allows them to download the uploaded file from S3.

---

# Tools Used:
* `Flask` Used to operate the webserver
* `Boto3` Python SDK used to connecto to S3 buckets and Lambda functions (can do other aws services)
* `S3` Store profile pictures and uploaded files
* `AWS Lambda` Calls SNS and SES functions
* `SNS` Sends email to webpage owner when new account is created
* `SES` Sends file download link to specified emails
* `MySQL/RDS` Store user credentials, profile pictures, and file uploads
* `EC2` Host Flask WebServer/application
* `IAM` Set access and identity permissions that we use when connecting with Boto3
---
When people access the application, they can only add files if they've added credentials to the MySQL database in AWS RDS. Anyone can connect, as by default, the "/add" route has permissions built into it to add a username and password to S3, my email is alerted after the function is invoked.

### lambda function: lambdaSNS

``` python
import boto3
def lambda_handler(event, context):
ACCESS_KEY = "AKIA3SR6ZX6FT4OAXVPJ"
SECRET_KEY = "*******************"
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
```
---

After that, they can use the "/login" route, which allows the user to input data and call the "/uploadSend" endpoint. This stores data in s3, keeps track of the file name in the MySQL database, and invokes my lambda function "lambdaSendFileLink" which sends an email to the entered emails that contains a link. 

### lambda function: lambdaSendFileLink

``` python
import boto3
import json
ACCESS_KEY = "AKIA3SR6ZX6FT4OAXVPJ"
SECRET_KEY = "********************"
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
```

---

1. Main page login
2. Create account page
3. File upload app page

<img width="607" alt="display" src="https://github.com/mfkimbell/cloud-file-sharing-service/assets/107063397/55885c0d-49e2-484a-a4b9-a19b043f3d1d">

---

This is the notification for new users:
<img width="1012" alt="Screenshot 2023-09-29 at 1 00 21 PM" src="https://github.com/mfkimbell/cloud-file-sharing-service/assets/107063397/ee5b7ae7-5e43-42aa-8ea6-68ad90b97463">


---

This is what is recieved when someone shares a file:
  
<img width="669" alt="email" src="https://github.com/mfkimbell/cloud-file-sharing-service/assets/107063397/b6fa9a79-4367-48f8-a0e2-98c87c25e8e8">
