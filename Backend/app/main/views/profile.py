# Online_Shopping/Backend/app/profile.py

from datetime import datetime, timedelta
from flask_login import current_user, login_user, login_manager, LoginManager, logout_user, login_required
import jwt
from flask import (Blueprint, Flask, abort, escape, flash, redirect,
                   render_template, request, session, url_for)
from jinja2 import TemplateNotFound
from .home import home

from .. import db
from ..model.user import User

#from flask.ext.login import LoginManager

profile = Blueprint('profile', __name__, template_folder='../../templates/profile')


@profile.route('/about')
def about():
    username = session['username']
    email = session['email'] 
    first_name = session['first_name']
    
    return render_template('/about.html', username=username, email=email, first_name=first_name)
    
@profile.route('/dashboard')   
def dashboard():
    username = session['username']
    first_name = session['first_name']
    email = session['email'] 
    last_name = session['last_name']
    return render_template('/dashboard.html', username=username, email=email, first_name=first_name, last_name=last_name)

@profile.route('/update')
def update():
    # Do some stuf
    return render_template('/update.html')

@profile.route('/update_username', methods=['GET', 'POST'])
def update_username():
    
    if request.method == "POST":
        new_username = request.form['username']
        update_username = User.query.filter_by(username=new_username).first()
        update_username.username = new_username
        new_username = session['username']
        db.session.commit()
        # return redirect(url_for('profile.about'))
    return render_template('/about.html', edit_username="edit_username", update_username=update_username)

@profile.route('/edit_password')
def edit_password():
    pass

@profile.route('/edit_email')
def edit_email():
    pass

@profile.route('/edit_address')
def edit_address():
    pass

@profile.route('/edit_phone')
def edit_phone():
    pass