# app/__init__.py

from flask import Flask
from flask_jsglue import JSGlue
from flask_migrate import Migrate, upgrade

from .blueprints import auth, chat
from .extensions import db, socketio
from .namespaces.chat import Chat


def create_app(environment: str | None = None, connection_uri: str | None = None) -> Flask:
    '''
    Creates Flask app.

    Parameters:
        environment (str | None): Environment.
        connection_uri (str | None): Database connection URI.

    Returns:
        Flask: Flask app.
    '''

    app: Flask = Flask(__name__, instance_relative_config=True)
    config: object = get_config(environment)

    configure_app(app, config, connection_uri)

    JSGlue(app)

    db.init_app(app)

    socketio.init_app(app)
    socketio.on_namespace(Chat('/'))

    Migrate(app, db)

    with app.app_context():
        upgrade()

    return app


def get_config(environment: str | None = None) -> object:
    '''
    Gets config based on environment.

    Parameters:
        environment (str | None): Environment.

    Returns:
        object: Config object.
    '''

    if environment == 'development':
        from .config import DevelopmentConfig as Config

    elif environment == 'testing':
        from .config import TestingConfig as Config

    elif environment == 'production':
        from .config import ProductionConfig as Config

    else:
        raise ValueError(f'Unknown environment: {environment}')

    return Config


def configure_app(app: Flask, config: object, connection_uri: str | None = None) -> None:
    '''
    Configures Flask app.

    Parameters:
        app (Flask): Flask app.
        config (object): Config object.
        connection_uri (str | None): Database connection URI.
    '''

    register_blueprints(app)

    app.config.from_object(config)

    if connection_uri:
        app.config['SQLALCHEMY_DATABASE_URI'] = connection_uri


def register_blueprints(app: Flask) -> None:
    '''
    Registers blueprints.

    Parameters:
        app (Flask): Flask app.
    '''

    app.register_blueprint(auth.bp)
    app.register_blueprint(chat.bp)

    app.add_url_rule('/', endpoint='index')
