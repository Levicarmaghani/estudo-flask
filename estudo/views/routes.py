# Importação de biblioteca 
from estudo.models.banco import db, Contato
from flask import render_template, url_for, request, redirect
from flask import Blueprint
from estudo.forms.contato_forms import ContatoForm

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

    # Variável para mandar para o index.htm 
    usuario = "Levi" 
    idade = 31

    # Outra froma de passar informação e com um dicionario utilizando o context

    context = {

        'usuario': usuario,
        'idade' : idade
    }
    return render_template('index.html', usuario=usuario, idade=idade, context=context)

# Rota métado para salva no banco de dados 
@main.route('/contato', methods=['GET', 'POST'])
def contato ():
    
    form = ContatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('main.homepage'))
    return render_template('contato.html', context=context, form=form)

# Rotas para listas
@main.route('/contatoLista')
def contato_lista():
    
    context = {}
    pesquisa = request.args.get('pesquisa', '')
    dados = Contato.query.order_by(Contato.nome)

    if pesquisa != '':
        dados = dados.filter_by(nome=pesquisa)
        context = dados.all()
        
    return render_template('contato_lista.html',
                        context = context,
                        pesquisa = pesquisa)













#------------------------=======================------------------------------------------
#------------------------FORMATO ANTIGO========-------------------------------------------
#-----------------------=========================----------------------------------------
# Método post é uma segurança melhor 
# Pagina do formulário para salva no banco de dados
@main.route('/contato_old', methods=['GET', 'POST']) 
def contato_old():
    # Dicionaro vazio
    context = {}
    if request.method == "GET":
        pesquisa = request.args.get('pesquisa')
        # Adiconando coisa uma chave e um valor 
    if request.method == 'POST':
        nome =  request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        contato = Contato(
            nome=nome,
            email=email,
            assunto=assunto,
            mensagem=mensagem
        )
        db.session.add(contato)
        db.session.commit()
        return redirect(url_for("main.suce"))
    # lembrando context do lado da esquerda nome que será enviado para o html
    # context do lado diretio variável python que existe na sua route
    return render_template("contato_old.html", context=context)


