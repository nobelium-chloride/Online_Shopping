import os
import unittest
import connexion
from flask_migrate import Migrate, MigrateCommand
from flask_login import current_user, login_user, login_manager, LoginManager, logout_user, login_required

from flask_script import Manager
from app.main.model import blacklist
from app.main.model.user import User
from app.main.model.product import Category, Category

from app.main import create_app, db

from app import blueprint

#1. Imported the home blueprint from home package in vews folder
from app.main.views.home import home
from app.main.views.profile import profile
from app.main.views.items import items
from app.main.views.cart import cart


app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')

app.register_blueprint(blueprint)

#2. Now register your above imported blueprints in the main app
app.register_blueprint(home)
app.register_blueprint(profile)
app.register_blueprint(items)
app.register_blueprint(cart)

#login Manager to use the login/logout functions/methods
login_manager = LoginManager()
login_manager.login_view = '/home.login' # Just added this
login_manager.init_app(app)


app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



if __name__ == '__main__':
    manager.run()


#Use this to delete/migrate db; when drop does not allow, then migrate again#
#with app.app_context():
    #if db.engine.url.drivername == 'sqlite':
        #migrate.init_app(app, db, render_as_batch=True)
    #else:
        #migrate.init_app(app, db)