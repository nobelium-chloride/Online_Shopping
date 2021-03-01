""" 
    Read More on Blueprints the below document:
    https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints 
    These document is a "blueprint" of my app that renders my static pages. 
    Cretae this blue print then in the main app that will be executed, register the blueprint
"""
from flask import Blueprint, render_template, abort, request, url_for, redirect
from jinja2 import TemplateNotFound

# Defining my blueprint for the home pages/views 
home = Blueprint('home', __name__, template_folder='../../templates/home')

#Loads and index page whe UI starts/opens, this open very well
@home.route('/')
def index():
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
    if request.method == 'POST':
        
        return render_template('/profile.html')

#Register then send to email for verification before logs in
@home.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('/verify_email.html')