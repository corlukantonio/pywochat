import os

basedir: str = os.path.abspath(os.path.dirname(__file__))


class Config:
    '''
    Config.
    '''

    SECRET_KEY = os.environ.get('PYWOCHAT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgres://hfmvpnanaienwj:b59da37312e5dca8ea7b9dc38cfcc4448fb01b9b56fa335722516ddb98ffee74@ec2-52-205-45-222.compute-1.amazonaws.com:5432/d5caqfl5fvpqrm'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
