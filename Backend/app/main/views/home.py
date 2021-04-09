""" 
    Read More on Blueprints the below document:
    https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints 
    These document is a "blueprint" of my app that renders my static pages. 
    Cretae this blue print then in the main app that will be executed, register the blueprint
"""
from flask import Flask, Blueprint, render_template, abort, request, url_for, redirect, flash,session, escape
from flask_login import current_user, login_user, login_manager, LoginManager, logout_user, login_required, utils
from jinja2 import TemplateNotFound
from ..model.user import User
from ..model.product import Product, Category, Brand
from .. import db, flask_bcrypt
import jwt
import uuid
from datetime import datetime, timedelta
import datetime
import dateutil
from werkzeug.security import generate_password_hash, check_password_hash
#from flask.ext.login import LoginManager
import crypt
import bcrypt
from ..config import *


# import the 
from ..controller.auth_controller import Auth
from ..service.auth_helper import login_user
from ..service.user_service import save_new_user, save_changes, generate_token


# Defining my blueprint for the home pages/views 
home = Blueprint('home', __name__, template_folder='../../templates/home')

#to work on this. Not working
#login_manager.login_view = 'login'


### MOVED THIS BIT TO THE ITEMS BLUEPRINT ###
#Loads and index page whe UI starts/opens, this open very well
@home.route('/')
def index():
    #if 'username' in session:
        # return 'you are already logged as, {}!'.format(escape(session['username']))
        #return render_template('/userhome.html')
    page = request.args.get('page',1,type=int)
    products = Product.query.filter(Product.stock > 0).paginate(page=page, per_page=4)
    #brands = Brand.query.all()
    return render_template('/index.html', products=products)


#Login with details in the db/data created by API
@home.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_email = request.form['username']
        user_password = request.form['password']

        user = User.query.filter_by(email = user_email).first()

        username = user.username
        
        if user and user.check_password(user_password):
            if user.admin == 1:
                #works
                login_user(user)
                
                #Check how I can use below
                session['logged_in'] = True
                session['email'] = user.email
                session['username'] = user.username
                session['first_name'] = user.first_name
                
                
                flash('You have successfully logged in as admin.', "success")
                print('Admin Username and Passwords match', user.username)
                return render_template('/adminDashboard.html', username=username)

            #Check how I can use below 
            session['logged_in'] = True
            session['email'] = user.email 
            session['username'] = user.username
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            username = user.username

            #works
            login_user(user)

            flash('You have successfully logged in.', "success")
            print('Username and Passowords match', user.username)
        return render_template('/userhome.html', username=username, email=user.email, first_name=user.first_name) 

    print('Please enter username and/or password')
    return render_template('/login.html')


@home.route('/logout', methods=['GET', 'POST'])
def logout():

    #Removing data from session by setting logged_flag to False
    session['logged_in'] = False
    session.pop('username', None)
    session.pop('email', None)
    session.clear()

    #logout user by removing "user id"
    logout_user()
    return redirect(url_for('home.index'))


#Register then send to email for verification before logs in
@home.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST": 
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password')
        address1 = request.form['address1']
        address2 = request.form['address2']
        #city = request.form.get('city')
        #state = request.form.get('state')
        #zip_code = request.form.get('zip_code')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return render_template('home.login')

        if password == confirm_password:
            correct_pass = flask_bcrypt.generate_password_hash(password).decode('utf-8')
        
            new_user = User(public_id=str(uuid.uuid4()), registered_on=datetime.datetime.utcnow(), email=email, username=username, password_hash=correct_pass, first_name=first_name, last_name=last_name, address1= address1, address2=address2)
        
            #add the new user to the database
            save_changes(new_user)
            flash('You have registered successfully')
            #This is what I need to use. This single like
            save_new_user

            #return render_template('/verify_email.html')
            return render_template('/verify_email.html')
        else:
           flash('Passwords do not match')
    return render_template('register.html')

    
        