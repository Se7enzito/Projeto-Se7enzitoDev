from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_session import Session

app = Flask(__name__, template_folder="../frontend/templates")

app.static_folder = '../frontend/src'
app.static_url_path = '/static'

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    return render_template('index.html', idade = 17)
    
# Código com gambiarra, depois olhar
@app.route('/login', methods = ['POST', 'GET'])
def login():
    user = session.get('user')
    senha = session.get('senha')
    
    if user == None or senha == None:
        return render_template('login.html')
    
    return render_template('dashboard.html', user=user)

@app.route('/entrar', methods = ['POST'])
def entrar():
    if request.method == 'POST':
        formEmail = request.form.get('email')
        formPass = request.form.get('password')
        
        # Gambiarra
        if formEmail == None or formPass == None or formEmail == "" or formPass == "":
            return redirect(url_for('login'))
        
        # Fazer validações
        return redirect(url_for('dashboard'))

@app.route('/registrar', methods = ['POST'])
def registrar():
    if request.method == 'POST':
        formUser = request.form.get('user')
        formEmail = request.form.get('email')
        formPass = request.form.get('password')
        
        # Fazer validações
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('senha', None)
    
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    
    if user == None:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', user=user)

@app.route('/contratar')
def contratar():
    user = session.get('user')
    
    if user == None:
        pass
    
    pass

@app.route('/saber_mais')
def saber_mais():
    user = session.get('user')
    
    if user == None:
        pass
    
    pass

@app.route('/gerenciamento')
def gerenciamento():
    user = session.get('user')
    
    if user == 'Se7enzitoDev':
        return render_template('gerenciamento.html', user=user)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)