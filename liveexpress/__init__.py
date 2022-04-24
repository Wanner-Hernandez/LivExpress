from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from liveexpress.config import Config
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

def create_app(config_name=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from liveexpress.auth import auth as auth_bp
    from liveexpress.main import main as main_bp
    from liveexpress.blog import post as post_bp
    from liveexpress.errors.handlers import errors

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(errors)


    return app