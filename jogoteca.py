from flask import Flask, url_for,flash, session, redirect, render_template, request
class jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = jogo('lol','MOBA','Online')
jogo2 = jogo('COD','Tiro','Playstation')
jogo3 = jogo('free fire','tiro','smartphone')
lista = [jogo1,jogo2,jogo3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Gustavo Tocantins', 'Guga', 'gustavo')
usuario2 = Usuario('Paulo Viegas', 'pirigueti','paulo')
usuario3 = Usuario('Fabio Ferreiria', 'fabiola','fabio') 
usuarios = {usuario1.nickname:usuario1,
            usuario2.nickname:usuario2,
            usuario3.nickname:usuario3}

app = Flask(__name__)
app.secret_key = 'Gustavo'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado']== None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria  = request.form['categoria']
    console = request.form['console']

    jogoa = jogo(nome,categoria, console)
    lista.append(jogoa)

    return redirect('/')

@app.route('/login')
def login():
    proxima = request.args.get('proxima') 
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' Logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuario não logado!')
        return redirect(url_for('login'))
        
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))
    
app.run(debug=True)