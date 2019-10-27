from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow

login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()

from app.api.api import(EmployeeListResource, DepartmentResource,
                        DepartmentListResource, RoleResource,
                        RoleListResource, EmployeeResource)
from app.blueprints.home import home
from app.blueprints.admin import admin
from app.blueprints.auth import auth
from app.api import api_bp

api = Api(api_bp)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///management.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py')

    Bootstrap(app)
    db.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    app.register_blueprint(home)
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(api_bp, url_prefix='/api')

    api.add_resource(EmployeeListResource, '/Employee')
    api.add_resource(EmployeeResource, '/Employee/<int:id>')
    api.add_resource(DepartmentListResource, '/Department')
    api.add_resource(DepartmentResource, '/Department/<int:id>')
    api.add_resource(RoleResource, '/Role/<int:id>')
    api.add_resource(RoleListResource, '/Role')

    with app.app_context():
        db.create_all()

    from app import models
    return app


