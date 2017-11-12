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

@app.route("/")
def index():


    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

###--------------------------
# Main
###--------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
