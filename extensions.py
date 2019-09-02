import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app_factory import app

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'contacts.sqlite')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
