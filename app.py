import datetime
import glob
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
from extensions import db

app: Flask = Flask(__name__, instance_relative_config=True)
JSGlue(app)
socketio: SocketIO = SocketIO(app)

model_files = glob.glob(os.path.join(os.path.dirname(__file__), 'models', '*.py'))
for model_file in model_files:
    if not model_file.endswith('__init__.py'):
        import_name = os.path.basename(model_file)[:-3]
        import_module = f'models.{import_name}'
        __import__(import_module)


@socketio.on('add_new_contact')
def add_new_contact(*json: Any) -> None:
    '''
    Adds new contact.

    Parameters:
        *json (Tuple[Any]): JSON.
    '''

    sql: TextClause = text("INSERT INTO contacts (user_1, user_2) VALUES (:user_1, :user_2)")

    db.session.execute(sql, {'user_1': json[1][2], 'user_2': json[0]})
    db.session.commit()

    db.session.execute(sql, {'user_1': json[0], 'user_2': json[1][2]})
    db.session.commit()


@socketio.on('choose_contact')
def choose_contact(*json: Any) -> None:
    '''
    Chooses contact.

    Parameters:
        *json (Tuple[Any]): JSON.
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

    print('jebo te isus')

    current_user: Row[Any] = __get_user_by_username(current_user_username)

    print('Target user: ' + msg)

    if target_user is not None:
        print(str(target_user['id']) + ' ' + str(current_user['id']))

    __insert_message(msg, current_user, target_user)

    print('Message: ' + msg)

    send([msg, current_user, target_user], broadcast=True)


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
        """
        INSERT INTO messages (author_id, sent_to_id, created, content)
        VALUES (:author_id, :sent_to_id, :created, :content)
        """)

    params: dict[str, Any] = {
        'author_id': current_user['id'],
        'sent_to_id': target_user['id'],
        'created': datetime.datetime.utcnow(),
        'content': msg
    }

    db.session.execute(sql, params)
    db.session.commit()


app.config.from_object(Config)
app.register_blueprint(auth.bp)
app.register_blueprint(chat.bp)
app.add_url_rule('/', endpoint='index')

db.init_app(app)

migrate = Migrate(app, db)


if __name__ == '__main__':
    socketio.run(app)
