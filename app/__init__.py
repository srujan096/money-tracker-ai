import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv()  # load environment variables from .env

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)

    # Load default config
    app.config.from_object('app.config.BaseConfig')

    # Allow overrides from instance config or env
    instance_config = os.path.join(app.instance_path, 'config.py')
    if os.path.exists(instance_config):
        app.config.from_pyfile(instance_config)

    if config_object:
        app.config.from_object(config_object)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    from app import models  # ensure models are imported so Flask can see them
    from app.models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # Import and register blueprints / routes
    from .routes import main_bp
    from .auth_routes import auth_bp

    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)


    return app
