# cloud-file-upload

(in progress, due Aug 8th)

# Architechture

<img width="1250" alt="arch" src="https://github.com/mfkimbell/cloud-file-upload/assets/107063397/9c56d10e-b86b-4c26-b292-ac8d1a74e797">


# Tools Used:
* `Flask` Webserver UI
* `Boto3` Used to connecto to S3 buckets and Lambda functions
* `AWS Lambda` Calls SNS
* `SNS` Sends email to webpage owner when new account is created
* `MySQL` Store user data
