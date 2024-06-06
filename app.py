#!/usr/bin/env python3
import os
from flask import Flask

debug_mode = False

app = Flask(__name__)

@app.route('/hello_world')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=debug_mode, port = "8080")