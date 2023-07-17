from flask_sqlalchemy import SQLAlchemy

from app import get_db
from extensions import db

db: SQLAlchemy = get_db()


class User(db.Model):
    '''
    User.
    '''

    __tablename__ = 'users'
    '''
    Table name.
    '''

    id = db.Column(db.Integer, primary_key=True)
    '''
    ID.
    '''

    username = db.Column(db.VARCHAR(30), unique=True, nullable=False)
    '''
    Username.
    '''

    password = db.Column(db.VARCHAR(94), nullable=False)
    '''
    Password.
    '''

    firstname = db.Column(db.VARCHAR(30), nullable=False)
    '''
    Firstname.
    '''

    lastname = db.Column(db.VARCHAR(30), nullable=False)
    '''
    Lastname.
    '''

    child = db.relationship("Message", uselist=False, back_populates="parent")
    '''
    Child.
    '''

    def __init__(self, username, password, firstname, lastname):
        '''
        Constructs a new `User` object.
        '''

        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
