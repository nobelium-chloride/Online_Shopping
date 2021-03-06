from flask import Blueprint, render_template, abort, request, url_for, redirect
from jinja2 import TemplateNotFound



items = Blueprint('items', __name__, template_folder='../../templates/admin')


@items.route('/add_category')
def add_category():
    # Do some stuf
    return render_template('/add_category.html')


@items.route('/product')
def product(product):
    # Do some stuff
    return render_template('/product.html')