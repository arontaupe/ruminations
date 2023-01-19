from flask import Flask, render_template  # makes a flask app and serves it to a specified port
import os  # can grab environment variables
import threading  # enables multithread behaviour
import time  # accurately measures time differences
from datetime import datetime  # handles dates
import json  # make me interact with json
from flask_httpauth import HTTPBasicAuth
# protects the rest api from being publicly available
from werkzeug.security import check_password_hash, generate_password_hash
# hashes the password, so it is not passed in clear

# initialize the flask app
app = Flask(__name__)

# get variables from outside the container, used for password protection
user = os.environ.get('USER')
pw = os.environ.get('PASS')
# hash the password
users = {user: generate_password_hash(pw)}
auth = HTTPBasicAuth()


def get_port():
    """
    finds out if the environment has a predefined port, otherwise use 5002
    :return: port number
    """
    return int(os.environ.get("PORT", 5002))


@auth.verify_password
def verify_password(username, password):
    """
Checks if http user is in user list and checks for correctness of password
    :param username:
    :param password:
    :return: boolean verified or not
    """
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.route('/')
def index():
    """
  default route, has text, so I can see when the app is running, indicates the Last date of update
    :return: Hello World
    """
    time_modified = datetime.fromtimestamp(os.stat("app.py").st_mtime)
    format_str = "%d/%m/%Y %H:%M:%S"
    # format datetime using strftime()
    time_modified = time_modified.strftime(format_str)
    text = f'Last Modified: {time_modified}'
    print(text)
    return render_template('index.html')


def main():
    # execute and expose the backend as a flask app on a given port
    app.run(host='0.0.0.0', port=get_port(), debug=True)


# run the app
if __name__ == '__main__':
    main()
