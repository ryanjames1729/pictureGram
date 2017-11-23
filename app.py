from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import *
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random, os, time, config
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




###--------------------------
# File upload handler
###--------------------------

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(15))
    usname = db.Column(db.String(15))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Pictures(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usname = db.Column(db.String(25))
    file = db.Column(db.String(25))
    date = db.Column(db.String(25))
    caption = db.Column(db.String(300))

class PhotoForm(FlaskForm):
    image = FileField('Upload your image here.')
    caption = StringField('What\'s going on in this picture?')

def message(new_user):
        # Basic variables for authorization:

    email = config.EMAIL
    pwd = config.PW
    auth = (email, pwd)
    # Message object:
    m = Message(auth=auth)
    # Recipients
    m.setRecipients(new_user)
    # Subject:
    m.setSubject('Thanks for Signing Up')
    # Body:
    user = Users.query.filter_by(email=new_user).first()
    uname = user.usname
    name = user.name
    m.setBody('Hello, {}.\n\n Thanks for signing up for an account on PicShare.\n\nYour user name is: {}\n\nLogin and start sharing pictures!\n -Ava'.format(name, uname))
    # Send:
    m.sendMessage()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route("/", methods=['GET', 'POST'])
def index():
    global current_user
    error = None
    if request.method == 'POST':
        usname = request.form['username']
        password = request.form['password']
        current_user = Users.query.filter_by(usname=usname).first()

        print("Auth?: " + str(current_user.is_authenticated))
        if current_user:
            if current_user.password == password:
                login_user(current_user)

                print("Auth?: " + str(current_user.is_authenticated))
                return render_template('profile.html', name=current_user.name)
            else:
                error='Invalid Credentials. Please try again.'
                flash("Wrong Password")
        else:
            error='You have not signed up for an account yet.'
            return render_template('index.html', error=error)


    return render_template('index.html')

@app.route("/login", methods=['GET','POST'])
def login():
    global current_user
    error = None
    if request.method == 'POST':
        usname = request.form['username']
        password = request.form['password']
        current_user = Users.query.filter_by(usname=usname).first()

        print("Auth?: " + str(current_user.is_authenticated))
        if current_user:
            if current_user.password == password:
                login_user(current_user)

                print("Auth?: " + str(current_user.is_authenticated))
                return render_template('profile.html', name=current_user.name)
            else:
                error='Invalid Credentials. Please try again.'
                flash("Wrong Password")
        else:
            error='You have not signed up for an account yet.'


    return render_template('login.html', error=error)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You are now logged out.')
    return redirect(url_for('index'))

@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = email[:(email.index("@"))]
        new_user = Users(name=name, email=email, usname=user, password=password, admin=0)
        db.session.add(new_user)
        db.session.commit()
        message(email)
        flash("Check your e-mail for account confirmation.")

    return render_template("signup.html")

@app.route("/feed")
@login_required
def feed():
    print("Auth?: " + str(current_user.is_authenticated))
    pictures = Pictures.query.all()
    pictures.reverse()


    return render_template('feed.html', pictures=pictures)

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = PhotoForm()
    f = form.image.data
    today = str(date.today())
    if form.validate_on_submit():
        try:
            filename = secure_filename(f.filename)
            basedir = os.path.abspath(os.path.dirname(__file__))
            f.save(os.path.join(basedir, app.config['UPLOADED_PHOTOS_DEST'], filename))
            new_photo = Pictures(usname = current_user.usname, file = filename, date = today, caption = str(form.caption.data))
            db.session.add(new_photo)
            db.session.commit()

            file_path = app.config['UPLOADED_PHOTOS_DEST'] + "/" + filename
            print('Path fo file is: ' + file_path)
        except:
            flash("File did not upload correctly.")



    return render_template('upload.html', form=form)

@app.route("/like", methods=['GET', 'POST'])
@login_required
def like():

    return redirect(url_for('feed.html'))


@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404

###--------------------------
# Main
###--------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
