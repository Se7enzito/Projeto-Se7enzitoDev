from flask import Flask, render_template, redirect, url_for, session, request
from flask_session import Session
from libs.db.dbAPI import GerenData
from libs.funcs.systemCripto import ensure_key_exists, load_key

app = Flask(__name__, template_folder="../frontend/templates")

app.static_folder = '../frontend/src'
app.static_url_path = '/static'

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

gerenData = GerenData()

@app.route('/')
def index():
    return render_template('index.html', idade = 17)
    
@app.route('/login', methods = ['POST', 'GET'])
def login():
    email = session.get('email')
    senha = session.get('senha')
    
    if email == None or senha == None:
        return render_template('login.html')
    
    dados = gerenData.getUserInfos(email)
    
    return render_template('dashboard.html', user=dados[0])

@app.route('/entrar', methods = ['POST'])
def entrar():
    if request.method == 'POST':
        formEmail = request.form.get('email')
        formPass = request.form.get('password')
        
        if formEmail == None or formPass == None or formEmail == "" or formPass == "":
            return redirect(url_for('login'))
        
        loginOk = gerenData.confirmLogin(formEmail, formPass)
        
        session['email'] = formEmail
        session['senha'] = formPass
        
        if loginOk:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))

@app.route('/registrar', methods = ['POST'])
def registrar():
    if request.method == 'POST':
        formUser = request.form.get('user')
        formEmail = request.form.get('email')
        formPass = request.form.get('password')
        
        if formUser == None or formEmail == None or formPass == None or formEmail == "" or formUser == "" or formPass == "":
            return redirect(url_for('login'))
        
        retorno = gerenData.criarUser(formUser, formEmail, formUser)
        
        session['email'] = formEmail
        session['senha'] = formPass
        
        if retorno == "Utilizador criado com sucesso.":
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))

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

@app.route('/marcar_aula')
def marcar_aula():
    user = session.get('user')
    
    if user == None:
        pass
    
    pass

@app.route('/aulas_anteriores')
def aulas_anteriores():
    user = session.get('user')
    
    if user == None:
        pass
    
    pass

@app.route('/acesso')
def acesso():
    user = session.get('user')
    
    if user == None:
        pass
    
    pass

@app.route('/contratar')
def contratar():
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
    ensure_key_exists()
    key = load_key()
    
    gerenData.criarTabelas()
    
    app.run(debug=True, port=8000)