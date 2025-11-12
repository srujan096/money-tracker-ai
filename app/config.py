import os

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-this')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, '..', 'instance', 'money_tracker.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
