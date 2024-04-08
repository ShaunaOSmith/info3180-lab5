from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_wtf.csrf import CSRFProtect 

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lab5_user:lab5@localhost:5432/lab5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views
from app import models