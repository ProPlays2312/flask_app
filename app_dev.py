from flask import Flask, render_template, request
from opperations import register, login
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            register(username, password)
            return 'Registration successful!'
        except Exception as e:
            return f'Error: {str(e)}'

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            if login(username, password):
                return 'Login successful!'
        except Exception as e:
            return f'Error: {str(e)}'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)