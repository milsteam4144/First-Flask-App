# A very simple Flask Hello World app for you to get started with...

from processing import do_calculation, calculate_mode
from flask import Flask, request
#STOPPED AT SESSIONS TO THE RESCUE

app = Flask(__name__)
app.config["DEBUG"] = True #Dic key:value pair to allow debugging (go to error.log if page not compiling)

@app.route('/hello')
def hello_world():
    return 'Hello this is Mallory!'

@app.route('/login')
def login():
    return '<b>Enter your login credentials here:</b> '


@app.route('/addNumbers', methods=["GET", "POST"])#This allows the page to send/post data as well as retrieve the webpage

def adder_page():
    #IF THE METHOD IS POST: Validate the user input to ensure they are of the float datatype
    errors = ""
    if request.method == "POST":
        number1 = None
        number2 = None
        try:
            number1 = float(request.form["number1"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number1"])
        try:
            number2 = float(request.form["number2"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number2"])

        #Do the calculation
        if number1 is not None and number2 is not None:
            result = do_calculation(number1, number2)
            return '''
                <html>
                    <body>
                        <p>The result is {result}</p>
                        <p><a href="/">Click here to calculate again</a>
                    </body>
                </html>
            '''.format(result=result)

    return '''
        <html>
            <body>
            {errors}
                <p>Enter your numbers:
                <form method="post" action="."> <!--This makes the "Do calculation" button (button with type "submit) request the same page that is on, but use the "post" method-->
                                                <!--HTTP "get" method gets a page from server--"post" method provides the server with data to store or process-->
                    <p><input name="number1" /></p>
                    <p><input name="number2" /></p>
                    <p><input type="submit" value="Do calculation" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)


#To get the mode (number that appears most often)
inputs = []

@app.route("/", methods=["GET", "POST"])
def mode_page():
    errors = ""
    if request.method == "POST":
        try:
            inputs.append(float(request.form["number"]))
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["number"])

        if request.form["action"] == "Calculate number":
            result = calculate_mode(inputs)
            inputs.clear()
            return '''
                <html>
                    <body>
                        <p>{result}</p>
                        <p><a href="/">Click here to calculate again</a>
                    </body>
                </html>
            '''.format(result=result)

    if len(inputs) == 0:
        numbers_so_far = ""
    else:
        numbers_so_far = "<p>Numbers so far:</p>"
        for number in inputs:
            numbers_so_far += "<p>{}</p>".format(number)

    return '''
        <html>
            <body>
                {numbers_so_far}
                {errors}
                <p>Enter your number:
                <form method="post" action=".">
                    <p><input name="number" /></p>
                    <p><input type="submit" name="action" value="Add another" /></p>
                    <p><input type="submit" name="action" value="Calculate number" /></p>
                </form>
            </body>
        </html>
    '''.format(numbers_so_far=numbers_so_far, errors=errors)
