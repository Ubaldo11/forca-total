import sqlite3
import hashlib

# ===== CONEXÃO =====
conexao = sqlite3.connect('meu_banco.db', check_same_thread=False)
conexao.row_factory = sqlite3.Row
cursor = conexao.cursor()

# ===== CRIAR TABELA =====
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
''')
conexao.commit()

# ===== FUNÇÃO PARA CRIPTOGRAFAR =====
def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# ===== ADICIONAR USUÁRIO =====
def adicionar_usuario(nome, email, senha):
    senha_hash = criptografar_senha(senha)
    
    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha_hash)
        )
        conexao.commit()
        print(" Usuário cadastrado!")
        return True
    except sqlite3.IntegrityError:
        print(" Email já cadastrado!")
        return False

# ===== CONSULTAR USUÁRIO (LOGIN) =====
def consultar_usuario(email, senha):
    senha_hash = criptografar_senha(senha)
    
    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
        (email, senha_hash)
    )
    resultado = cursor.fetchone()
    
    if resultado:
        print(" Bem-vindo!")
        return resultado
    else:
        print(" Email ou senha inválidos!")
        return None

# ===== CONSULTAR SE EXISTE =====
def consultar_existe(email):
    cursor.execute(
        "SELECT email FROM usuarios WHERE email = ?", (email,)
    )
    existe = cursor.fetchone()
    if existe == None:
        return False
    else:
        return True