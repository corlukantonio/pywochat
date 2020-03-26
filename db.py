import datetime

from flask_sqlalchemy import SQLAlchemy

from app import get_app


app = get_app()

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
    password = db.Column(db.VARCHAR(30), nullable=False)
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
        default=datetime.datetime.utcnow,
        nullable=False)
    content = db.Column(db.TEXT, nullable=False)

    def __init__(self, author_id, sent_to_id, content):
        self.author_id = author_id
        self.sent_to_id = sent_to_id
        self.content = content


# Get the "db" variable
def get_db():
    return db
