# cloud-file-upload

(in progress, due Aug 8th)

<img width="1250" alt="Project Architecture" src="https://github.com/mfkimbell/cloud-file-upload/assets/107063397/39024bec-f049-4d3c-bf70-5f35496be306">


**Tools Used:**
* `Flask` Webserver UI
* `Boto3` Used to connecto to S3 buckets and Lambda functions
* `AWS Lambda` Calls SNS
* `SNS` Sends email to webpage owner when new account is created
