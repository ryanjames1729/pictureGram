from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import *
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random
import os, time
from werkzeug.utils import secure_filename
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from O365 import Message
from datetime import *

###--------------------------
# App Configuration
###--------------------------

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "howsitgoingbro1234508234129458751239487"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
firstTime = False

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(15))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


@app.route("/")
def index():


    return render_template('index.html')



@app.route("/login", methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                return render_template('profile.html', name=user.name)
            else:
                error='Invalid Credentials. Please try again.'
        else:
            error='You have not signed up for an account yet.'
    return render_template('login.html', error=error)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

###--------------------------
# Main
###--------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
