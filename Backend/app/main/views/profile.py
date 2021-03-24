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
    first_name = session['first_name']
    email = session['email'] 
    last_name = session['last_name']
    return render_template('/about.html', username=username, email=email, first_name=first_name, last_name=last_name)
        

@profile.route('/update')
def update():
    # Do some stuf
    return render_template('/update.html')
