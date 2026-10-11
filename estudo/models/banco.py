from estudo import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# Função para informar qual o usuário que sera retornado, que está logado
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Classe usuário cadastro
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String, nullable = True)
    sobrenome = db.Column(db.String, nullable = True)
    email = db.Column(db.String, unique=True, nullable = True)
    senha = db.Column(db.String, nullable = True) 

    # Um usuário pode ter  varios post(registro)
    posts = db.relationship('Post', backref='user', lazy=True)

# classe contato
class Contato(db.Model):

    # Atributos
    id = db.Column(db.Integer, primary_key=True)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    nome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    assunto = db.Column(db.String, nullable=True)
    mensagem = db.Column(db.Text, nullable=True)
    respondido = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Relação de tabela com a tabela User 
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    mensagem = db.Column(db.String, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def msg_resumo(self):
        return f"{self.mensagem[:20]}..."

# Tabela para recuperação de senha
class PasswordReset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False, unique=True)
    expiracao = db.Column(db.DateTime, nullable=False)
    usado = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

"""
nullable = True
pode ser null(vazio no banco)
não é obrigatório

nullable = False
não pode ser NULL
é obrigatorio preencher
"""

