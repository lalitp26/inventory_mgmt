from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '#E23DSSD$%$FDvdfsd#23S$#SF'

from . import routing