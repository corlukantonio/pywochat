import glob
import os
from typing import Any

import psycopg2
from flask import Flask
from flask_jsglue import JSGlue
from flask_migrate import Migrate, upgrade
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

from blueprints import auth, chat
from config import Config
from config_test import ConfigTest
from extensions import db, socketio
from namespaces.chat import Chat

file_path = os.path.dirname(__file__)
model_path = os.path.join(file_path, 'models', '*.py')
model_files = glob.glob(model_path)

for model_file in model_files:
    if not model_file.endswith('__init__.py'):
        import_name = os.path.basename(model_file)[:-3]
        import_module = f'models.{import_name}'
        __import__(import_module)


# def create_app() -> Flask:
#     app: Flask = Flask(__name__, instance_relative_config=True)
#     JSGlue(app)
#     socketio.init_app(app)

#     model_files = glob.glob(os.path.join(
#         os.path.dirname(__file__), 'models', '*.py'))
#     for model_file in model_files:
#         if not model_file.endswith('__init__.py'):
#             import_name = os.path.basename(model_file)[:-3]
#             import_module = f'models.{import_name}'
#             __import__(import_module)

#     app.config.from_object(Config)
#     app.register_blueprint(auth.bp)
#     app.register_blueprint(chat.bp)
#     app.add_url_rule('/', endpoint='index')
#     db.init_app(app)

#     return app


def create_app_test(connection_uri: str) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    JSGlue(app)
    socketio.init_app(app)
    socketio.on_namespace(Chat('/'))

    model_files = glob.glob(os.path.join(
        os.path.dirname(__file__), 'models', '*.py'))
    for model_file in model_files:
        if not model_file.endswith('__init__.py'):
            import_name = os.path.basename(model_file)[:-3]
            import_module = f'models.{import_name}'
            __import__(import_module)

    app.config.from_object(ConfigTest)
    app.secret_key = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_uri
    app.register_blueprint(auth.bp)
    app.register_blueprint(chat.bp)
    app.add_url_rule('/', endpoint='index')
    db.init_app(app)
    migrate = Migrate(app, db, directory="migrations")

    with app.app_context():
        upgrade()

    return app


def create_database_if_not_exists(database_uri: str, database_name: str = "pywochat") -> None:
    """
    Checks if the specified database exists, and creates it if it does not.

    Parameters:
        database_uri (str): The URI to connect to the PostgreSQL server.
        database_name (str): The name of the database to create if it doesn't exist.
    """
    # Modify the URI to connect to the default 'postgres' database instead of the target DB
    default_uri = database_uri.rsplit('/', 1)[0] + '/postgres'

    try:
        # Connect to the PostgreSQL server
        engine = create_engine(default_uri)
        with engine.connect() as connection:
            # Check if the target database already exists
            result = connection.execute(text(
                f"SELECT 1 FROM pg_database WHERE datname = :dbname"), {"dbname": database_name})

            if not result.fetchone():
                # If database does not exist, create it
                # End transaction for CREATE DATABASE
                connection.execute(text("COMMIT"))
                connection.execute(text(f"CREATE DATABASE {database_name}"))
                print(f"Database '{database_name}' created successfully.")
            else:
                print(f"Database '{database_name}' already exists.")

    except OperationalError as e:
        print(f"Error: {e}. Unable to check or create the database.")


if 'TESTING' not in os.environ:
    app: Flask = Flask(__name__, instance_relative_config=True)
    JSGlue(app)
    socketio.init_app(app)
    socketio.on_namespace(Chat('/'))

    app.config.from_object(Config)
    app.register_blueprint(auth.bp)
    app.register_blueprint(chat.bp)
    app.add_url_rule('/', endpoint='index')

    db.init_app(app)

    migrate = Migrate(app, db, directory="migrations")


# with app.app_context():
#     create_database_if_not_exists(app.config['SQLALCHEMY_DATABASE_URI'])
#     db.create_all()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
