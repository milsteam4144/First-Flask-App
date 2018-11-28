# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)
app.config["DEBUG"] = True #Dic key:value pair to allow debugging (go to error.log if page not compiling)

#Empty list to hold the comments
comments = []

@app.route("/", methods=["GET", "POST"]) # GET allows users to view the page, POST sends data
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=comments)

    #If the request is not a GET, it is a POST and this code will execute
    comments.append(request.form["contents"])
    return redirect (url_for('index'))

