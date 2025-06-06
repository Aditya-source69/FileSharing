from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pymysql
import boto3
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from datetime import datetime

# Use environment variables for sensitive data
ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

#Database configuration
ENDPOINT = os.environ.get('DB_ENDPOINT')
PORT = os.environ.get('DB_PORT', '3306')
USR = os.environ.get('DB_USER', 'admin')
PASSWORD = os.environ.get('DB_PASSWORD')
DBNAME = os.environ.get('DB_NAME', 'appdb')

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

app = Flask(__name__, static_folder="staticFiles")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def main():
    return render_template("login.html")


@app.route("/notfound")
def notfound():
    return render_template("usernotfound.html")


@app.route("/login")
def login():
    return render_template("login.html")


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
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name="us-east-1"
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
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name="us-east-1"
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
        FunctionName="lambdaSendFileLink",
        InvocationType="Event",
        Payload=json.dumps(lambda_payload),
    )

    return render_template("/upload.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to filename to make it unique
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            unique_filename = timestamp + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            file_url = request.host_url + 'uploads/' + unique_filename
            return render_template('success.html', file_url=file_url)
    return render_template('upload.html')


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
