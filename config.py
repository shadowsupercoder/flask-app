import os


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = '64LedGRHlXyHopEbcVMxj11pbSBosJPg'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
