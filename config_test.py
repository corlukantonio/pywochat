import os

basedir: str = os.path.abspath(os.path.dirname(__file__))


class ConfigTest:
    '''
    Config.
    '''

    SECRET_KEY = os.environ.get('PYWOCHAT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
