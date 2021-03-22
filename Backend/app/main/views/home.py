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
from .. import db
import jwt
from datetime import datetime, timedelta
#from flask.ext.login import LoginManager


# import the 
from ..controller.auth_controller import Auth
from ..service.auth_helper import login_user


# Defining my blueprint for the home pages/views 
home = Blueprint('home', __name__, template_folder='../../templates/home')

#to work on this. Not working
#login_manager.login_view = 'login'

#Loads and index page whe UI starts/opens, this open very well
@home.route('/')
def index():
    if 'username' in session:
        #return 'you are already logged as, {}!'.format(escape(session['username']))
        return render_template('/userhome.html')
    return render_template('/index.html')

@home.route('/choose_login')
def choose_login():
   return render_template('/login.html')

@home.route('/choose_register')
def choose_register():
   return render_template('/register.html')    

@home.route('/no_account')
def no_account():
    return redirect(url_for('home.choose_register'))

@home.route('/have_account')
def have_account():
    return redirect(url_for('home.choose_login'))

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
                
                flash('You have successfully logged in as admin.', "success")
                print('Admin Username and Passwords match', user.username)
                return render_template('/adminDashboard.html', username=username)

            #Check how I can use below 
            session['logged_in'] = True
            session['email'] = user.email 
            session['username'] = user.username
            username = user.username

            #works
            login_user(user)

            flash('You have successfully logged in.', "success")
            print('Username and Passowords match', user.username)
            return render_template('/userhome.html', username=username, email=user.email) 

    print('Please enter username and/or password')
    return redirect(url_for('home.choose_login'))


@home.route('/logout', methods=['GET', 'POST'])
# @login_required --Check how to use this decorator
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
@home.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('/verify_email.html')
