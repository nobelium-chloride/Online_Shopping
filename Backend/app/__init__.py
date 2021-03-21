# app/__init__.py

from flask_restplus import Api
from flask import Blueprint
from flask import Flask
import connexion
from datetime import timedelta
from werkzeug.utils import cached_property
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns


app = Flask(__name__)
app.secret_key = b'2%N@0^by##@!k)vx~'

# this does not seem to work. Session doesnt time out in 3min
app.permanent_session_lifetime =  timedelta(minutes=3)

blueprint = Blueprint('api', __name__, url_prefix='/myapi')

api = Api(blueprint,
    title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service',
          )   

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)


