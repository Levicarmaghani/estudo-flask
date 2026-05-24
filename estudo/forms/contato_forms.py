# Usando biblioteca wtf para formulário
from flask_wtf import FlaskForm
# tudo que for trabalha nesse arquivo EX: TEXTO, NÚMEROS, precisa importa
from wtforms import StringField, SubmitField
#Para campo ser preenchido obrigatoriamente
from wtforms.validators import DataRequired, Email

from  estudo import db
from estudo.models.banco import Contato

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(),])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = StringField('Mensagem')
    btnSubmit = SubmitField("Enviar", validators=[DataRequired()])

    def save(self):
        contato = Contato(
            nome = self.nome.data,
            email = self.email.data,
            assunto = self.assunto.data,
            mensagem = self.mensagem.data
        )

        db.session.add(contato)
        db.session.commit()

"""
self o form inteiro
self.nome campo nome
.data valor digitado nele
"""




    