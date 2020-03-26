import os

from flask import Flask
from flask_socketio import SocketIO, send


app = Flask(__name__)
socketio = SocketIO(app)


# Get the "app" variable
def get_app():
    return app


# Register blueprints
def register_blueprints():
    import auth
    app.register_blueprint(auth.bp)

    import chat
    app.register_blueprint(chat.bp)
    app.add_url_rule('/', endpoint='index')


def init_socketio_actions():
    from db import get_db

    @socketio.on('add_new_contact')
    def add_new_contact(*json):
        db = get_db()

        db.session.execute(
            'INSERT INTO contacts (user_1, user_2) VALUES (:user_1, user_2)',
            {
                'user_1': json[1][2],
                'user_2': json[0]
            }
        )
        db.session.commit()

        db.session.execute(
            'INSERT INTO contacts (user_1, user_2) VALUES (:user_1, user_2)',
            {
                'user_1': json[0],
                'user_2': json[1][2]
            }
        )

    @socketio.on('choose_contact')
    def choose_contact(*json):
        pass

    @socketio.on('message')
    def handle_message(msg, currentUser, targetUser):
        db = get_db()

        targetUserId = db.session.execute(
            'SELECT * FROM users WHERE username = :username', {'username': targetUser[2]}).fetchone()

        print('Target user: ' + msg)

        currentUserId = db.session.execute(
            'SELECT * FROM users WHERE username = :username',
            {'username': currentUser}
        ).fetchone()

        print(str(targetUserId['id']) + ' ' + str(currentUserId['id']))

        db.session.execute(
            'INSERT INTO messages (author_id, sent_to_id, content) VALUES (:author_id, :sent_to_id, :content)',
            {
                'author_id': currentUserId['id'],
                'sent_to_id': targetUserId['id'],
                'content': msg
            }
        )
        db.session.commit()

        print('Message: ' + msg)

        send([msg, currentUser, targetUser], broadcast=True)


if __name__ == '__main__':
    register_blueprints()
    init_socketio_actions()

    socketio.run(app)
