from config import db 

class Test(db.Model):
    name = db.Column(db.String(10))

    