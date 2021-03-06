from flask import Blueprint, render_template, abort, request, url_for, redirect
from jinja2 import TemplateNotFound

from flask import Flask, Blueprint, render_template, abort, request, url_for, redirect, flash,session, escape
from flask_login import current_user, login_manager, LoginManager
from jinja2 import TemplateNotFound
from ..model.user import User
from .. import db
import jwt
from datetime import datetime, timedelta


# import the 
from ..controller.auth_controller import Auth
from ..service.auth_helper import login_user
from .home import login



items = Blueprint('items', __name__, template_folder='../../templates/admin')


@items.route('/create_category', methods=['GET', 'POST'])
def create_category():
    # Do some stuff when you push the create category button
    # This will insert a category field in the database
    username = User.username

    return render_template('/create_category.html', username=username)


@items.route('/product')
def product(product):
    # Do some stuff
    return render_template('/product.html')