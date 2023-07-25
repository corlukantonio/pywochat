from flask_sqlalchemy import SQLAlchemy

from extensions import db


class Message(db.Model):
    '''
    Message.
    '''

    __tablename__ = 'messages'
    '''
    Table name.
    '''

    id = db.Column(db.Integer, primary_key=True)
    '''
    ID.
    '''

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    '''
    Author ID.
    '''

    sent_to_id = db.Column(db.Integer, nullable=False)
    '''
    Sent to ID.
    '''

    created = db.Column(db.DateTime, nullable=False)
    '''
    Created.
    '''

    content = db.Column(db.TEXT, nullable=False)
    '''
    Content.
    '''

    def __init__(self, author_id, sent_to_id, created, content):
        '''
        Constructs a new `Message` object.
        '''

        self.author_id = author_id
        self.sent_to_id = sent_to_id
        self.created = created
        self.content = content
