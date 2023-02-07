from flask import Flask, render_template, request, flash  # makes a flask app and serves it to a specified port
import os  # can grab environment variables
from datetime import datetime  # handles dates
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
# protects the rest api from being publicly available
from werkzeug.security import check_password_hash, generate_password_hash
# hashes the password, so it is not passed in clear
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, InputRequired, Length, Regexp, NumberRange
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField

# initialize the flask app
app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# the name of the database; add path if necessary
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# get variables from outside the container, used for password protection
user = os.environ.get('USER')
pw = os.environ.get('PASS')
# hash the password
webUsers = {user: generate_password_hash(pw)}
auth = HTTPBasicAuth()


# each table in the database needs a class to be created
# db.Model is required - don't change it
# identify all columns by name and data type
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    iban = db.Column(db.String)
    updated = db.Column(db.String)

    def __init__(self, firstname, lastname, iban, updated):
        self.firstname = firstname
        self.lastname = lastname
        self.iban = iban
        self.updated = updated


class AddUser(FlaskForm):
    # id used only by update/edit
    id_field = HiddenField()
    firstname = StringField('What is your first Name?',
                            [InputRequired(),
                             Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid name"),
                             Length(min=3, max=25, message="Invalid name length")
                             ])
    lastname = StringField('What is your last Name?',
                           [InputRequired(),
                            Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid name"),
                            Length(min=3, max=25, message="Invalid name length")
                            ])
    iban = StringField('What is your IBAN?',
                       [InputRequired(),
                        Regexp(r'^[A-Za-z\s\-\']+$', message="Invalid IBAN"),
                        Length(min=3, max=25, message="Invalid IBAN length")
                        ])
    # updated - date - handled in the route function
    updated = HiddenField()
    submit = SubmitField('Submit and collectivize me')


def get_port():
    """
    finds out if the environment has a predefined port, otherwise use 5002
    :return: port number
    """
    return int(os.environ.get("PORT", 5002))


@app.before_first_request
def create_tables():
    db.create_all()


@auth.verify_password
def verify_password(username, password):
    """
Checks if http user is in user list and checks for correctness of password
    :param username:
    :param password:
    :return: boolean verified or not
    """
    if username in webUsers:
        return check_password_hash(webUsers.get(username), password)
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


@app.route('/show')
def show():
    return render_template('show.html', users=Users.query.all())


@app.route('/mousetrack')
def mousetrack():
    return render_template('mousetrack_demo.html')

@app.route('/mousesave')
def mousesave():
    return render_template('mousetrack_save_demo.html')

@app.route('/onboard', methods=['GET', 'POST'])
def onboard():
    # you must tell the variable 'form' what you named the class, above
    form = AddUser()

    if form.validate_on_submit():
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        iban = request.form['iban']

        # get today's date from function, above all the routes
        now = datetime.now()  # current date and time
        format_str = "%d/%m/%Y %H:%M:%S"
        updated = now.strftime(format_str)

        # the data to be inserted
        record = Users(firstname, lastname, iban, updated)
        # Flask-SQLAlchemy magic adds record to database
        db.session.add(record)
        db.session.commit()
        # create a message to send to the template
        message = f"The data for {firstname} has been submitted."
        return render_template('onboard.html',
                               form=form,
                               message=message)
    else:
        # show validaton errors
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form, field).label.text,
                    error
                ), 'error')
        return render_template('onboard.html', form=form)


def main():
    # execute and expose the backend as a flask app on a given port
    app.run(host='0.0.0.0', port=get_port(), debug=True)


# run the app
if __name__ == '__main__':
    main()
