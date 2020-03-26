import datetime
import os

from flask import Flask
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from flask_jsglue import JSGlue


app = Flask(__name__)
socketio = SocketIO(app)
JSGlue(app)

app.config.from_mapping(SECRET_KEY='dev')

# If running on localhost set this to 'dev'
ENV = 'dev'

# Connect to the database
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/pywochat'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database handler
db = SQLAlchemy(app)


# Model for "users" table
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(30), unique=True, nullable=False)
    password = db.Column(db.VARCHAR(94), nullable=False)
    firstname = db.Column(db.VARCHAR(30), nullable=False)
    lastname = db.Column(db.VARCHAR(30), nullable=False)

    child = db.relationship("Message", uselist=False, back_populates="parent")

    def __init__(self, username, password, firstname, lastname):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname


# Model for "contacts" table
class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    user_1 = db.Column(db.VARCHAR(30), nullable=False)
    user_2 = db.Column(db.VARCHAR(30), nullable=False)

    def __init__(self, user_1, user_2):
        self.user_1 = user_1
        self.user_2 = user_2


# Model for "messages" table
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    sent_to_id = db.Column(db.Integer, nullable=False)
    created = db.Column(
        db.DateTime,
        nullable=False)
    content = db.Column(db.TEXT, nullable=False)

    def __init__(self, author_id, sent_to_id, created, content):
        self.author_id = author_id
        self.sent_to_id = sent_to_id
        self.created = created
        self.content = content


# Get the "app" var
def get_app():
    return app


# Get the "db" var
def get_db():
    return db


# Import modules and register blueprints
def register_blueprints():
    import auth
    app.register_blueprint(auth.bp)

    import chat
    app.register_blueprint(chat.bp)
    app.add_url_rule('/', endpoint='index')


# Init SocketIO actions
def init_socketio_actions():
    @socketio.on('add_new_contact')
    def add_new_contact(*json):
        db = get_db()

        db.session.execute(
            "INSERT INTO contacts (user_1, user_2) VALUES (:user_1, :user_2)",
            {
                'user_1': json[1][2],
                'user_2': json[0]
            }
        )
        db.session.commit()

        db.session.execute(
            "INSERT INTO contacts (user_1, user_2) VALUES (:user_1, :user_2)",
            {
                'user_1': json[0],
                'user_2': json[1][2]
            }
        )
        db.session.commit()

    @socketio.on('choose_contact')
    def choose_contact(*json):
        pass

    @socketio.on('message')
    def handle_message(msg, currentUser, targetUser):
        db = get_db()

        targetUserId = db.session.execute(
            "SELECT * FROM users WHERE username = :username",
            {'username': targetUser[2]}
        ).fetchone()

        print('Target user: ' + msg)

        currentUserId = db.session.execute(
            "SELECT * FROM users WHERE username = :username",
            {'username': currentUser}
        ).fetchone()

        print(str(targetUserId['id']) + ' ' + str(currentUserId['id']))

        db.session.execute(
            "INSERT INTO messages (author_id, sent_to_id, created, content) VALUES (:author_id, :sent_to_id, :created, :content)",
            {
                'author_id': currentUserId['id'],
                'sent_to_id': targetUserId['id'],
                'created': datetime.datetime.utcnow(),
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
