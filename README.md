# cloud-file-upload

In this application, a user can create an account and upload a profile picture. This will save their information on RDS in a MySQL database, it will then send an email to my personal email telling me a user has created an account. A user can enter their credentials and allow them to login to the main webapp. A user can then select up to 5 emails to upload a file to. Each address will recieve an email with a link that allows them to download the uploaded file from S3.

# Architechture

<img max-width="800" alt="arch" src="https://github.com/mfkimbell/cloud-file-upload/assets/107063397/9c56d10e-b86b-4c26-b292-ac8d1a74e797">

---

# Tools Used:
* `Flask` Webserver UI
* `Boto3` Used to connecto to S3 buckets and Lambda functions
* `S3` Store profile pictures and uploaded files
* `AWS Lambda` Calls SNS and SES functions
* `SNS` Sends email to webpage owner when new account is created
* `SES` Sends file download link to specified emails
* `MySQL/RDS` Store user credentials and profile pictures
* `EC2` Host Flask WebServer/application
* `IAM` Allows for increased user permissions.
---

1. Main page login
2. Create account page
3. File upload app page
  
<img width="609" alt="display" src="https://github.com/mfkimbell/cloud-file-sharing-service/assets/107063397/8e7f842d-ccf6-40e0-8630-86029c8685c5">
