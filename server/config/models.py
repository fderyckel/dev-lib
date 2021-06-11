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
    isbn = db.Column(db.String(20), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    fee = db.Column(db.Integer, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)

    def __repr__(self) -> str:
        return str(self.isbn)


class Member(db.Model):
    """
    Model for maintaining Member records
    to reference book issues.    
    """

    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(250), nullable=False, unique=True)
    debt = db.Column(db.Integer)
    issue = db.relationship('Issues', backref='user_issued',
                            lazy=True, cascade="all, delete")

    def __repr__(self) -> db.Model:
        return str(self.user_email)
