# Importação de biblioteca 
from flask import render_template, url_for
from flask import Blueprint

# url_for ele usa o nome da função em vez do nome da rota 

# Blueprint  registra rota
main = Blueprint('main', __name__)
# Se estiver usando o blueprint no flask sempre vai ultilizar no html o nome do blueprint
# Ex: url_for('nome_do_blueprint.nome_da_funcao')

# acesso a rota chama a função 
# Quando a pessoa acessar a rota chama a função que retorna o html 
# pelo render_template
@main.route('/')
def homepage():
    return render_template('index.html')

@main.route('/nova')
def novapag():
    return 'outra view'

