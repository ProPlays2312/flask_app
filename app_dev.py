# Description: This file contains the code for the web application.
#importing libraries
from flask import Flask, render_template, request
from opperations import register, login, check_sqli
#creating the app
app = Flask(__name__)

#home route
@app.route('/')
def home():
    return render_template('index.html')

#register route
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    #check if request is POST and get data
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        quote = request.form['quote']
        #check for SQL Injection
        try:
            if check_sqli(username) or check_sqli(password):
                pass
        except Exception as e:
            raise e 
        #register user 
        try:
            register(username, password, name, email, quote)
            return 'Registration successful!'
        except Exception as e:
            return f'Error: {str(e)}'

#login route
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    #check if request is POST and get data
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #check for SQL Injection
        try:
            if check_sqli(username) or check_sqli(password):
                pass
        except Exception as e:
            raise e
        #login user and get data
        try:
            if login(username, password):
                a = login(username, password)
                date, name, email, quote = a[0], a[1], a[2], a[3]
                pass
        except Exception as e:
            return f'Error: {str(e)}'
        #returning HTML
        html = f"""<!DOCTYPE html>
                     <html>
                     <head>
                            <title>Details</title>
                     </head>
                     <body>
                            <div style="text-align: center;">
                             <h2 style="color: red;">Login Successful!</h2>
                            </div>
                            <div style="text-align:left;" id="Name"><h3>Name:{name}</h3></div>
                            <div style="text-align:left;" id="Email"><h3>Email:{email}</h3></div>
                            <div style="text-align:left;" id="Date"><h3>Date</h3>{date}</div>
                            <div style="text-align:left;" id="Quote"><h3>Quote</h3>{quote}</div>
                      </body>
                      </html>"""
    return html

#running the app
if __name__ == '__main__':
    app.run(debug=False, port=8080)