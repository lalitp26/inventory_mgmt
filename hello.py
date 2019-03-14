from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/hello')
def hello_world():
    return "Hello from flask demo"

if __name__ == '__main__':
    app.run(debug = True)

