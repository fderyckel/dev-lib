from flask import Flask
from .routing import Login
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os

load_dotenv()


app = Flask(__name__)
app.secret_key = [os.getenv('SECRET_KEY')]
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
app.add_url_rule('/', view_func=Login.as_view(name='login',
                 template_name='login.html'))
