from os import path, environ
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = '64LedGRHlXyHopEbcVMxj11pbSBosJPg'
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY_PTX = environ.get('SECRET_KEY_PTX')
    SHOP_ID = environ.get('SHOP_ID')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
