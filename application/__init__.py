import os

from flask import Flask
from flask_socketio import SocketIO, send
from flask_jsglue import JSGlue
from application.db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    socketio = SocketIO(app)
    jsglue = JSGlue(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'application.sqlite')
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load from test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @socketio.on('add_new_contact_event')
    def add_new_contact(*json):
        db = get_db()
        db.executemany(
            'INSERT INTO contact (user_1, user_2) VALUES (?, ?)',
            [(json[1][2], json[0]), (json[0], json[1][2])]
        )
        db.commit()

    @socketio.on('choose_contact')
    def choose_contact(*json):
        pass

    @socketio.on('message')
    def handleMessage(msg, currentUser, targetUser):
        db = get_db()

        targetUserId = db.execute(
            'SELECT * FROM user WHERE username = ?', (targetUser[2],)
        ).fetchone()

        currentUserId = db.execute(
            'SELECT * FROM user WHERE username = ?', (currentUser,)
        ).fetchone()

        print(str(targetUserId['id']) + ' ' + str(currentUserId['id']))

        db.execute(
            'INSERT INTO message (author_id, sent_to_id, content) VALUES (?, ?, ?)',
            (currentUserId['id'], targetUserId['id'], msg)
        )
        db.commit()

        print('Message: ' + msg)
        send([msg, currentUser, targetUser], broadcast=True)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import chat
    app.register_blueprint(chat.bp)
    app.add_url_rule('/', endpoint='index')

    if __name__ == '__main__':
        socketio.run(app)

    return app
