from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '#E23DSSD$%$FDvdfsd#23S$#SF'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


from . import routing
from . import models