from app.main import db
from app.main.model.product import Brand, Category


def get_all_categories():
    return Category.query.all()

def get_all_brands():
    return Brand.query.all()

def save_new_brand(data):
    brand = Brand.query.filter_by(name=data['name']).first()
    if not brand:
        new_brand = Brand(name=data['name'])
        save_changes(new_brand)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Brand already exists. Please Create new one.',
        }
        return response_object, 409

def save_new_category(data):
    category = Category.query.filter_by(name=data['name']).first()
    if not category:
        new_category = Category(name=data['name'])
        save_changes(new_category)
    else:
        response_object = {
            'status': 'fail',
            'message': 'Category already exists. Please Create new one.',
        }
        return response_object, 409

def save_changes(data):
    db.session.add(data)
    db.session.commit()
