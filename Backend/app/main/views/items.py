from flask import Blueprint, render_template, abort, request, url_for, redirect, current_app, message_flashed, flash
from jinja2 import TemplateNotFound
import os
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

from flask import Flask, Blueprint, render_template, abort, request, url_for, redirect, flash,session, escape
from flask_login import current_user, login_manager, LoginManager, login_required
from jinja2 import TemplateNotFound
from ..model.user import User
from ..model.product import Brand, Category, Product
from ..service.product_service import save_changes, save_new_brand, save_new_category
from .. import db
from ...main import create_app
import jwt
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from secrets import token_hex
import secrets
from werkzeug import secure_filename, FileStorage
import datetime

# import the 
from ..controller.auth_controller import Auth
from ..service.auth_helper import login_user
from .home import login

photos = UploadSet('photos', IMAGES)

items = Blueprint('items', __name__, template_folder='../../templates/admin')


### INSERT ITEMS ###
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
        
        flash(f'The Category {category_name} has been added to the database', "success")
        #return redirect(url_for("items.add_category"))
    return render_template('/category.html', username=username, add_a_category="add_a_category")


@items.route('/add_brand', methods=['GET', 'POST'])
def add_brand():
    # Do some stuff when you push the create category button
    # This will insert a category field in the database
    username = User.username

    if request.method == "POST":
        
        brand_name = request.form['brand']
        brand = Brand(name=brand_name)

        save_changes(brand)
        flash("The Brand {brand_name} has been added to the database", "success")
        return redirect(url_for("items.add_brand"))
    return render_template('/category.html', username=username, add_a_brand="add_a_brand")


@items.route('/add_product', methods=['GET', 'POST'])
def add_product():
    username = User.username
    brand = Brand.query.all()
    category = Category.query.all()

    if request.method=="POST":
        name = request.form['product']
        price = request.form['price']
        stock = request.form['stock']
        discount = request.form['discount']
        color = request.form['color']
        category_name = request.form.get('category')
        brand_name = request.form.get('brand')
        # Add discriprion and image fields to forms as well as db
        description = request.form['description']

        #The below can save a file to folder images
        image_main=photos.save(request.files.get('image_main'), name=secrets.token_hex(10) + ".")
        image_1=photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2=photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3=photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        product = Product(name=name, price=price, stock=stock, discount=discount, color=color, category_id=category_name, brand_id=brand_name, description=description, pub_date=datetime.datetime.utcnow(), image_main=image_main, image_1=image_1,image_2=image_2, image_3=image_3)
        save_changes(product)
        flash('The product { product } has been added successfully', 'Success')
        return redirect(url_for("items.add_product"))

    #products = Product.query.all()
    return render_template('/category.html', username=username, brands=brand, categories=category, add_a_product="add_a_product")


### SELECT ALL ITEMS ###
@items.route('/view_products')
def view_products():
    products = Product.query.all()
    return render_template('/tables_records.html', products=products, view_all_products="view_all_products")


@items.route('/view_categories')
def view_categories():
    categories = Category.query.all()
    return render_template('/tables_records.html', categories=categories, view_all_categories="view_all_categories")


@items.route('/view_brands')
def view_brands():
    brands = Brand.query.all()
    return render_template('/tables_records.html', brands=brands, view_all_brands="view_all_brands")

@items.route('/brands')
def brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('/category.html', brands=brands)


### UPDATE ITEMS == Edit Buttons ###
@items.route('/update_brand/<int:id>', methods=['GET', 'POST'])
def update_brand(id):
    update_brand = Brand.query.get_or_404(id) 
    brand = request.form.get('brand_name')
    if request.method == "POST":
        update_brand.name = brand
        db.session.commit()
        #flash(f'The Brand {brand} has been updated to the database', "success")
        return redirect(url_for("items.view_brands"))
    return render_template('/update_records.html', edit_a_brand="edit_a_brand", update_brand=update_brand)


@items.route('/update_category/<int:id>', methods=['GET', 'POST'])
def update_category(id):
    update_category = Category.query.get_or_404(id) 
    category = request.form.get('category_name')
    if request.method == "POST":
        update_category.name = category
        db.session.commit()
        return redirect(url_for("items.view_categories"))
    return render_template('/update_records.html', update_category=update_category)


@items.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    # Work on this
    brands = Brand.query.all()
    categories = Category.query.all()

    update_product = Product.query.get_or_404(id)

    name = request.form.get('product')
    price = request.form.get('price')
    stock = request.form.get('stock')
    discount = request.form.get('discount')
    color = request.form.get('color')
    category_name = request.form.get('category')
    brand_name = request.form.get('brand')
    description = request.form.get('description')

    if request.method == "POST":
        update_product.name = name
        update_product.price = price 
        update_product.stock = stock
        update_product.discount = discount
        update_product.color = color
        update_product.category_id = category_name
        update_product.brand_id = brand_name
        update_product.description = description

        if request.files.get('image_main'):
            try:
                os.unlink(os.path.join(current_app.root_path, "../static/images/" + update_product.image_main))
                update_product.image_main = photos.save(request.files.get('image_main'), name=secrets.token_hex(10) + ".")
            except:
                update_product.image_main=photos.save(request.files.get('image_main'), name=secrets.token_hex(10) + ".")


        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "../static/images/" + update_product.image_1))
                update_product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                update_product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")


        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "../static/images/" + update_product.image_2))
                update_product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                update_product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")


        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "../static/images/" + update_product.image_3))
                update_product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                update_product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        db.session.commit()
        return redirect(url_for("items.view_products"))
    return render_template('/update_records.html', brands=brands, categories=categories, update_product=update_product)


### DELETE ITEMS ###
@items.route('/delete_category/<int:id>', methods=['POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        db.session.commit()
        return redirect(url_for('items.view_categories'))
    flash(f'The Category { category } cannot be deleted', "Warning!")
    return redirect(url_for('items.view_categories'))


@items.route('/delete_brand/<int:id>', methods=['POST'])
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        db.session.commit()
        return redirect(url_for('items.view_brands'))
    flash('The Brand { brand } cannot be deleted', "Warning!")
    return redirect(url_for('items.view_brands'))


@items.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    if request.method=="POST":
        try: 
            os.unlink(os.path.join(current_app.root_path, "../static/images/" + update_product.image_main))
            os.unlink(os.path.join(current_app.root_path, "../static/images/" + update_product.image_1))
            os.unlink(os.path.join(current_app.root_path, "../static/images/" + update_product.image_2))
            os.unlink(os.path.join(current_app.root_path, "../static/images/" + update_product.image_3))
        except Exception as e:
            print(e)

        db.session.delete(product)
        db.session.commit()
        flash('The Product { product } has been deleted', "Success!")
        return redirect(url_for('items.view_products'))
    flash(f'The Product { product } cannot be deleted', "Warning!")
    return redirect(url_for('items.view_products'))