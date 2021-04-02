from flask import Blueprint, render_template, abort, request, url_for, redirect
from jinja2 import TemplateNotFound

from flask import Flask, Blueprint, render_template, abort, request, url_for, redirect, flash,session, escape
from flask_login import current_user, login_manager, LoginManager, login_required
from jinja2 import TemplateNotFound
from ..model.user import User
from ..model.product import Brand, Category
from ..service.product_service import save_changes, save_new_brand, save_new_category
from .. import db
import jwt
from datetime import datetime, timedelta


# import the 
from ..controller.auth_controller import Auth
from ..service.auth_helper import login_user
from .home import login



items = Blueprint('items', __name__, template_folder='../../templates/admin')


@items.route('/add_category', methods=['GET', 'POST'])
def add_category():
    # Do some stuff when you push the create category button
    # This will insert a category field in the database
    username = User.username
    if request.method == "POST":
        
        #getcategory = request.form.get('category')
        category_name = request.form['category']
        category = Category(name=category_name)

        save_changes(category)
        
        flash(f'The Category  {category_name} has been added to the database', "success")
        return redirect(url_for("items.add_category"))
    return render_template('/category.html', username=username, categories="categories")


@items.route('/add_brand', methods=['GET', 'POST'])
def add_brand():
    # Do some stuff when you push the create category button
    # This will insert a category field in the database
    username = User.username

    if request.method == "POST":
        
        brand_name = request.form['brand']
        brand = Brand(name=brand_name)

        save_changes(brand)
        
        #flash(f'The Brand {brand_name} has been added to the database', "success")
        return redirect(url_for("items.add_brand"))
    return render_template('/category.html', username=username, brands="brands")



@items.route('/add_product', methods=['GET', 'POST'])
def add_product():
    # Do some stuff
    
    #if request.method=="POST":
        #name = request.form['name']
        #price = request.form['price']
        #name = request.form['name']
        #name = request.form['name']
        #name = request.form['name']
        #name = request.form['name']
    brands = Brand.query.all()
    categories = Category.query.all()

        #flash(f'The Brand {brand_name} has been added to the database', "success")
    #return redirect(url_for("items.add_product"))
    return render_template('/category.html', brands=brands, categories=categories, products="products")