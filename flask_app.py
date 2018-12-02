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

#Display the default page
@app.route("/", methods=["GET", "POST"]) # GET allows users to view the page, POST sends data
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())

    #If the request is not a GET, it is a POST (send data) and this code will execute
    if request.method == "POST":
        comment = Comment(content=request.form["contents"]) #Creates the comment object and assigns it to a variable
        db.session.add(comment) #Sends the command to the database, leaves a transaction open
        db.session.commit() #Commits the changes to the db and closes the transaction
        return redirect (url_for('index'))

#Display the login html page
@app.route("/login/")
def login():
    return render_template("login_page.html")