# Importando estrutura Flask
from flask import Flask

#Importando a plataforma resend
import resend

# Importando Flask-Mail
from flask_mail import Mail

# Importando extensão do banco de dados
from flask_sqlalchemy import SQLAlchemy

# Importando extensão do Migrate
from flask_migrate import Migrate

# Bilioteca sigiliosa
from flask_login import LoginManager
from dotenv import load_dotenv

#Biblioteca para buscar arquivos de ambientes
import os


# Biblioteca de login
from flask_bcrypt import Bcrypt




# Carregar variaveis de ambiente que estão dentro do arquivo .env
load_dotenv('.env')

#Reuperando chave secreta do .env
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
# configurando a API do Resend
resend.api_key = RESEND_API_KEY

# teste
def enviar_email_teste():
    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": "leviagustinho@outlook.com",
        "subject": "Teste do meu sistema flask",
        "html": "<h1>Funcionou!</h1><p>Este é um teste Resend.</p>"
    })


# Criando objetos de migração
db = SQLAlchemy()

# SQLAlchemy é a extensão do banco de dados, ele é um ORM (Object-Relational Mapping) que facilita a manipulação do banco de dados, ele permite criar tabelas e realizar operações de forma mais simples.

migrate = Migrate() 

# Migrate é a extensão de migração, ele é utilizado para gerenciar as mudanças no banco de dados, ele permite criar e aplicar migrações, que são arquivos que descrevem as mudanças no banco de dados 


# Vamos instanciar minha classe ou criar um objeto da classe
login_manager = LoginManager()
login_manager.login_view = 'login'
bcrypt = Bcrypt()
mail = Mail()




def create_app():
    app = Flask(__name__)

    @app.route("/teste-email")
    def teste_email():
        enviar_email_teste()
        return "E-mail enviado"

    # Configuração
    # Define qual banco vai ser utilizado, nesse caso o sqlite, e o nome do arquivo do banco de dados
    # Aqui está o arquivo do banco de dados, ele vai ser criado na raiz do projeto
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Token de segurança 
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    #================================================================================
    #============================CONFIG E-MAIL========================================
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT']  = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    # Inicializar extensões
    # Inicialização de apllicação aqui ligamos o banco db ao nosso app que é o flask
    db.init_app(app)

    #Conecta oMigrate ao app e ao banco de dados 
    migrate.init_app(app, db) # type: ignore

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    bcrypt.init_app(app)
    mail.init_app(app)







 
   

    # IMPORTANTE: importar models aqui no final
    from .models.banco import Contato, User
    from estudo.views.routes import main

     # Registrar rotas
    app.register_blueprint(main)

    return app


