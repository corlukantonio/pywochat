import datetime
from typing import Any

from flask import Flask
from flask_jsglue import JSGlue
from flask_socketio import SocketIO, send
from sqlalchemy import Row, TextClause, text

import auth
import chat
from config import Config
from extensions import db

app: Flask = Flask(__name__, instance_relative_config=True, template_folder='templates')
socketio: SocketIO = SocketIO()


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
def handle_message(msg: Any, current_user: Any, target_user: dict[int, Any]) -> None:
    '''
    Handles message.

    Parameters:
        msg (Any): Message.
        current_user (Any): Current user.
        target_user (dict[int, Any]): Target user.
    '''

    target_user_id: Row[Any] | None = __get_target_user_id(target_user[2])

    print('Target user: ' + msg)

    current_user_id: Row[Any] | None = __get_current_user_id(current_user)

    current_user_id: Row[Any] | None = db.session.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {'username': current_user}
    ).fetchone()

    if target_user_id is not None:
        print(str(target_user_id['id']) + ' ' + str(current_user_id['id']))

    db.session.execute(
        text(
            "INSERT INTO messages (author_id, sent_to_id, created, content) VALUES (:author_id, :sent_to_id, :created, :content)"),
        {'author_id': current_user_id['id'],
         'sent_to_id': target_user_id['id'],
         'created': datetime.datetime.utcnow(),
         'content': msg})
    db.session.commit()

    print('Message: ' + msg)

    send([msg, current_user, target_user], broadcast=True)


def __get_target_user_id(target_user: Any) -> Row[Any] | None:
    '''
    Get target user ID.

    Parameters:
        target_user (Any): Target user.

    Returns:
        Row[Any] | None: Target user ID.
    '''

    sql: TextClause = text('SELECT * FROM users WHERE username = :username')

    return db.session.execute(sql, {'username': target_user}).fetchone()


def __get_current_user_id(current_user: Any) -> Row[Any] | None:
    '''
    Get current user ID.

    Parameters:
        current_user (Any): Current user.

    Returns:
        Row[Any] | None: Current user ID.
    '''

    sql: TextClause = text('SELECT * FROM users WHERE username = :username')

    return db.session.execute(sql, {'username': current_user}).fetchone()


app.config.from_object(Config)
app.register_blueprint(auth.bp)
app.register_blueprint(chat.bp)
app.add_url_rule('/', endpoint='index')

socketio.init_app(app)
JSGlue(app)
db.init_app(app)


if __name__ == '__main__':
    socketio.run(app)
