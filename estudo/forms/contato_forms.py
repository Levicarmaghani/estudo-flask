# Usando biblioteca wtf para formulário
from flask_wtf import FlaskForm

# tudo que for trabalha nesse arquivo EX: TEXTO, NÚMEROS, precisa importa
# Senha
from wtforms import StringField, SubmitField, PasswordField, TextAreaField



#Para campo ser preenchido obrigatoriamente, validação de senha
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import current_user

# Para validação de email
from wtforms import ValidationError


from  estudo import db, bcrypt
from estudo.models.banco import Contato, User, Post

#====================Classe Formulário ======================================
class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(),])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = TextAreaField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField("Enviar", validators=[DataRequired()])

    def save(self):
        contato = Contato(
            nome = self.nome.data,
            email = self.email.data,
            assunto = self.assunto.data,
            mensagem = self.mensagem.data,

            #Pegamos o usuario logado e salvamos o id dele no banco 
            user_id = current_user.id
        )

        db.session.add(contato)
        db.session.commit()

"""
self o form inteiro
self.nome campo nome
.data valor digitado nele
"""
class PostForm(FlaskForm):
    mensagem = StringField('Mensagem', validators=[DataRequired() ])
    btnSubmit = SubmitField('enviar')

    def save(self, user_id):
        post = Post(
            Mensagem = self.mensagem.data,
            user_id = user_id
        )

        db.session.add(post)
        db.session.commit()
        



    