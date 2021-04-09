from flask import Blueprint, render_template, abort, request, url_for, redirect, current_app, message_flashed, flash, session
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

cart = Blueprint('cart', __name__, template_folder='../../templates')


# Feature to allow to add multiple products to cart 
def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


# Feature to allow to add 1 ptoduct item to cart (cannot add same product twice though)
@cart.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    try:
        session['shop_cart'] = True
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        color = request.form.get('colors')
        product = Product.query.filter_by(id=product_id).first()
        print(product.name)

        if product_id and quantity and color and request.method=="POST":
            DictItems = {product_id:{'name':product.name, 'price':int(product.price),'discount':product.discount, 'color': product.color, 'description':product.description, 'quantity':quantity}}
            print(DictItems) 
            if 'shopping_cart' in session:
                print(session['shopping_cart'])
                if product_id in session['shopping_cart']:
                    print('This item is already in your cart')
                else:
                    session['shopping_cart'] = MagerDicts(session['shopping_cart'], DictItems)
                    return redirect(request.referrer) 
            else:
                session['shopping_cart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)




