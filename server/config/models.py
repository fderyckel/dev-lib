from config import db
from datetime import datetime

class Admin(db.Model):
    """
    Model for admins (lib inchange)
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return str(self.email)


class Issues(db.Model):
    """
    Model for issues 
    instance only created when a book is issued
    """

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(250), nullable=False, unique=True)
    book_name = db.Column(db.String(30), nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.Integer, nullable=False)
    debt = db.Column(db.Integer)
    issue_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return str(self.user_email)
