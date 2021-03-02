# Online_Shopping/Backend/app/profile.py

from flask import Blueprint, render_template, abort, request, url_for, redirect
from jinja2 import TemplateNotFound



profile = Blueprint('profile', __name__, template_folder='../../templates/profile')


@profile.route('/about')
def about(about):
    # Do some stuff
    return render_template('/about.html')

@profile.route('/edit')
def edit():
    # Do some stuf
    return render_template('/edit.html')
