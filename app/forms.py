from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, IntegerField, BooleanField,
     SubmitField,TextAreaField,FloatField)
from wtforms.validators import InputRequired, Length, EqualTo, Email,NumberRange


ERROS = {
'requerido':'Campo obrigatório. Por favor, preencha.',
'quant_caracter_usuario':'Quantidade de caracteres inválido. Por favor, tente outro nome de usuário.',
'email':'Formato de e-mail inválido. Por favor, tente novamente.',
'senhas_iguais':'A confirmação de senha deve ser igual a senha. Por favor tente novamente.',
'range_numeros':'Você só pode dar uma nota entre 0 e 10. Por favor, tente outro número'
}

class CadastroUsuarioForm(FlaskForm):
    nome_completo = StringField("nome completo", validators=[InputRequired(message=ERROS['requerido'])])
    nome_usuario = StringField("nome de usuário", validators=[Length(min=1,max=20,message=ERROS['quant_caracter_usuario']),
        InputRequired(message=ERROS['requerido'])])
    senha = PasswordField("Senha", validators=[InputRequired(message=ERROS['requerido'])])
    confirmacao_senha = PasswordField("Digite a Senha novamente", validators=[InputRequired(message=ERROS['requerido']),
        EqualTo('senha',message=ERROS['senhas_iguais'])])
    email = StringField("email", validators=[Email(message=ERROS['email']),
        InputRequired(message=ERROS['requerido'])])
    cpf = StringField("cpf", validators=[InputRequired(message=ERROS['requerido'])])
    enviar = SubmitField("enviar")

class LoginUsuarioForm(FlaskForm):
    nome_usuario = StringField("nome de usuário",validators=[InputRequired(message=ERROS['requerido']),
        Length(min=1,max=20,message=ERROS['quant_caracter_usuario'])])
    senha = PasswordField("Senha",validators=[InputRequired(message=ERROS['requerido'])])
    logar = SubmitField("logar")

class CadastroCidadeForm(FlaskForm):
    nome_cidade = StringField("nome da cidade", validators=[InputRequired(message=ERROS['requerido'])])
    descricao_cidade = TextAreaField("descrição da cidade")
    favorita = BooleanField("cidade favorita")
    notificacao = BooleanField("notificações por e-mail")
    enviar = SubmitField("enviar")

class EdicaoCidadeForm(FlaskForm):
    notificacao = BooleanField("notificação por e-mail")
    descricao_cidade = TextAreaField("descrição da cidade")
    favorita = BooleanField("cidade favorita")
    editar = SubmitField("editar")

class AvaliacaoSiteForm(FlaskForm):
    nota = FloatField("Nota de 0 a 10",validators=[InputRequired(message=ERROS['requerido']),
        NumberRange(min=0,max=10,message=ERROS['range_numeros'])])
    comentario = TextAreaField("Comentário sobre o site")
    avaliar = SubmitField("avaliar site")
    
