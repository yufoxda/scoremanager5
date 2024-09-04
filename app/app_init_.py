import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Database.Schema.schema import Book,Song,Lyricist,SongWriter,Arranger
from Database.Schema.schema import SongLyricistAssociation,SongWriterAssociation,SongArrangerAssociation

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the app
app = Flask(__name__, template_folder="../Pages/Templates",static_folder="../Pages/Static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database/ompuscores.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

per_page = 30

import rootes.rootes