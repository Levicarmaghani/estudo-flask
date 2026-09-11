from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
    Length
)

from estudo import bcrypt, db
from estudo.models import User


#================== Classe Cadastro =======================================
class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired() ])
    sobrenome = StringField('Sobrenome', validators=[DataRequired() ])
    email = StringField('E-Mail', validators=[DataRequired(), Email() ])
    senha = PasswordField("Senha", validators=[DataRequired() ])
    confirmacao_senha = PasswordField('Senha', validators=[DataRequired(), EqualTo('senha') ])
    btnSubmit = SubmitField('Cadastrar')

    def validate_email(self, email):
        usuario = User.query.filter_by(email=email.data).first()

        if usuario:
            raise ValidationError(
                "Este e-mail já possui cadastro."
            )
    
    def save(self):
        senha_hash = bcrypt.generate_password_hash(self.senha.data).decode('utf-8')
        user = User(
            nome = self.nome.data,
            sobrenome = self.sobrenome.data,
            email = self.email.data,
            senha = senha_hash
        )

        db.session.add(user)
        db.session.commit()
        return user



#-------------------------Classe Login------------------------------
class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

    def autenticar(self):
        usuario = User.query.filter_by(email=self.email.data).first()

        if not usuario:
            return None

        # usuário.senha     hash vindo do banco
        # self.senha.data senha digitada
        if not bcrypt.check_password_hash(usuario.senha, self.senha.data):
            return None

        return usuario

#======================================================================================
#==============================RECUPERAÇÃO DE SENHA===================================
#======================================================================================

class RecuperarSenhaForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Recuperar Senha')

#======================================================================================
#==============================REDEFINIÇÃO DE SENHA ===================================
#======================================================================================
class RedefinirSenhaForm(FlaskForm):
    senha = PasswordField("Nova Senha", validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField("Confirmar Senha", validators=[DataRequired(),EqualTo("senha", message="As senha precisam ser iguais.")])
    submit = SubmitField("Redefinir senha")



