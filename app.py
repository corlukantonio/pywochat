import datetime
import glob
import json
import os
from typing import Any

from flask import Flask
from flask_jsglue import JSGlue
from flask_migrate import Migrate
from flask_socketio import SocketIO, send
from sqlalchemy import Row, TextClause, text

import auth
import chat
from config import Config
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
def handle_message(msg: str, current_user_username: str, target_user: dict[str, Any]) -> None:
    '''
    Handles message.

    Parameters:
        msg (str): Message.
        current_user_username (str): Current user username.
        target_user (dict[str, Any]): Target user.
    '''

    current_user: Row[Any] = __get_user_by_username(current_user_username)
    target_user: Row[Any] = __get_user_by_username(target_user[2])

    print('Target user: ' + msg)

    if target_user is not None:
        print(str(target_user[0]) + ' ' + str(current_user[0]))

    __insert_message(msg, current_user, target_user)

    print('Message: ' + msg)

    send([msg, json.dumps(current_user, cls=CustomEncoder), json.dumps(target_user, cls=CustomEncoder)], broadcast=True)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Row):
            return {'id': obj.id, 'username': obj.username}
        return super().default(obj)


def __get_user_by_username(username: str) -> Row[Any]:
    '''
    Gets user by username.

    Parameters:
        user (str): Username.

    Returns:
        Row[Any] | None: User.
    '''

    sql: TextClause = text('SELECT * FROM users WHERE username = :username')
    params: dict[str, Any] = {'username': username}

    return db.session.execute(sql, params).fetchone()


def __insert_message(msg: str, current_user: Row[Any], target_user: dict[str, Any]) -> None:
    '''
    Inserts message.

    Parameters:
        msg (str): Message.
        current_user (Row[Any]): Current user.
        target_user (dict[str, Any]): Target user.
    '''

    sql: TextClause = text(
        f'''
        INSERT INTO {Message.__tablename__} (author_id, sent_to_id, created, content)
        VALUES (:author_id, :sent_to_id, :created, :content)
        ''')
    params: dict[str, Any] = {
        'author_id': current_user[0],
        'sent_to_id': target_user[0],
        'created': datetime.datetime.utcnow(),
        'content': msg
    }

    db.session.execute(sql, params)
    db.session.commit()


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


app.config.from_object(Config)
app.register_blueprint(auth.bp)
app.register_blueprint(chat.bp)
app.add_url_rule('/', endpoint='index')

db.init_app(app)

migrate = Migrate(app, db, directory="migrations")


if __name__ == '__main__':
    socketio.run(app)
