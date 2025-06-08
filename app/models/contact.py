from ..extensions import db


class Contact(db.Model):
    '''
    Contact.
    '''

    __tablename__ = 'contacts'
    '''
    Table name.
    '''

    id = db.Column(db.Integer, primary_key=True)
    '''
    ID.
    '''

    user_1 = db.Column(db.VARCHAR(30), nullable=False)
    '''
    User 1.
    '''

    user_2 = db.Column(db.VARCHAR(30), nullable=False)
    '''
    User 2.
    '''

    def __init__(self, user_1, user_2):
        '''
        Constructs a new `Contact` object.
        '''

        self.user_1 = user_1
        self.user_2 = user_2
