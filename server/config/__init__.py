from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

load_dotenv()


app = Flask(__name__)
app.secret_key = [os.getenv('SECRET_KEY')]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite3'
db = SQLAlchemy(app)

from .routing import Login

app.add_url_rule('/', view_func=Login.as_view(name='login',
                 template_name='login.html'))