import os

basedir: str = os.path.abspath(os.path.dirname(__file__))


class Config:
    '''
    Config.
    '''

    SECRET_KEY = os.environ.get('PYWOCHAT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    '''
    Development config.
    '''

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('PYWOCHAT_DATABASE_URI')


class TestingConfig(Config):
    '''
    Testing config.
    '''

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('PYWOCHAT_DATABASE_URI')


class ProductionConfig(Config):
    '''
    Production config.
    '''

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('PYWOCHAT_DATABASE_URI')
