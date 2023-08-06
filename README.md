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
* `MySQL/RDS` Store user credentials, profile pictures, and file uploads
* `EC2` Host Flask WebServer/application
* `IAM` Set access and identity permissions
---

1. Main page login
2. Create account page
3. File upload app page

<img width="607" alt="display" src="https://github.com/mfkimbell/cloud-file-sharing-service/assets/107063397/55885c0d-49e2-484a-a4b9-a19b043f3d1d">


---
This is what the email notification will look like
  
<img width="669" alt="email" src="https://github.com/mfkimbell/cloud-file-sharing-service/assets/107063397/b6fa9a79-4367-48f8-a0e2-98c87c25e8e8">
