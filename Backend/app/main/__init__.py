from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from .config import config_by_name
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from . import config


db = SQLAlchemy()
flask_bcrypt = Bcrypt()

#Added for Uploads of file


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    patch_request_class(app)

    return app

