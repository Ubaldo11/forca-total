from flask import Flask, request, jsonify, render_template, url_for, redirect, session
from banco_de_dados import adicionar_usuario, consultar_usuario, consultar_existe
from Apis.treino import gerar_treino
from Apis.formatar import formatar_exercicios
from functools import wraps
from Apis.loc import localizacao_por_ip, buscar_academias
import os
from Apis.musica import buscar_videos_playlist

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "AIzaSyAP-X-T1VqmJ5m1kafvDWZnOSgAKXrHQB0")
PLAYLIST_ID = "PLgc4Fs1GgMArRtsmuBRGhO1D_UFkLS3fV"

app = Flask(__name__)

app.secret_key = 'chave_super_secreta_123'

def login_obrigatorio(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    # session está disponível em todas as rotas
    if 'usuario_id' in session:
        return render_template('index.html', logado=True, nome=session['usuario_nome'])
    return render_template('index.html', logado=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = consultar_usuario(email, senha)
        
        if usuario:
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro='Email ou senha inválidos')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if consultar_existe(email) == False:
            adicionar_usuario(nome, email, senha)
            return redirect(url_for('login'))   
        else:
            return render_template('cadastro.html', erro='Email já cadastrado')  
    
    return render_template('cadastro.html') 

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/treino', methods=['GET'])
@login_obrigatorio
def treino():
    return render_template('treino.html')


@app.route('/exercicios', methods=['POST'])
@login_obrigatorio
def exercicios():
    grupo = request.form.get('grupo_muscular')
    lista = []

    if grupo:
        dados = gerar_treino(grupo)
        lista = formatar_exercicios(dados)

    return render_template('exercicios.html', exercicios=lista, grupo=grupo)

@app.route('/loc', methods=['GET', 'POST'])
@login_obrigatorio
def loc():
    if request.method == 'POST':
        dados = request.get_json() or {}
        lat = dados.get('latitude')
        lon = dados.get('longitude')
        
        if lat and lon:
            lista = buscar_academias(lat, lon, raio_metros=5000)
            if not lista:
                return jsonify({'erro': 'Nenhuma academia encontrada na sua região.'}), 404
            
            return jsonify({'academias': lista})
        
        return jsonify({'erro': 'Coordenadas não recebidas corretamente.'}), 400

    # Requisição GET: apenas carrega a estrutura HTML da página
    return render_template('academias.html')

@app.route('/musica')
@login_obrigatorio
def musica():
    videos, erro = buscar_videos_playlist(PLAYLIST_ID, YOUTUBE_API_KEY)
    return render_template("musica.html", videos=videos or [], erro=erro)


if __name__ == '__main__':
    app.run(debug=True)
