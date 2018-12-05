# A simple blog using flask with a database

#https://www.bogotobogo.com/python/Flask/Python_Flask_Blog_App_Tutorial_5.php

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime
import os
import uuid
import json


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

#Enable Flask Migrate
migrate = Migrate(app, db)

#Set path to images
UPLOAD_FOLDER = '/home/milsteam4144/mysite/images/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


#Set up the login system
app.secret_key = "bdyew87ahdiuaWGS0'MG" # Secret random key used for cryptography
login_manager = LoginManager()
login_manager.init_app(app)

#Defines a "User" class
class User(UserMixin, db.Model): #The user class inherits from both Flask-Login's UserMixin and SQLAlchemy's db.Model

    __tablename__ = "users" #This syntax comes from SQLAlchemy's db.Model class

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username


#A function that accepts a string(username) and returns a corresponding User object from a dictionary
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(username=user_id).first()

#Defines a class to hold the comments using a model
class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    image = db.Column(db.String(500))
    posted = db.Column(db.DateTime, default=datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)

#Define the "index" VIEW
@app.route("/", methods=["GET", "POST"]) # GET allows users to view the page, POST sends data
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())

    #If the request is not a GET, it is a POST (send data) and this code will execute
    if request.method == "POST":
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        if not current_user.is_authenticated: #If the user is not logged in, redirect them to same page, but do not post the comment
            return redirect(url_for('index'))
        if f_name is None:
            image = ''
        else:
            image =  "/static/" + f_name
        comment = Comment(content=request.form["contents"], commenter=current_user, image=image) #Creates the comment object and assigns it to a variable
        db.session.add(comment) #Sends the command to the database, leaves a transaction open
        db.session.commit() #Commits the changes to the db and closes the transaction
        return redirect (url_for('index'))





#Login VIEW
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login_page.html", error=False)

    if request.method == "POST":
        user = load_user(request.form["username"])
        if user is None:
            return render_template("login_page.html", error=True)

        if not user.check_password(request.form["password"]):
            return render_template("login_page.html", error=True)
        else: #If the password matches, log the user in
            login_user(user)
            return redirect(url_for('index'))

#Logout VIEW
@app.route("/logout/")
@login_required #This means that the logout view can only be viewed by users that are logged in
def logout():
    logout_user()
    return redirect (url_for('index'))