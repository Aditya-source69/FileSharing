from flask import Flask, render_template, request, redirect, url_for
import pymysql
import boto3
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os


ACCESS_KEY = "ACCESS_KEY"
SECRET_KEY = "SECRET_KEY"

#EC2 server
ENDPOINT = "appdb.ct3zejlpfiwm.us-east-1.rds.amazonaws.com"
PORT = "3306"
USR = "admin"  # ??????
PASSWORD = "password1"
DBNAME = "appdb"  # ??????


app = Flask(__name__, static_folder="staticFiles")


@app.route("/")
def main():
    return render_template("login.html")


@app.route("/notfound")
def notfound():
    return render_template("usernotfound.html")


@app.route("/login")
def login():
    render_template("login")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/add", methods=["POST"])
def add():
    email = request.form.get("email")
    password = request.form.get("password")
    desc = "account"
    #  imagepath=request.form.get("imagefilepath")
    f = request.files["file"]
    filename = f.filename.split("\\")[-1]
    f.save(secure_filename(filename))
    # filename=imagepath.split("\\")[-1]

    client = boto3.client(
        "s3",
        aws_access_key_id="aws_access_key_id",
        aws_secret_access_key=" aws_secret_access_key",
        # THIS MIGHT BE NEEDED

    )

    client.upload_file(
        filename,
        "mkcloudbucket",
        "images/" + filename,
        ExtraArgs={
            "GrantRead": 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'
        },
    )

    s3 = boto3.resource("s3")
    bucket = s3.Bucket("mkcloudbucket")
    for item in bucket.objects.all():
        print(item.key)

    conn = pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO userdetails(email,password,imagelocation) VALUES('"
        + email
        + "','"
        + password
        + "','"
        + filename
        + "');"
    )
    print("Insert Success")
    conn.commit()
    os.remove(filename)

    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name="us-east-1",
    )

    # lambda_payload={"email":email, "arn":"arn:aws:sns:us-east-1:795774402443:mksns"}
    lambda_payload = {"email": email}
    lambda_client.invoke(
        FunctionName="lambdaSNS",
        InvocationType="Event",
        Payload=json.dumps(lambda_payload),
    )

    return redirect("/")


@app.route("/uploadSend", methods=["GET", "POST"])
def uploadSend():
    email1 = request.form.get("email1")
    email2 = request.form.get("email2")
    email3 = request.form.get("email3")
    email4 = request.form.get("email4")
    email5 = request.form.get("email5")
    desc = request.form.get("description")
    #  imagepath=request.form.get("imagefilepath")
    f = request.files["file"]
    filename = f.filename.split("\\")[-1]
    f.save(secure_filename(filename))

    AllEmails = [email1, email2, email3, email4, email5]
    emails = []
    for email in AllEmails:
        if email != "":
            emails.append(email)

    client = boto3.client(
        "s3",
        aws_access_key_id="aws_access_key_id",
        aws_secret_access_key="aws_secret_access_key",
    )

    client.upload_file(
        filename,
        "mkcloudbucket",
        filename,
        ExtraArgs={
            "GrantRead": 'uri="http://acs.amazonaws.com/groups/global/AllUsers"'
        },
    )

    conn = pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO userupload(imagelocation) VALUES('" + filename + "');")
    print("Insert Success 3")
    conn.commit()

    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name="us-east-1",
    )

    lambda_payload = {"email": emails, "filename": filename}
    lambda_client.invoke(
        FunctionName="mylambdatest",
        InvocationType="Event",
        Payload=json.dumps(lambda_payload),
    )

    return render_template("/upload.html")


@app.route("/upload", methods=["GET"])
def upload():
    return render_template("/upload.html")


@app.route("/search", methods=["POST"])
def search():
    email = request.form.get("email")
    print(email)
    return redirect("viewdetails/" + str(email))


@app.route("/viewdetails/<email>")
def viewdetails(email):
    try:
        conn = pymysql.connect(
            host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM userdetails Where email ='" + email + "';")
        conn.commit()
        query_results = cur.fetchall()
        print(query_results)
        client = boto3.client(
            "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
        )
        url = client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": "applab1",
                "Key": "images/" + str(query_results[0][3]),
            },
            ExpiresIn=3600,
        )
        url = str(url).split("?")[0]
        item = {
            "email": query_results[0][0],
            "password": query_results[0][1],
            "link": url,
        }
        print(item)
        return render_template("viewdetails.html", item=item)
    except Exception as e:
        print("Database connection failed due to {}".format(e))
        return redirect("/")


@app.route("/initialize")
def initialize():
    try:
        print("INITIALIZING DATABASE")
        conn = pymysql.connect(
            host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME
        )
        cur = conn.cursor()
        try:
            cur.execute("DROP TABLE userdetails;")
            print("table deleted")
        except Exception as e:
            print("cannot delete table")
        cur.execute(
            "CREATE TABLE userdetails(email VARCHAR(20), password VARCHAR(20), imagelocation VARCHAR(50));"
        )
        print("table created")
        cur.execute(
            "INSERT INTO userdetails(email,password,imagelocation) VALUES('test1@gmail.com','password', 'Default.png');"
        )
        print("Insert Success")
        cur.execute(
            "INSERT INTO userdetails(email,password,imagelocation) VALUES('test2@gmail.com','password', 'Default.png');"
        )
        print("Insert Success")
        cur.execute(
            "INSERT INTO userdetails(email,password,imagelocation) VALUES('test3@gmail.com','password', 'Default.png');"
        )
        print("Insert Success")
        cur.execute(
            "INSERT INTO userdetails(email,password,imagelocation) VALUES('test4@gmail.com','password', 'Default.png');"
        )
        print("Insert Success")

        try:
            cur.execute("DROP TABLE userupload;")
            print("table deleted 2")
        except Exception as e:
            print("cannot delete table 2")
        cur.execute("CREATE TABLE userupload(imagelocation VARCHAR(50));")
        print("table created 2")
        cur.execute("INSERT INTO userupload(imagelocation) VALUES('Default.png');")
        print("Insert Success 2")
        cur.execute("INSERT INTO userupload(imagelocation) VALUES('Default.png');")
        print("Insert Success 2")
        cur.execute("INSERT INTO userupload(imagelocation) VALUES('Default.png');")
        print("Insert Success 2")
        cur.execute("INSERT INTO userupload(imagelocation) VALUES('Default.png');")
        print("Insert Success 2")
        conn.commit()

        cur.execute("SELECT * FROM userupload;")
        query_results = cur.fetchall()
        print(query_results)
        return redirect("/")
    except Exception as e:
        print("Database connection failed due to {}".format(e))
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
