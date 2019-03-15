from flask import render_template
from src import app

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/hello')
def hello_world():
    return "Hello from flask demo"