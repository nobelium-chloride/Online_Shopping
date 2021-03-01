# app/__init__.py

from flask_restplus import Api
from flask import Blueprint
from flask import Flask
import connexion

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns


app = Flask(__name__)

blueprint = Blueprint('api', __name__, url_prefix='/myapi')

api = Api(blueprint,
    title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service',
          )   

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)


