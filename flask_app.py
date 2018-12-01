# A simple blog using flask with a database

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["DEBUG"] = True #Dic key:value pair to allow debugging (go to error.log if page not compiling)

#Code to connect to Database
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username = "milsteam4144",
    password = "Happy2_dev",
    hostname="milsteam4144.mysql.pythonanywhere-services.com",
    databasename="milsteam4144$comments",
    )
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#Creates a class to hold the comments using a model
class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))

#Empty list to hold the comments
comments = []

@app.route("/", methods=["GET", "POST"]) # GET allows users to view the page, POST sends data
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=comments)

    #If the request is not a GET, it is a POST and this code will execute
    comments.append(request.form["contents"])
    return redirect (url_for('index'))

