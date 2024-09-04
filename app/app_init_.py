# from database.skima.createSQL import Book, Song, Author, PublishURL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the app
app = Flask(__name__, template_folder="pages/templates",static_folder="pages/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/onpuscores.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

per_page = 30

import rootes