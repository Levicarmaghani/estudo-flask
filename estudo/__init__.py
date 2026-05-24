# Importando estrutura Flask
from flask import Flask

# Importando extensão do banco de dados
from flask_sqlalchemy import SQLAlchemy
# Importando extensão do Migrate
from flask_migrate import Migrate

# Criando objetos de migração
db = SQLAlchemy()

# SQLAlchemy é a extensão do banco de dados, ele é um ORM (Object-Relational Mapping) que facilita a manipulação do banco de dados, ele permite criar tabelas e realizar operações de forma mais simples.

migrate = Migrate() 

# Migrate é a extensão de migração, ele é utilizado para gerenciar as mudanças no banco de dados, ele permite criar e aplicar migrações, que são arquivos que descrevem as mudanças no banco de dados 


def create_app():
    app = Flask(__name__)

    # Configuração
    # Define qual banco vai ser utilizado, nesse caso o sqlite, e o nome do arquivo do banco de dados
    # Aqui está o arquivo do banco de dados, ele vai ser criado na raiz do projeto
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Token de segurança 
    app.config['SECRET_KEY'] = 'LFNGLIREANG-OPIEANHBGA!!IN'

    # Inicializar extensões
    # Inicialização de apllicação aqui ligamos o banco db ao nosso app que é o flask
    db.init_app(app)

    #Conecta oMigrate ao app e ao banco de dados 
    migrate.init_app(app, db) # type: ignore

   

    # IMPORTANTE: importar models aqui no final
    from .models.banco import Contato
    from estudo.views.routes import main

     # Registrar rotas
    app.register_blueprint(main)

    return app


