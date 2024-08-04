from flask import Flask, render_template
from flask_session import Session

app = Flask(__name__, template_folder="../frontend/templates")

app.static_folder = '../frontend/src'
app.static_url_path = '/static'

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/entrar')
def entrar():
    pass

@app.route('/logout')
def logout():
    pass

@app.route('/dashboard')
def cadastro():
    pass

@app.route('/login')
def login():
    pass

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)