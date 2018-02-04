from flask import (Flask, g, render_template, flash, redirect, url_for, make_response, request)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                             login_required)
import models
import forms
import graphs
from api import *
from flask_restful import Api

DEBUG = False
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = '123456789'

api = Api(app)
api.add_resource(User, '/api/user')
api.add_resource(Data, '/api/data')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.Users.get(models.Users.id == userid)
    except models.DoesNotExist:
        return None
        
@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.get_conn()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/register', methods=('GET','POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Registration completed!", "success")
        models.Users.create_user(
                                username=form.username.data,
                                title=form.title.data,
                                first_name=form.first_name.data,
                                middle_name=form.middle_name.data,
                                last_name=form.last_name.data,
                                phone_number=form.phone_number.data,
                                email=form.email.data,
                                password=form.password.data
                                )
        return redirect(url_for('index'))
    return render_template('register.html',form = form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.Users.get(models.Users.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password is incorrect. Please try again.", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Welcome to this prototype app!\n"
                      "This app draws a graph from the numbers you imput", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password is incorrect. Please try again.", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required            
def logout():
    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for("index"))


@app.route('/', methods=('GET','POST'))
@login_required
def index():
    form = forms.DataEntry()
    if form.validate_on_submit():
        models.DataEntry.create_entry(input1=form.input1.data)
        return render_template('index.html', form = form)
    return render_template('index.html', form = form)

@app.route('/graph.png')
def plot():
    response = make_response(graphs.update_graph())
    response.mimetype = 'image/png'
    return response

if __name__ == '__main__':
    models.initialize()
    try:
        models.Users.create_user(
            username= 'admin',
            title= 'Mr.',
            first_name= 'admin',
            middle_name= '',
            last_name = 'Admin',
            phone_number = '123456789',
            email='admin@admin.com',
            password = 'admin',
            admin = True
            )
    except ValueError:
        pass

app.run(debug=DEBUG, host=HOST, port=PORT)

    
