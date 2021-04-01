from .. import db

class Brand(db.Model):
    """ Brand Model to store products brand and category """
    __tablename__ = "brand"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

class Category(db.Model):
    """ Category Model to store products brand and category """
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


#db.create_all()