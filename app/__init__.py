from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import app_config
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object(app_config[config_name])
    Bootstrap(flask_app)
    db.init_app(flask_app)

    login_manager.init_app(flask_app)
    login_manager.login_message = "You must be logged in to access this page"
    login_manager.login_view = "auth.login"
    migrate = Migrate(flask_app, db)

    from app import models
    from .auth import auth as auth_blueprint
    flask_app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    flask_app.register_blueprint(home_blueprint)

    from .blog import blog as blog_blueprint
    flask_app.register_blueprint(blog_blueprint)

    return flask_app
