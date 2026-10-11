# ============================================================
# FLASK
# ============================================================

from flask import (
    render_template,
    url_for,
    request,
    redirect,
    flash
)

from flask import Blueprint


# ============================================================
# BANCO DE DADOS E MODELOS
# ============================================================

from estudo import db

from estudo.models.banco import (
    Contato,
    User,
    Post,
    PasswordReset
)


# ============================================================
# FORMULÁRIOS
# ============================================================

from estudo.forms.contato_forms import (
    ContatoForm,
    PostForm
)

from estudo.forms.auth_forms import (
    CadastroForm,
    LoginForm,
    RecuperarSenhaForm,
    RedefinirSenhaForm,
    ExcluirRegistroForm
)


# ============================================================
# EXTENSÕES
# ============================================================

from estudo import bcrypt, mail


# ============================================================
# ENVIO DE E-MAIL
# ============================================================

# Resend — envio de e-mails pela API
import resend

# Flask-Mail — ainda utilizado no projeto
from flask_mail import Message


# ============================================================
# AUTENTICAÇÃO
# ============================================================

from flask_login import (
    login_user,
    current_user,
    logout_user,
    login_required
)


# ============================================================
# TOKEN E DATA/HORA
# ============================================================

# Geração de token seguro
import secrets

# Controle de validade do token
from datetime import datetime, timedelta


# url_for ele usa o nome da função em vez do nome da rota 

# Blueprint  registra rota
main = Blueprint('main', __name__)
# Se estiver usando o blueprint no flask sempre vai ultilizar no html o nome do blueprint
# Ex: url_for('nome_do_blueprint.nome_da_funcao')

# acesso a rota chama a função 
# Quando a pessoa acessar a rota chama a função que retorna o html 
# pelo render_template

#===============================================================
#-----------------HOME-----------------------------------------
#===============================================================
@main.route('/', methods=['GET', 'POST'])
def homepage():

    # Verifica se tem usuário logado 
    if current_user.is_authenticated:
        return redirect(url_for('main.contato'))

    
    # instanciando a classe LoginForm, ou seja criando objeto
    form = LoginForm()
    
    

    # verificando se o email é valido
    if form.validate_on_submit():
        usuario = form.autenticar()

        if usuario:
            login_user(usuario, remember=False)
            return redirect(url_for('main.contato'))

        flash ("E-mail ou senha incorretos", 'danger')

       
    # Variável para mandar para o index.htm 
    usuario = "Levi" 
    idade = 31
    

    # Outra froma de passar informação e com um dicionario utilizando o context
    context = {
        'usuario': usuario,
        'idade' : idade
    }
    return render_template('login.html', usuario=usuario, idade=idade, context=context, form=form)


#============================================================================
#------------------CADASTRO USUÁRIO------------------------------------------
#============================================================================
@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro_usuario():
    form = CadastroForm()
    
    if form.validate_on_submit():
        form.save()

        flash("Cadastro efetuado com sucesso!", 'success')
        return redirect(url_for('main.homepage'))
    
    return render_template('cadastro_usuario.html', form=form)


       

#======================================================================
#------------Rota métado para salva no banco de dados -----------------
#=======================================================================
@main.route('/contato', methods=['GET', 'POST'])
@login_required # função de proteção das rotas 
def contato ():
    
    form = ContatoForm()
    context = {}
    print(current_user.is_authenticated)
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('main.contato_lista'))
    return render_template('contato.html', context=context, form=form)

#=================================================================
#------------------------LOGOUT-----------------------------------
#=================================================================
# Essa rota remove o id do usuário
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("main.homepage"))


#=====================================================================
#-----------------------ROTA PARA NOVO POST-------------------------
#=====================================================================
@main.route('/post/novo',methods=['Get', 'Post'])
@login_required
def PostNovo():
    form = PostForm()

    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('main.homepage'))
    return render_template('post_novo.html', form=form)




#=====================================================================
#-----------------------ROTA PARA VER A LISTA-------------------------
#=====================================================================
@main.route('/contatoLista')
@login_required
def contato_lista():

    pesquisa = request.args.get('pesquisa', '')
    dados = Contato.query.filter_by(user_id=current_user.id)         
    
    if pesquisa != '':
        dados = dados.filter(Contato.nome.contains(pesquisa))
  

    context = dados.all()
        
        
    return render_template('contato_lista.html',
                        context = context,
                        pesquisa = pesquisa)


#===============Rota de Mensagem=========================
@main.route("/post/ver")
@login_required
def post_lista():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('post_lista.html', posts=posts)

@main.route("/ver-mensagem/<int:id>")
@login_required
def ver_mensagem(id):
    mensagem = Contato.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    return render_template('ver_mensagem.html', mensagem=mensagem)


#==========================================================
#------------------------ESQUECI SENHA----------------------
#===========================================================
@main.route("/esqueci_senha", methods=['GET', 'POST'])
def esqueci_senha():
    form = RecuperarSenhaForm()

    # O Formulário foi enviado e passou todas as validações
    if form.validate_on_submit():

        # Buscar no banco o email digitado, 
        usuario = User.query.filter_by(email=form.email.data).first()
        # Se existir usuario com email do banco 
        if usuario:
            # Código secreto aleatório para recuperação de senha
            token = secrets.token_urlsafe(32)
            # Pega horário atual e adiciona 15 minutos
            expiracao = datetime.utcnow() + timedelta(minutes=15)

            #Criando objeto da Classe (PasswordReset)
            reset = PasswordReset(
                token = token,
                expiracao = expiracao,
                # Pegando o ID do usuário que foi encontrado pelo e-mail digitado no formulário
                user_id = usuario.id
            )
            db.session.add(reset)
            db.session.commit()


            # Cria link de recuperação de senha, será o link enviado pelo email 
            #'main.recuperar_senha"= rota que receberá o token
            # token=token envia o token pela URL, no email, depois pegamos esse token como no link e colocamos como parametro na função
            # _external=True = gera a UTL completa
            link = url_for("main.recuperar_senha",  token=token, _external=True)

            # Envia o e-mail através do Resend
           # RESEMD = serviços de envio de e-mail na nuvem
           # O Flask envia os dados pela API e o Resend realiza o envio 
            resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": usuario.email,
                "subject": "Recuperação de senha",
                "html": f"""
                    <h2>Recuperação de senha</h2>

                    <p>Clique no botão abaixo para redefinir sua senha:</p>

                    <a href="{link}">
                        Redefinir minha senha
                    </a>

                    <p>Este link é válido por 15 minutos.</p>
                """
            })
            return redirect(url_for("main.email_enviado"))
            
        
    return render_template("esqueci_senha.html", form=form)

@main.route("/email_enviado")
def email_enviado():
    return render_template("email_enviado.html")

#-------------------------------------------------------------------
#============================Recuperar senha========================
#---------------------------------------------------------------------
# O token recebido pela URL é passado como parâmetro para a função
@main.route("/recuperar_senha/<token>", methods=['GET', 'POST'])
def recuperar_senha(token):

    # Busca o token no banco igual ao token que no parametro da função 
    reset = PasswordReset.query.filter_by(token=token).first()

    # Verifica se o token existe
    if not reset:
        return "Token inválido"

    # Verifica se o token já foi utilizado
    if reset.usado:
        return "Este token já foi utilizado"

    # Verifica se o token expirou
    if datetime.utcnow() > reset.expiracao:
        return "Este token expirou"

    # Cria o formulário
    form = RedefinirSenhaForm()

    # Verifica se o formulário foi enviado e é válido
    if form.validate_on_submit():

        # Busca o usuário relacionado ao token
        usuario = User.query.get(reset.user_id)

        # Cria um novo hash para a nova senha
        usuario.senha = bcrypt.generate_password_hash(
            form.senha.data
        ).decode("utf-8")

        # Marca o token como utilizado
        reset.usado = True

        # Salva as alterações no banco
        db.session.commit()

        # Volta para o login
        return redirect(url_for("main.homepage"))

    return render_template(
        "redefinir_senha.html",
        form=form
    )

@main.route("/teste_email")
def teste_email():

    mensagem = Message(
        subject="Teste de envio",
        sender="seuemail@outlook.com",
        recipients=["seuemail@outlook.com"]
    )

    mensagem.body = "Este é um teste de envio pelo Flask."

    mail.send(mensagem)

    return "E-mail enviado com sucesso!"



#-------------------------------------------------------------------
#============================EXCLUIR REGISTRO========================
#--------------------------------------------------------------------
@main.route("/excluir_contato/<int:id>")
@login_required
def excluir_contato(id):

    contato = Contato.query.get_or_404(id)

    db.session.delete(contato)
    db.session.commit()

    flash("Contato excluído com sucesso!", "success")

    return redirect(url_for("main.contato_lista"))

    
        
    













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


