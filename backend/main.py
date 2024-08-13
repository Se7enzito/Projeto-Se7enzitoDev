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
    email = session.get('email')
    
    if email == None:
        return redirect(url_for('login'))
    
    dados = gerenData.getUserInfos(email)
    
    user = gerenData.getUser(email)
    
    notificacoes = gerenData.getNotificacoes(user)
    aulas = gerenData.getAulas(user)
    propostas  = gerenData.getPropostas(user)
    
    return render_template('dashboard.html', user=dados[0], perm=dados[3], notificacoes=notificacoes, aulas=aulas, propostas=propostas)

@app.route('/marcar_aula')
def marcar_aula():
    email = session.get('email')
    
    if email == None:
        return redirect(url_for('login'))
    
    pass

@app.route('/aulas_anteriores')
def aulas_anteriores():
    email = session.get('email')
    
    if email == None:
        return redirect(url_for('login'))
    
    pass

@app.route('/acesso')
def acesso():
    email = session.get('email')
    
    if email == None:
        return redirect(url_for('login'))
    
    pass

@app.route('/contratar')
def contratar():
    email = session.get('email')
    
    if email == None:
        return redirect(url_for('login'))
    
    pass

@app.route('/gerenciamento')
def gerenciamento():
    email = session.get('email')
    
    if email == 'Se7enzitoDev':
        dados = gerenData.getUserInfos(email)
        
        return render_template('gerenciamento.html', user=dados[0])
    
    return redirect(url_for('index'))

@app.route('/servicos')
def servicos():
    pass

@app.route('/servicos/<int:id>')
def servicos(id):
    servico = gerenData.getServicoId(id)
    
    if servico is None:
        return f"Serviço com ID {id} não encontrado.", 404
    
    # Fazer configuração do site
    return f'Serviço de ID {id}'

@app.route('/portfolio')
def portfolio():
    pass

if __name__ == '__main__':    
    ensure_key_exists()
    key = load_key()
    
    gerenData.criarTabelas()
    
    app.run(debug=True, port=8000)