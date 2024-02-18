import datetime
import glob
import json
import os
from typing import Any

from flask import Flask
from flask_jsglue import JSGlue
from flask_migrate import Migrate, upgrade
from flask_socketio import SocketIO, send
from sqlalchemy import Row, TextClause, text

import auth
import chat
from config import Config
from config_test import ConfigTest
from extensions import db, socketio
from models.contact import Contact
from models.message import Message

file_path = os.path.dirname(__file__)
model_path = os.path.join(file_path, 'models', '*.py')
model_files = glob.glob(model_path)

for model_file in model_files:
    if not model_file.endswith('__init__.py'):
        import_name = os.path.basename(model_file)[:-3]
        import_module = f'models.{import_name}'
        __import__(import_module)


app: Flask = Flask(__name__, instance_relative_config=True)
JSGlue(app)
socketio.init_app(app)


@socketio.on('add_contact')
def add_contact(json: dict[str, Any]) -> None:
    '''
    Adds contact.

    Parameters:
        json (dict[str, Any]): JSON.
    '''

    sql: TextClause = text(
        f'''
        INSERT INTO {Contact.__tablename__} (user_1, user_2)
        VALUES (:user_1, :user_2)
        ''')

    logged_in_user_username = json['loggedInUserUsername']
    found_contact_username = json['foundContact'][2]

    db.session.execute(sql, {'user_1': found_contact_username, 'user_2': logged_in_user_username})
    db.session.commit()

    db.session.execute(sql, {'user_1': logged_in_user_username, 'user_2': found_contact_username})
    db.session.commit()


@socketio.on('choose_contact')
def choose_contact(*json: Any) -> None:
    '''
    Chooses contact.

    Parameters:
        *json (tuple[Any]): JSON.
    '''

    pass


@socketio.on('message')
def handle_message(msg: str, sender_username: str, target_user: list[str]) -> None:
    '''
    Handles message.

    Parameters:
        msg (str): Message.
        sender_username (str): Sender username.
        target_user (list[str]): Target user.
    '''

    print(target_user)

    sender: Row[Any] | None = __get_user_by_username(sender_username)
    receiver: Row[Any] | None = __get_user_by_username(target_user["username"])

    if sender is None:
        raise ValueError('Sender cannot be None.')

    if receiver is None:
        raise ValueError('Receiver cannot be None.')

    __insert_message(msg, sender, receiver)

    data = __get_message_update(msg, sender, receiver)

    send(json.dumps(data), broadcast=True)


def __get_user_by_username(username: str) -> (Row[Any] | None):
    '''
    Gets user by username.

    Parameters:
        username (str): Username.

    Returns:
        Row[Any] | None: User.
    '''

    sql: TextClause = text('SELECT * FROM users WHERE username = :username')
    params: dict[str, Any] = {'username': username}

    return db.session.execute(sql, params).fetchone()


def __insert_message(msg: str, sender: Row[Any], receiver: Row[Any]) -> None:
    '''
    Inserts message.

    Parameters:
        msg (str): Message.
        sender (Row[Any]): Sender.
        receiver (Row[Any]): Receiver.
    '''

    sql: TextClause = text(
        f'''
        INSERT INTO {Message.__tablename__} (author_id, sent_to_id, created, content)
        VALUES (:author_id, :sent_to_id, :created, :content)
        ''')
    params: dict[str, Any] = {
        'author_id': sender[0],
        'sent_to_id': receiver[0],
        'created': datetime.datetime.utcnow(),
        'content': msg
    }

    db.session.execute(sql, params)
    db.session.commit()


def __get_message_update(msg: str, sender: Row[Any], receiver: Row[Any]) -> dict[str, Any]:
    return {
        "message": msg,
        "sender": {
            "id": sender.id,
            "username": sender.username
        },
        "receiver": {
            "id": receiver.id,
            "username": receiver.username
        }
    }


def create_app() -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    JSGlue(app)
    socketio: SocketIO = SocketIO(app)

    model_files = glob.glob(os.path.join(os.path.dirname(__file__), 'models', '*.py'))
    for model_file in model_files:
        if not model_file.endswith('__init__.py'):
            import_name = os.path.basename(model_file)[:-3]
            import_module = f'models.{import_name}'
            __import__(import_module)

    app.config.from_object(Config)
    app.register_blueprint(auth.bp)
    app.register_blueprint(chat.bp)
    app.add_url_rule('/', endpoint='index')
    db.init_app(app)

    return app

def create_app_test(connection_uri: str) -> Flask:
    app: Flask = Flask(__name__, instance_relative_config=True)
    JSGlue(app)
    socketio: SocketIO = SocketIO(app)

    model_files = glob.glob(os.path.join(os.path.dirname(__file__), 'models', '*.py'))
    for model_file in model_files:
        if not model_file.endswith('__init__.py'):
            import_name = os.path.basename(model_file)[:-3]
            import_module = f'models.{import_name}'
            __import__(import_module)

    app.config.from_object(ConfigTest)
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_uri
    app.register_blueprint(auth.bp)
    app.register_blueprint(chat.bp)
    app.add_url_rule('/', endpoint='index')
    db.init_app(app)
    migrate = Migrate(app, db, directory="migrations")

    with app.app_context():
        upgrade()

    return app


app.config.from_object(Config)
app.register_blueprint(auth.bp)
app.register_blueprint(chat.bp)
app.add_url_rule('/', endpoint='index')

db.init_app(app)

migrate = Migrate(app, db, directory="migrations")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
